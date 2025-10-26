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
