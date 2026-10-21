from aiogram import F, Router
from aiogram.types import Message

router = Router()


@router.message(F.text == "🏪 Магазин")
async def shop_stub(message: Message):
    await message.answer(
        "🏪 Магазин\n\n"
        "Этот раздел сейчас в разработке.\n\n"
        "Скоро здесь можно будет покупать подписки на другие сервисы, "
        "а также дарить подарки Telegram 🎁.\n\n"
        "Следите за обновлениями!"
    )
