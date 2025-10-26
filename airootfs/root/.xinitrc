#!/bin/bash
# Автозапуск установщика Reaven OS

# Запускаем boot_screen который покажет заставку и запустит installer
/usr/bin/python3 /usr/local/bin/boot_screen.py

# Если установщик завершился, запускаем резервный терминал
exec /usr/bin/xterm
