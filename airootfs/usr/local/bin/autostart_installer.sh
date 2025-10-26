#!/bin/bash
#
# Good Face Team
# Developer: Vladislav Klimov
# Team period: 2021 - 2025
# File creation date: October 26, 2025
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

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
