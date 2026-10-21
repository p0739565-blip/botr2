"""Тексты сообщений бота — собраны в одном месте, чтобы не искать
формулировки по всем handlers/*.py."""

NEED_CHANNEL_SUB_TEXT = (
    "Привет! Чтобы получить доступ к VPN, подпишись на наш канал "
    "и нажми «Я подписался»."
)

WELCOME_TEXT = (
    "👋 Добро пожаловать в Маквин VPN\n\n"
    "Быстрый и стабильный VPN.\n\n"
    "Выберите действие:"
)

NOT_SUBSCRIBED_ALERT = "Ты пока не подписан на канал 🙁"

ALREADY_HAS_SUBSCRIPTION_TEXT = (
    "У вас уже есть подписка.\n"
    "Используйте кнопку 💳 Купить подписку для продления."
)

INVOICE_TITLE = "Подписка Маквин VPN"

PAYMENT_THANKS_TEXT = "✅ Оплата прошла успешно! Готовим вашу подписку..."


def buy_subscription_text(price_stars: int, days: int) -> str:
    return (
        "💳 Покупка подписки Маквин VPN\n\n"
        f"⭐ Telegram Stars — {price_stars} за {days} дней\n"
        "💳 Банковская карта — скоро доступно\n"
        "₿ Криптовалюта — скоро доступно\n\n"
        "Нажмите кнопку ниже, чтобы оплатить Stars 👇"
    )


def invoice_description_text(days: int) -> str:
    return f"Доступ к VPN на {days} дней. Оплата через Telegram Stars."

NO_ACTIVE_SUBSCRIPTION_TEXT = (
    "❌ У вас пока нет активной подписки.\n\n"
    "Оформите через 💳 Купить подписку."
)

INSTRUCTION_TEXT = (
    "📖 Инструкция Маквин VPN\n\n"
    "1️⃣ Установите клиент:\n"
    "• Android — Happ / v2rayNG\n"
    "• Windows — v2rayN\n"
    "• iOS — Streisand / Shadowrocket\n\n"
    "2️⃣ Оформите подписку — 🚀 Получить VPN (бесплатный пробный период "
    "при первом заходе) или 💳 Купить подписку\n\n"
    "3️⃣ Добавьте ссылку подписки в приложение.\n\n"
    "VPN обновляется автоматически."
)

SUPPORT_TEXT = (
    "🆘 Поддержка Маквин VPN\n\n"
    "Если возникли проблемы:\n"
    "• проверьте интернет\n"
    "• обновите подписку\n"
    "• перезапустите VPN клиент\n\n"
    "Если это не помогло — нажмите кнопку ниже, чтобы создать обращение "
    "в поддержку, и мы ответим вам прямо здесь, в этом чате."
)

TICKET_ASK_DESCRIPTION_TEXT = (
    "📝 Опишите проблему текстом — что именно не работает, "
    "на каком устройстве и когда началось."
)

TICKET_ASK_ATTACHMENTS_TEXT = (
    "📎 Если есть скриншот или видео проблемы — пришлите их сейчас "
    "(можно несколько). Когда закончите — нажмите «✅ Отправить заявку»."
)

TICKET_ATTACHMENT_RECEIVED_TEXT = "Вложение добавлено. Можете прислать ещё, или нажмите «✅ Отправить заявку»."

TICKET_CREATED_TEXT = (
    "✅ Заявка #{ticket_id} создана.\n\n"
    "Мы ответим вам прямо здесь, в этом чате, как только сможем. "
    "Можете писать дополнительные сообщения — они попадут в это же обращение."
)

TICKET_ALREADY_OPEN_TEXT = (
    "У вас уже есть открытое обращение #{ticket_id}. "
    "Просто напишите сообщение сюда — оно попадёт в поддержку."
)

TICKET_MESSAGE_FORWARDED_TEXT = "✅ Сообщение отправлено в поддержку."

TICKET_CLOSED_NOTICE_TEXT = (
    "ℹ️ Ваше обращение #{ticket_id} закрыто поддержкой. "
    "Если проблема повторилась — создайте новое обращение через 🆘 Поддержка."
)

TICKET_EXIT_TEXT = "Вы вышли из чата с поддержкой. Обращение остаётся открытым — просто напишите ещё раз, если понадобится."


def subscription_issued_text(sub_url: str, expiry_str: str) -> str:
    return (
        "✅ Подписка выдана!\n\n"
        f"Действует до: {expiry_str}\n\n"
        f"Ссылка для добавления в клиент (v2rayN, Happ, Hiddify и т.д.):\n"
        f"`{sub_url}`\n\n"
        "Или отсканируйте QR-код ниже."
    )


def my_subscription_text(status: str, expiry_str: str, sub_url: str) -> str:
    return (
        "📱 Ваша подписка\n\n"
        f"Статус: {status}\n"
        f"До: {expiry_str}\n\n"
        f"Ссылка для добавления в клиент (v2rayN, Happ, Hiddify и т.д.):\n"
        f"`{sub_url}`\n\n"
        "Или отсканируйте QR-код ниже."
    )


def profile_text(
    created_at_str: str,
    balance: int,
    total_invited: int,
    paid_invited: int,
    sub_status: str | None = None,
    sub_expiry_str: str | None = None,
    sub_url: str | None = None,
) -> str:
    if sub_url:
        sub_block = (
            "📶 Подписка\n"
            f"Статус: {sub_status}\n"
            f"До: {sub_expiry_str}\n"
            f"Ссылка:\n`{sub_url}`\n"
            "(или отсканируйте QR-код ниже)"
        )
    else:
        sub_block = (
            "📶 Подписка\n"
            "Пока нет — оформите через 💳 Купить подписку."
        )

    return (
        "👤 Мой профиль\n\n"
        f"Регистрация: {created_at_str}\n"
        f"Баланс: {balance}₽\n\n"
        f"{sub_block}\n\n"
        "🤝 Рефералы\n"
        f"Приглашено: {total_invited} (оплатили: {paid_invited})\n\n"
        "Подробнее и ссылка-приглашение — в разделе 🤝 Реферальная программа."
    )
