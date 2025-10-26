#!/bin/bash
# Автозапуск Reaven OS Installer

# Проверяем что мы в Live среде и установщик еще не запущен
if [ -f /run/archiso/bootmnt/archiso.img ] && [ -z "$INSTALLER_STARTED" ]; then
    export INSTALLER_STARTED=1
    echo "🚀 Запускаем Reaven OS Installer..."
    
    # Ждем завершения инициализации
    sleep 5
    
    # Запускаем установщик
    startx /usr/bin/python3 /usr/local/bin/boot_screen.py -- /usr/bin/Xorg -keeptty &
fi
