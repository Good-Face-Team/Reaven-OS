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
import tkinter as tk
from tkinter import ttk
import time
import subprocess
import os
from helper import create_gradient # Импортируем нашу функцию

class BootScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1280x720+0+0")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#000000') # Черный фон по умолчанию
        self.root.overrideredirect(True)
        
        # Цвета градиента (современный синий)
        self.color_top = "#0a1a3a"
        self.color_bottom = "#000011"
        
        self.canvas = tk.Canvas(self.root, bg=self.color_bottom, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        self.setup_ui()
        
        # Привязываем отрисовку градиента к изменению размера окна
        self.canvas.bind('<Configure>', self.draw_gradient_background)
        
        # Запускаем анимацию и переход
        self.animate_dots(0)
        self.root.after(3000, self.launch_installer) # Даем 3 секунды
        
    def draw_gradient_background(self, event):
        """Рисует фон при изменении размера окна."""
        create_gradient(self.canvas, event.width, event.height, self.color_top, self.color_bottom)
        # Перемещаем текст поверх градиента
        self.canvas.tag_raise("text")

    def setup_ui(self):
        """Настраивает текст на экране."""
        self.canvas.create_text(self.root.winfo_screenwidth() / 2, 
                               self.root.winfo_screenheight() / 2 - 50, 
                               text="Reaven OS", 
                               fill='white', font=('Arial', 64, 'bold'),
                               tags="text")
        
        self.loading_text = self.canvas.create_text(
                               self.root.winfo_screenwidth() / 2, 
                               self.root.winfo_screenheight() / 2 + 30, 
                               text="Запуск установщика", 
                               fill='#aaccff', font=('Arial', 24),
                               tags="text")

    def animate_dots(self, dot_count):
        """Анимирует точки '...'"""
        dots = "." * (dot_count % 4)
        self.canvas.itemconfig(self.loading_text, text=f"Запуск установщика{dots}")
        self.root.after(500, self.animate_dots, dot_count + 1)
    
    def launch_installer(self):
        self.root.destroy()
        # Убедитесь, что installer.py находится в /usr/local/bin
        os.system("python3 /usr/local/bin/installer.py")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    boot = BootScreen()
    boot.run()
