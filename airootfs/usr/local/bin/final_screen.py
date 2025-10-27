#!/usr/bin/env python3

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

import tkinter as tk
from tkinter import ttk
import time
import subprocess
import threading
import os
from helper import create_gradient # Импортируем нашу функцию

class FinalScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1280x720+0+0")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#000000')
        self.root.overrideredirect(True)

        self.root.config(cursor="none")
        
        # Цвета градиента
        self.color_top = "#0a1a3a"
        self.color_bottom = "#000011"
        
        self.canvas = tk.Canvas(self.root, bg=self.color_bottom, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        self.load_user_data()
        self.setup_ui()
        
        self.canvas.bind('<Configure>', self.draw_gradient_background)
        self.start_countdown()
    
    def load_user_data(self):
        """Загружает данные пользователя из временного файла."""
        self.username = "user" # По умолчанию
        self.password = "reaven123" # По умолчанию
        try:
            with open("/tmp/user.info", "r") as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    self.username = lines[0].strip()
                    self.password = lines[1].strip()
            os.remove("/tmp/user.info") # Очищаем
        except Exception as e:
            print(f"Не удалось прочитать /tmp/user.info: {e}")

    def draw_gradient_background(self, event):
        """Рисует фон при изменении размера окна."""
        create_gradient(self.canvas, event.width, event.height, self.color_top, self.color_bottom)
        self.canvas.tag_raise("text") # Поднимаем текст наверх

    def setup_ui(self):
        """Настраивает интерфейс финального экрана"""
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()

        self.canvas.create_text(sw / 2, sh / 2 - 150, 
                               text="Система почти готова", 
                               fill='white', font=('Arial', 48, 'bold'),
                               tags="text")
        
        self.dots = self.canvas.create_text(sw / 2, sh / 2 - 90, 
                               text="Завершение установки", 
                               fill='#aaccff', font=('Arial', 24),
                               tags="text")
        
        self.countdown_text = self.canvas.create_text(sw / 2, sh / 2, 
                               text="Перезагрузка через: 10", 
                               fill='#aaccff', font=('Arial', 20),
                               tags="text")
        
        info = f"""
        Reaven OS успешно установлена!

        Данные для входа:
        Логин: {self.username}
        Пароль: {self.password}

        Сайт: https://reaven.goodfaceteam.ru
        """
        
        self.canvas.create_text(sw / 2, sh / 2 + 120, text=info, 
                               fill='#cccccc', font=('Arial', 14), 
                               justify='center', tags="text")
    
    def start_countdown(self):
        """Запускает обратный отсчет"""
        def countdown():
            for i in range(10, 0, -1):
                self.canvas.itemconfig(self.countdown_text, 
                                     text=f"Перезагрузка через: {i}")
                
                # Анимация точек
                dots = "." * (i % 4)
                self.canvas.itemconfig(self.dots, text=f"Завершение установки{dots}")
                
                self.root.update()
                time.sleep(1)
            
            # Финальное сообщение
            self.canvas.itemconfig(self.countdown_text, 
                                 text="Перезагрузка...", fill="white")
            self.canvas.itemconfig(self.dots, text="")
            self.root.update()
            time.sleep(2)
            
            # Перезагрузка
            subprocess.run("reboot", shell=True)
        
        thread = threading.Thread(target=countdown)
        thread.daemon = True
        thread.start()
    
    def run(self):
        """Запуск финального экрана"""
        self.root.mainloop()

if __name__ == "__main__":
    final = FinalScreen()
    final.run()
