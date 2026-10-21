"""
Пополнение бонусного баланса на сумму, которую пользователь указывает
сам (в отличие от покупки подписки, где сумма зависит от тарифа).

Переиспользует всю существующую инфраструктуру создания платежей
(Platega/Stars) — она уже рассчитана на произвольный словарь "тарифа"
с полями title/card/stars/days, так что здесь просто собирается
синтетический "тариф" на введённую сумму вместо реального из TARIFFS.

tariff_key="topup" — зарезервированный ключ, по которому
app.webhooks.platega.process_status_update и
app.handlers.payment.successful_payment отличают пополнение баланса от
покупки подписки и зачисляют деньги на баланс вместо выдачи подписки.
"topup" не должен совпадать ни с одним реальным ключом в
app.settings.tariffs.TARIFFS.
"""

import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from app.keyboards.inline import topup_method_keyboard
from app.services import platega
from app.services.payments import (
    build_stars_invoice,
    create_card_payment,
    create_crypto_payment,
    create_sbp_payment,
)
from app.services.users import get_or_create_user

logger = logging.getLogger(__name__)

router = Router()

MIN_TOPUP = 10
MAX_TOPUP = 100_000


class BalanceTopupStates(StatesGroup):
    waiting_amount = State()


def _topup_tariff(amount: int) -> dict:
    return {
        "title": "Пополнение баланса",
        "days": 0,
        "card": amount,
        "stars": amount,
    }


@router.message(F.text == "💰 Пополнить баланс")
async def balance_topup_entry(message: Message, state: FSMContext):
    await state.set_state(BalanceTopupStates.waiting_amount)
    await message.answer(
        f"На какую сумму пополнить баланс?\n\n"
        f"Введите число от {MIN_TOPUP} до {MAX_TOPUP} (в рублях)."
    )


@router.message(BalanceTopupStates.waiting_amount, F.text)
async def receive_amount(message: Message, state: FSMContext):
    raw = message.text.strip().replace(" ", "")

    if not raw.isdigit():
        await message.answer(
            "Нужно просто число, например 500. Введите сумму ещё раз:"
        )
        return

    amount = int(raw)

    if not (MIN_TOPUP <= amount <= MAX_TOPUP):
        await message.answer(
            f"Сумма должна быть от {MIN_TOPUP} до {MAX_TOPUP}₽. "
            "Введите сумму ещё раз:"
        )
        return

    await state.update_data(topup_amount=amount)

    await message.answer(
        f"Пополнение на {amount}₽. Выберите способ оплаты:",
        reply_markup=topup_method_keyboard(),
    )


@router.callback_query(
    BalanceTopupStates.waiting_amount, F.data.startswith("topup_method_")
)
async def choose_topup_method(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    amount = data.get("topup_amount")

    if amount is None:
        await callback.answer("Сессия истекла, начните заново.", show_alert=True)
        await state.clear()
        return

    method = callback.data.removeprefix("topup_method_")

    user = await get_or_create_user(
        callback.from_user.id, callback.from_user.username
    )
    tariff = _topup_tariff(amount)

    await callback.answer()

    if method == "stars":
        invoice = build_stars_invoice(tariff)
        # payload с префиксом "topup:" — так successful_payment отличает
        # пополнение баланса от покупки подписки (см. докстринг модуля).
        await callback.message.answer_invoice(
            provider_token="",
            payload=f"topup:{amount}",
            **invoice,
        )
        await state.clear()
        return

    try:
        if method == "card":
            pay_url = await create_card_payment(
                user=user,
                chat_id=callback.message.chat.id,
                tariff_key="topup",
                tariff=tariff,
            )
        elif method == "sbp":
            pay_url = await create_sbp_payment(
                user=user,
                chat_id=callback.message.chat.id,
                tariff_key="topup",
                tariff=tariff,
            )
        elif method == "crypto":
            pay_url = await create_crypto_payment(
                user=user,
                chat_id=callback.message.chat.id,
                tariff_key="topup",
                tariff=tariff,
            )
        else:
            await state.clear()
            return
    except platega.PlategaError as e:
        logger.error(
            "balance_topup: Platega API error tg_id=%s amount=%s status=%s body=%s",
            callback.from_user.id, amount, e.status, e.body,
        )
        await callback.message.answer(
            "Не получилось создать ссылку на оплату. Попробуйте ещё раз "
            "чуть позже или оплатите через Telegram Stars."
        )
        await state.clear()
        return
    except Exception:
        logger.exception(
            "balance_topup: unexpected error tg_id=%s amount=%s",
            callback.from_user.id, amount,
        )
        await callback.message.answer(
            "Не получилось создать ссылку на оплату (техническая ошибка). "
            "Попробуйте ещё раз чуть позже или оплатите через Telegram Stars."
        )
        await state.clear()
        return

    await callback.message.answer(
        f"Пополнение баланса на {amount}₽.\n\n"
        "После оплаты баланс пополнится автоматически в течение пары минут.",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text="💳 Перейти к оплате",
                    url=pay_url,
                )
            ]]
        ),
    )
    await state.clear()
