#!/bin/bash
# Скрипт автозапуска установщика Reaven OS (работает как login shell)

echo ""
echo "🎮 Добро пожаловать в Reaven OS!"
echo "🔄 Запуск установщика через 3 секунды..."
echo ""

# Ждем немного
sleep 3

# Проверяем что X-сервер не запущен
if ! pgrep -x "Xorg" > /dev/null; then
    echo "🚀 Запускаем X-сервер и установщик..."
    exec startx /usr/bin/python3 /usr/local/bin/boot_screen.py -- /usr/bin/Xorg -screen 1280x720 -keeptty
else
    echo "✅ X-сервер уже запущен"
    export DISPLAY=:0
    exec python3 /usr/local/bin/boot_screen.py
fi

# Если что-то пошло не так, запускаем резервную оболочку
exec /bin/bash
