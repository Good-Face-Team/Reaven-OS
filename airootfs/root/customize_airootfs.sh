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

set -e -u

echo "=== Setting up Reaven OS Installer ==="

# Базовая настройка системы
echo "Configuring locale..."
echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
echo "ru_RU.UTF-8 UTF-8" >> /etc/locale.gen
locale-gen
echo "LANG=en_US.UTF-8" > /etc/locale.conf

echo "Setting timezone..."
ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime
hwclock --systohc

echo "Setting hostname..."
echo "reaven-live" > /etc/hostname

echo "Creating live user..."
useradd -m -G wheel -s /bin/bash liveuser
echo "liveuser:live" | chpasswd

echo "Configuring sudo..."
echo "%wheel ALL=(ALL) ALL" >> /etc/sudoers

echo "Setting up X11 autostart..."
mkdir -p /etc/X11/xinit/
cat > /etc/X11/xinit/xinitrc << 'XEOF'
#!/bin/bash

# Disable screen saving
xset -dpms
xset s off

# Start Reaven OS boot screen
if [ -f /usr/local/bin/boot_screen.py ]; then
    echo "Starting Reaven OS Boot Screen..."
    python3 /usr/local/bin/boot_screen.py
else
    echo "Boot screen not found, starting fallback..."
    xterm -geometry 80x24+0+0 -e "echo 'Reaven OS Installer'; bash"
fi
XEOF

chmod +x /etc/X11/xinit/xinitrc

echo "Enabling NetworkManager..."
systemctl enable NetworkManager

echo "=== Reaven OS setup complete! ==="
