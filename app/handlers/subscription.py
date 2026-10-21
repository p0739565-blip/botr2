from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select

from app.config import SUB_DOMAIN
from app.db import async_session
from app.models import Subscription
from app.services.qr import make_qr
from app.services.referral import get_referral_stats
from app.services.subscription import send_subscription
from app.services.users import get_or_create_user, is_subscribed
from app.settings.tariffs import TARIFFS
from app.texts.messages import NOT_SUBSCRIBED_ALERT, profile_text

router = Router()


@router.callback_query(F.data == "check_sub")
async def cb_check_sub(callback: CallbackQuery, bot: Bot):
    user = await get_or_create_user(callback.from_user.id, callback.from_user.username)

    if not await is_subscribed(bot, callback.from_user.id):
        await callback.answer(NOT_SUBSCRIBED_ALERT, show_alert=True)
        return

    await callback.answer()
    await send_subscription(callback, user, TARIFFS["trial"]["days"])


@router.message(F.text == "👤 Мой профиль")
async def my_profile(message: Message):

    user = await get_or_create_user(
        message.from_user.id,
        message.from_user.username
    )

    async with async_session() as session:

        result = await session.execute(
            select(Subscription)
            .where(
                Subscription.user_id == user.id
            )
            .order_by(
                Subscription.created_at.desc()
            )
        )

        sub = result.scalars().first()

    stats = await get_referral_stats(user.id)
    created_at_str = user.created_at.strftime("%d.%m.%Y")

    if sub:
        expiry = sub.expiry.strftime("%d.%m.%Y %H:%M")
        status = "🟢 Активна" if sub.is_valid else "🔴 Истекла"
        sub_url = f"{SUB_DOMAIN}/sub/{sub.token}"

        text = profile_text(
            created_at_str=created_at_str,
            balance=stats["balance"],
            total_invited=stats["total_invited"],
            paid_invited=stats["paid_invited"],
            sub_status=status,
            sub_expiry_str=expiry,
            sub_url=sub_url,
        )

        qr_file = make_qr(sub_url)

        await message.answer_photo(
            photo=qr_file,
            caption=text,
            parse_mode="Markdown",
        )
        return

    text = profile_text(
        created_at_str=created_at_str,
        balance=stats["balance"],
        total_invited=stats["total_invited"],
        paid_invited=stats["paid_invited"],
    )

    await message.answer(text, parse_mode="Markdown")
