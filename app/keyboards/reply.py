from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def main_menu(user_id: int) -> ReplyKeyboardMarkup:
    """user_id — внутренний ID пользователя в БД (User.id), не
    Telegram tg_id.

    "🚀 Получить VPN" (пробный период) показывается только до самой
    первой когда-либо выданной подписки — дальше на этом месте
    "🏪 Магазин" (см. app.handlers.shop): вводный бесплатный доступ
    имеет смысл предлагать один раз, а не показывать кнопку, которая
    после первого использования всё равно ведёт на "у вас уже есть
    подписка"."""

    # Локальный импорт — иначе циклический импорт с
    # app.services.subscription, который сам использует эту клавиатуру.
    from app.services.subscription import has_ever_had_subscription

    has_history = await has_ever_had_subscription(user_id)

    kb = ReplyKeyboardBuilder()

    if has_history:
        kb.row(
            KeyboardButton(text="🏪 Магазин")
        )
    else:
        kb.row(
            KeyboardButton(text="🚀 Получить VPN")
        )

    kb.row(
        KeyboardButton(text="💳 Купить подписку"),
        KeyboardButton(text="👤 Мой профиль")
    )

    kb.row(
        KeyboardButton(text="💰 Пополнить баланс"),
        KeyboardButton(text="🎟 Промокод")
    )

    kb.row(
        KeyboardButton(text="🤝 Реферальная программа")
    )

    kb.row(
        KeyboardButton(text="📖 Инструкция"),
        KeyboardButton(text="🆘 Поддержка")
    )
    kb.row(
        KeyboardButton(text="📚 Документы")
    )

    return kb.as_markup(
        resize_keyboard=True
    )
