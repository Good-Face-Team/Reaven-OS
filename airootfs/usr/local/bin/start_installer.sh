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

# Автозапуск установщика с правильными настройками

# Ждем завершения инициализации
sleep 2

# Запускаем X-сервер с автоматическим определением разрешения
Xorg :0 -verbose 3 &
export DISPLAY=:0

# Ждем запуска X
sleep 3

# Запускаем установщик
python3 /usr/local/bin/installer.py
