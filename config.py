import os

# Секретный ключ для защиты сессий
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY не задан в .env")

# Хеш пароля администратора
ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH")
