"""
Good Face Team
Developer: Vladislav Klimov
Team period: 2021 - 2025
File creation date: October 26, 2025

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

#!/usr/bin/env python3

def create_gradient(canvas, width, height, color1, color2):
    """
    Рисует плавный вертикальный градиент на холсте.
    Удаляет старый градиент по тегу 'gradient'.
    """
    canvas.delete("gradient")
    
    # Разбираем цвета на R, G, B
    r1, g1, b1 = canvas.winfo_rgb(color1)
    r2, g2, b2 = canvas.winfo_rgb(color2)
    
    r_ratio = (r2 - r1) / height
    g_ratio = (g2 - g1) / height
    b_ratio = (b2 - b1) / height

    # Рисуем 1-пиксельные линии для создания градиента
    for i in range(height):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        
        # Конвертируем обратно в hex
        color = f'#{nr:04x}{ng:04x}{nb:04x}'
        
        canvas.create_line(0, i, width, i, fill=color, tags="gradient")
    
    # Перемещаем градиент на задний план
    canvas.tag_lower("gradient")
