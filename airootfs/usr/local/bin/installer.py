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
from tkinter import ttk, messagebox, filedialog
import subprocess
import threading
import os
import time
import sys
from helper import create_gradient # Импортируем нашу функцию

class RavenOSInstaller:
    def __init__(self):
        if "DISPLAY" not in os.environ:
            print("🚀 Запускаю Xorg автоматически...")
            subprocess.run("Xorg :0 &", shell=True)
            time.sleep(2)
            os.environ["DISPLAY"] = ":0"
            
        self.root = tk.Tk()
        self.root.title("Reaven OS Installer")
        self.root.geometry("1280x720+0+0")
        self.root.attributes('-fullscreen', True)
        
        # --- НОВЫЙ ФОН ---
        # Цвета градиента
        self.color_top = "#0a1a3a"
        self.color_bottom = "#2a0a2a"
        
        self.bg_canvas = tk.Canvas(self.root, bg=self.color_bottom, highlightthickness=0)
        self.bg_canvas.pack(fill='both', expand=True)
        self.bg_canvas.bind('<Configure>', self.draw_gradient_background)
        # --- КОНЕЦ НОВОГО ФОНА ---

        # Данные пользователя
        self.current_step = 0
        self.username = tk.StringVar(value="user")
        self.password = tk.StringVar(value="reaven123")
        self.hostname = tk.StringVar(value="reavenos")
        self.timezone = tk.StringVar(value="Europe/Moscow")
        self.locale = tk.StringVar(value="en_US.UTF-8")
        self.keyboard_layout = tk.StringVar(value="us")
        self.selected_disk = tk.StringVar(value="")
        self.use_goodface_id = tk.BooleanVar(value=False)
        self.goodface_email = tk.StringVar(value="")
        self.goodface_password = tk.StringVar(value="")
        
        # Флаг установки
        self.installation_started = False
        self.installation_completed = False
        
        # Список дисков
        self.disks = []
        
        self.setup_ui()
        self.load_disks()

    def draw_gradient_background(self, event):
        """Рисует фон при изменении размера окна."""
        create_gradient(self.bg_canvas, event.width, event.height, self.color_top, self.color_bottom)

    def setup_ui(self):
        # --- ИЗМЕНЕНО ---
        # Основной фрейм теперь это "карточка" поверх холста
        # Используем tk.Frame, чтобы легко задать белый фон
        self.main_frame = tk.Frame(self.bg_canvas, bg='#ffffff', bd=2, relief='ridge')
        # Размещаем по центру, занимая 70% ширины и 80% высоты
        self.main_frame.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.8, relheight=0.9)
        
        # Применяем стиль к ttk виджетам внутри
        style = ttk.Style(self.root)
        style.configure("Accent.TButton", font=("Arial", 12, "bold"), foreground="white", background="#007acc")
        style.configure('.', font=('Arial', 11))
        style.configure('TLabel', background='#ffffff')
        style.configure('TFrame', background='#ffffff')
        style.configure('TCheckbutton', background='#ffffff')
        
        # --- КОНЕЦ ИЗМЕНЕНИЙ ---
        
        # Заголовок (внутри main_frame)
        title_frame = ttk.Frame(self.main_frame)
        title_frame.pack(fill='x', pady=(10, 20), padx=20)
        
        ttk.Label(title_frame, text="Reaven OS", font=('Arial', 24, 'bold')).pack(side='left')
        ttk.Label(title_frame, text="Установка системы", font=('Arial', 14)).pack(side='right')
        
        # Основной контент
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Кнопки навигации
        self.nav_frame = ttk.Frame(self.main_frame)
        self.nav_frame.pack(fill='x', pady=(20, 20), padx=20)
        
    
        # --- ИЗМЕНЕНО: Используем .grid() для кнопок навигации ---
        # Настраиваем две колонки в nav_frame, чтобы они занимали по 50% ширины
        self.nav_frame.columnconfigure(0, weight=1)
        self.nav_frame.columnconfigure(1, weight=1)

        self.back_btn = ttk.Button(self.nav_frame, text="Назад", command=self.previous_step)
        # Размещаем кнопку в первой колонке и растягиваем по горизонтали (ew = east-west)
        self.back_btn.grid(row=0, column=0, sticky='ew', padx=5, ipady=5)
        
        self.next_btn = ttk.Button(self.nav_frame, text="Далее", command=self.next_step, style="Accent.TButton")
        # Размещаем кнопку во второй колонке и растягиваем
        self.next_btn.grid(row=0, column=1, sticky='ew', padx=5, ipady=5)
        # --- КОНЕЦ ИЗМЕНЕНИЙ ---

          
        self.show_step(0)
        
    def show_step(self, step):
        self.current_step = step
        # Очищаем контент
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        steps = [
            self.step_welcome,
            self.step_disk_selection,
            self.step_region,
            self.step_user_account,
            self.step_installation,
            self.step_finish
        ]
        
        if step < len(steps):
            steps[step]()
            
        # Обновляем кнопки навигации
        self.back_btn.config(state='normal' if step > 0 else 'disabled')
        
        if step == len(steps) - 1:
            if self.installation_completed:
                self.next_btn.config(text="Завершить", command=self.finish_installation)
            else:
                self.next_btn.config(text="Начать установку", command=self.start_installation)
        elif step == len(steps) - 2:  # Шаг перед установкой
            self.next_btn.config(text="Начать установку", command=self.start_installation)
        else:
            self.next_btn.config(text="Далее", command=self.next_step)
    
    def step_welcome(self):
        content = ttk.Frame(self.content_frame)
        content.pack(fill='both', expand=True, padx=50, pady=50)
        
        ttk.Label(content, text="Добро пожаловать в Reaven OS!", 
                 font=('Arial', 20, 'bold')).pack(pady=20)
        
        ttk.Label(content, text="Игровой дистрибутив на основе Arch Linux",
                 font=('Arial', 14)).pack(pady=10)
        
        features = [
            "🎮 Готовый игровой компьютер с предустановленным Steam, Wine, Lutris",
            "🚀 Высокая производительность и оптимизация для игр",
            "🎨 Современный рабочий стол KDE Plasma",
            "🔧 Полная поддержка Vulkan и игровых технологий",
            "🌐 Интеграция с Good Face ID для облачной синхронизации"
        ]
        
        for feature in features:
            ttk.Label(content, text=feature, font=('Arial', 12)).pack(anchor='w', pady=5)
        
        ttk.Label(content, text="Нажмите 'Далее' чтобы продолжить установку",
                 font=('Arial', 11)).pack(pady=20)
    
    def step_disk_selection(self):
        content = ttk.Frame(self.content_frame)
        content.pack(fill='both', expand=True)
        
        ttk.Label(content, text="Выберите диск для установки", 
                 font=('Arial', 16, 'bold')).pack(pady=20)
        
        # Фрейм для списка дисков
        disk_frame = ttk.Frame(content)
        disk_frame.pack(fill='both', expand=True, padx=50)
        
        # Список дисков
        self.disk_listbox = tk.Listbox(disk_frame, height=10, font=('Arial', 11), 
                                      bg='#f0f0f0', bd=1, relief='solid')
        self.disk_listbox.pack(fill='both', expand=True)
        
        for disk in self.disks:
            self.disk_listbox.insert('end', f"{disk['name']} - {disk['size']} - {disk['model']}")
        
        # Кнопки управления дисками
        disk_buttons = ttk.Frame(content)
        disk_buttons.pack(pady=10)
        
        ttk.Button(disk_buttons, text="Обновить список", 
                  command=self.load_disks).pack(side='left', padx=5)
        ttk.Button(disk_buttons, text="Форматировать диск", 
                  command=self.format_disk).pack(side='left', padx=5)
        
        # Информация о выбранном диске
        self.disk_info = ttk.Label(content, text="Выберите диск из списка", 
                                  font=('Arial', 10))
        self.disk_info.pack(pady=10)
        
        # Привязываем выбор в списке
        self.disk_listbox.bind('<<ListboxSelect>>', self.on_disk_select)
    
    def step_region(self):
        content = ttk.Frame(self.content_frame)
        content.pack(fill='both', expand=True, padx=50, pady=20)
        
        ttk.Label(content, text="Настройка региона и времени", 
                 font=('Arial', 16, 'bold')).pack(pady=20)
        
        # Часовой пояс
        ttk.Label(content, text="Часовой пояс:").pack(anchor='w')
        timezone_combo = ttk.Combobox(content, textvariable=self.timezone,
                                     values=["Europe/Moscow", "Europe/London", "America/New_York", "Asia/Yekaterinburg"])
        timezone_combo.pack(fill='x', pady=5)
        
        # Локаль
        ttk.Label(content, text="Локаль:").pack(anchor='w', pady=(10,0))
        locale_combo = ttk.Combobox(content, textvariable=self.locale,
                                   values=["en_US.UTF-8", "ru_RU.UTF-8"])
        locale_combo.pack(fill='x', pady=5)
        
        # Раскладка клавиатуры
        ttk.Label(content, text="Раскладка клавиатуры:").pack(anchor='w', pady=(10,0))
        keyboard_combo = ttk.Combobox(content, textvariable=self.keyboard_layout,
                                     values=["us", "ru"])
        keyboard_combo.pack(fill='x', pady=5)
    
    def step_user_account(self):
        content = ttk.Frame(self.content_frame)
        content.pack(fill='both', expand=True, padx=50, pady=20)
        
        ttk.Label(content, text="Создание учетной записи", 
                 font=('Arial', 16, 'bold')).pack(pady=20)
        
        # Основная учетная запись
        ttk.Label(content, text="Имя пользователя:").pack(anchor='w')
        ttk.Entry(content, textvariable=self.username).pack(fill='x', pady=5)
        
        ttk.Label(content, text="Пароль:").pack(anchor='w', pady=(10,0))
        ttk.Entry(content, textvariable=self.password, show="*").pack(fill='x', pady=5)
        
        ttk.Label(content, text="Имя компьютера:").pack(anchor='w', pady=(10,0))
        ttk.Entry(content, textvariable=self.hostname).pack(fill='x', pady=5)
        
        # Good Face ID
        ttk.Checkbutton(content, text="Войти через Good Face ID", 
                       variable=self.use_goodface_id).pack(anchor='w', pady=(20,0))
        
        self.gf_frame = ttk.Frame(content)
        
        ttk.Label(self.gf_frame, text="Email Good Face ID:").pack(anchor='w')
        ttk.Entry(self.gf_frame, textvariable=self.goodface_email).pack(fill='x', pady=5)
        
        ttk.Label(self.gf_frame, text="Пароль Good Face ID:").pack(anchor='w', pady=(10,0))
        ttk.Entry(self.gf_frame, textvariable=self.goodface_password, show="*").pack(fill='x', pady=5)
        
        # Привязываем видимость Good Face ID полей
        self.use_goodface_id.trace('w', self.toggle_goodface_fields)
        self.toggle_goodface_fields()
    
    def step_installation(self):
        content = ttk.Frame(self.content_frame)
        content.pack(fill='both', expand=True)
        
        ttk.Label(content, text="Установка системы", 
                 font=('Arial', 16, 'bold')).pack(pady=20)
        
        if not self.installation_started:
            # Экран перед установкой
            ttk.Label(content, text="Всё готово к установке!", 
                     font=('Arial', 14)).pack(pady=10)
            
            ttk.Label(content, text="Параметры установки:", 
                     font=('Arial', 12, 'bold')).pack(pady=(20, 10))
            
            summary_text = f"""
            Диск: {self.selected_disk.get()}
            Пользователь: {self.username.get()}
            Имя компьютера: {self.hostname.get()}
            Часовой пояс: {self.timezone.get()}
            Good Face ID: {'Да' if self.use_goodface_id.get() else 'Нет'}
            """
            
            ttk.Label(content, text=summary_text, font=('Arial', 11), justify='left').pack(pady=10)
            
            ttk.Label(content, text="Нажмите 'Начать установку' чтобы продолжить",
                     font=('Arial', 11)).pack(pady=20)
            
        else:
            # Экран установки
            # Прогресс-бар
            self.progress = ttk.Progressbar(content, mode='determinate')
            self.progress.pack(fill='x', padx=50, pady=10)
            
            # Список этапов
            self.steps_frame = ttk.Frame(content)
            self.steps_frame.pack(fill='both', expand=True, padx=50)
            
            # --- ИСПРАВЛЕН БАГ (добавлена запятая) ---
            self.installation_steps = [
                "Разметка диска",
                "Установка базовой системы",
                "Установка KDE Plasma",
                "Установка игровых пакетов",
                "Настройка системы",
                "Настройка брендинга",
                "Создание пользователя",
                "Настройка сервисов",
                "Завершение установки"
            ]
            
            self.step_labels = []
            for i, step in enumerate(self.installation_steps):
                label = ttk.Label(self.steps_frame, text=f"○ {step}", font=('Arial', 11))
                label.pack(anchor='w', pady=2)
                self.step_labels.append(label)
            
            # Лог установки
            self.log_text = tk.Text(content, height=8, bg='black', fg='white', 
                                   font=('Monospace', 9), bd=1, relief='solid')
            self.log_text.pack(fill='both', expand=True, padx=50, pady=10)
    
    def step_finish(self):
        content = ttk.Frame(self.content_frame)
        content.pack(fill='both', expand=True, padx=50, pady=50)
        
        if self.installation_completed:
            ttk.Label(content, text="Установка завершена!", 
                     font=('Arial', 20, 'bold'), foreground='green').pack(pady=20)
            
            ttk.Label(content, text="Reaven OS успешно установлена на ваш компьютер.",
                     font=('Arial', 14)).pack(pady=10)
            
            summary = f"""
            Имя пользователя: {self.username.get()}
            Имя компьютера: {self.hostname.get()}
            Часовой пояс: {self.timezone.get()}
            
            После перезагрузки вы сможете:
            • Войти в систему KDE Plasma
            • Запускать Steam и игры
            • Наслаждаться оптимизированной игровой системой
            """
            
            ttk.Label(content, text=summary, font=('Arial', 11), justify='left').pack(pady=20)
            
            ttk.Label(content, text="Нажмите 'Завершить' для перехода к экрану перезагрузки.", font=('Arial', 11)).pack(pady=10)

            # --- ИЗМЕНЕНО: Используем .grid() для финальной кнопки ---
            finish_frame = ttk.Frame(content)
            finish_frame.pack(fill="x", pady=30, expand=True) # expand=True поможет с центрированием
            
            # Настраиваем одну колонку, которая займет всё пространство
            finish_frame.columnconfigure(0, weight=1)

            finish_btn = ttk.Button(finish_frame, text="ЗАВЕРШИТЬ УСТАНОВКУ", 
                                  command=self.finish_installation,
                                  style="Accent.TButton")
            # Размещаем кнопку в сетке и растягиваем, делаем ее высокой
            finish_btn.grid(row=0, column=0, sticky="ew", ipady=10)
            # --- КОНЕЦ ИЗМЕНЕНИЙ ---
            
        else:
            ttk.Label(content, text="Установка не завершена", 
                     font=('Arial', 16, 'bold'), foreground='red').pack(pady=20)
            ttk.Label(content, text="Произошла ошибка во время установки.\nПожалуйста, проверьте лог на предыдущем экране.",
                     font=('Arial', 12), justify='center').pack(pady=10)
    
    def toggle_goodface_fields(self, *args):
        if self.use_goodface_id.get():
            self.gf_frame.pack(fill='x', pady=10)
        else:
            self.gf_frame.pack_forget()
    
    def load_disks(self):
        self.disks = []
        try:
            result = subprocess.run("lsblk -J -o NAME,SIZE,MODEL,MOUNTPOINT", 
                                  shell=True, capture_output=True, text=True, check=True)
            import json
            disks_data = json.loads(result.stdout)
            
            for device in disks_data['blockdevices']:
                if device['name'].startswith(('sd', 'vd', 'nvme')) and not device.get('mountpoint'):
                    self.disks.append({
                        'name': f"/dev/{device['name']}",
                        'size': device['size'],
                        'model': device.get('model', 'Unknown'),
                    })
            
            if hasattr(self, 'disk_listbox'):
                self.disk_listbox.delete(0, 'end')
                for disk in self.disks:
                    self.disk_listbox.insert('end', f"{disk['name']} - {disk['size']} - {disk['model']}")
                    
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить список дисков: {e}\n{getattr(e, 'stderr', '')}")
    
    def on_disk_select(self, event):
        selection = self.disk_listbox.curselection()
        if selection:
            disk_index = selection[0]
            self.selected_disk.set(self.disks[disk_index]['name'])
            disk_info = self.disks[disk_index]
            self.disk_info.config(
                text=f"Выбран: {disk_info['name']} | Размер: {disk_info['size']} | Модель: {disk_info['model']}"
            )
    
    def format_disk(self):
        if not self.selected_disk.get():
            messagebox.showwarning("Внимание", "Выберите диск для форматирования")
            return
        
        if messagebox.askyesno("Подтверждение", 
                              f"ВНИМАНИЕ! Все данные на диске {self.selected_disk.get()} будут удалены!\n\nПродолжить?"):
            try:
                subprocess.run(f"wipefs -a {self.selected_disk.get()}", shell=True, check=True)
                subprocess.run(f"parted -s {self.selected_disk.get()} mklabel gpt", shell=True, check=True)
                messagebox.showinfo("Успех", "Диск успешно отформатирован")
                self.load_disks()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка форматирования: {e}")
    
    def next_step(self):
        if self.current_step == 1 and not self.selected_disk.get():
            messagebox.showwarning("Внимание", "Выберите диск для установки")
            return
        self.show_step(self.current_step + 1)
    
    def previous_step(self):
        self.show_step(self.current_step - 1)
    
    def start_installation(self):
        if not self.selected_disk.get():
            messagebox.showwarning("Внимание", "Сначала выберите диск для установки")
            return
            
        self.installation_started = True
        self.show_step(4)  # Переходим к экрану установки
        
        # Запускаем установку в отдельном потоке
        thread = threading.Thread(target=self.installation_process)
        thread.daemon = True
        thread.start()
    
    def update_progress(self, step, status):
        if step < len(self.step_labels):
            self.step_labels[step].config(text=f"✅ {self.installation_steps[step]}")
        
        self.progress['value'] = ((step + 1) / len(self.installation_steps)) * 100
        self.log_message(status)
    
    def log_message(self, message):
        if hasattr(self, 'log_text'):
            self.log_text.insert('end', f"{message}\n")
            self.log_text.see('end')
            self.root.update() # Обновляем UI
    
    def run_command(self, command):
        try:
            self.log_message(f"▶ {command}")
            # Используем Popen для потокового вывода, если нужно, но run проще
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            if result.stdout:
                self.log_message(f"  {result.stdout.strip()}")
            return True
        except subprocess.CalledProcessError as e:
            self.log_message(f"❌ Ошибка: {e.stderr}")
            return False
        except Exception as e:
            self.log_message(f"💥 Исключение: {str(e)}")
            return False
    
    def installation_process(self):
        try:
            disk = self.selected_disk.get()

            # Определяем суффиксы разделов
            part_suffix = "p" if "nvme" in disk else ""
            boot_part = f"{disk}{part_suffix}1"
            root_part = f"{disk}{part_suffix}2"

            # Этап 1: Разметка диска
            self.update_progress(0, "Разметка диска...")
            commands = [
                f"parted -s {disk} mklabel gpt",
                f"parted -s {disk} mkpart primary fat32 1MiB 513MiB",
                f"parted -s {disk} set 1 esp on",
                f"parted -s {disk} mkpart primary ext4 513MiB 100%",
                f"mkfs.fat -F32 {boot_part}",
                f"mkfs.ext4 -F {root_part}", # -F для принудительного форматирования
                f"mount {root_part} /mnt",
                f"mkdir -p /mnt/boot/efi",
                f"mount {boot_part} /mnt/boot/efi"
            ]

            for cmd in commands:
                if not self.run_command(cmd):
                    raise Exception(f"Ошибка выполнения: {cmd}")

            # Этап 2: Базовая система
            self.update_progress(1, "Установка базовой системы...")
            packages = "base linux linux-firmware sudo nano bash-completion networkmanager grub efibootmgr"
            if not self.run_command(f"pacstrap -K /mnt {packages}"): # -K для инициализации pacman keys
                raise Exception("Ошибка pacstrap")
            self.run_command("genfstab -U /mnt >> /mnt/etc/fstab")

            # Этап 3: KDE Plasma
            self.update_progress(2, "Установка рабочего стола...")
            packages = "xorg-server xorg-xinit sddm plasma dolphin konsole firefox"
            if not self.run_command(f"arch-chroot /mnt pacman -S --noconfirm {packages}"):
                self.log_message("⚠️ Ошибка установки KDE, но продолжаем...")

            # Этап 4: Игровые пакеты
            self.update_progress(3, "Установка игровых пакетов...")
            packages = "steam wine-staging lutris gamemode mangohud vulkan-icd-loader"
            self.run_command(f"arch-chroot /mnt pacman -S --noconfirm {packages}")

            # Этап 5: Настройка системы
            self.update_progress(4, "Настройка системы...")
            setup_commands = [
                f"echo '{self.hostname.get()}' > /mnt/etc/hostname",
                f"echo '{self.locale.get()} UTF-8' >> /mnt/etc/locale.gen",
                "echo 'ru_RU.UTF-8 UTF-8' >> /mnt/etc/locale.gen",
                "arch-chroot /mnt locale-gen",
                f"echo 'LANG={self.locale.get()}' > /mnt/etc/locale.conf",
                f"arch-chroot /mnt ln -sf /usr/share/zoneinfo/{self.timezone.get()} /etc/localtime",
                "arch-chroot /mnt hwclock --systohc"
            ]

            for cmd in setup_commands:
                self.run_command(cmd)

            # Этап 6: Брендинг
            self.update_progress(5, "Настройка брендинга...")
            os_release = f'''NAME="Reaven OS"
PRETTY_NAME="Reaven OS"
ID=reaven
BUILD_ID=rolling
HOME_URL="https://reaven.goodfaceteam.ru/"'''

            try:
                with open("/mnt/etc/os-release", "w") as f:
                    f.write(os_release)
            except Exception as e:
                self.log_message(f"⚠️ Не удалось записать os-release: {e}")

            # Этап 7: Создание пользователя
            self.update_progress(6, "Создание пользователя...")
            user_commands = [
                f"arch-chroot /mnt useradd -m -G wheel -s /bin/bash {self.username.get()}",
                f"echo '{self.username.get()}:{self.password.get()}' | arch-chroot /mnt chpasswd",
                "echo '%wheel ALL=(ALL) NOPASSWD: ALL' | tee /mnt/etc/sudoers.d/wheel_nopasswd"
            ]

            for cmd in user_commands:
                if not self.run_command(cmd):
                    raise Exception("Ошибка создания пользователя")

            # Этап 8: Настройка сервисов
            self.update_progress(7, "Настройка сервисов...")
            services = ["NetworkManager", "sddm", "bluetooth", "cups", "avahi-daemon"]
            for service in services:
                if self.run_command(f"arch-chroot /mnt systemctl enable {service}"):
                    self.log_message(f"✅ Включен сервис: {service}")
                else:
                    self.log_message(f"⚠️ Не удалось включить сервис: {service}")

            # Good Face ID настройка
            if self.use_goodface_id.get():
                self.log_message("Настройка Good Face ID...")
                gf_dir = "/mnt/home/{}/.goodface".format(self.username.get())
                self.run_command(f"mkdir -p {gf_dir}")
                with open("/mnt/usr/share/applications/goodface-id.desktop", "w") as f:
                    f.write('''[Desktop Entry]
Name=Good Face ID
Exec=firefox https://id.goodfaceteam.ru/
Icon=system-users
Type=Application''')

            # Загрузчик
            self.log_message("Установка загрузчика...")

            self.run_command("mkdir -p /mnt/boot/efi")

            self.run_command("mount --bind /sys/firmware/efi/efivars /mnt/sys/firmware/efi/efivars")

            boot_commands = [
                # Устанавливаем GRUB в EFI режиме
                f"arch-chroot /mnt grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=REAVEN_OS --recheck",
                # Создаем конфиг GRUB
                "arch-chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg"
            ]

            for cmd in boot_commands:
                if not self.run_command(cmd):
                    self.log_message(f"⚠️ Ошибка выполнения: {cmd}")
                    # Пробуем альтернативный метод
                    if "grub-install" in cmd:
                        self.log_message("Пробуем альтернативный метод установки GRUB...")

                        # --- ИСПРАВЛЕНИЕ 4: Убран '{disk}' из команды ---
                        alt_cmd = f"arch-chroot /mnt grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=REAVEN_OS --removable"
                        self.run_command(alt_cmd)

            # --- ИСПРАВЛЕНИЕ 5: Размонтируем efivars ---
            self.run_command("umount /mnt/sys/firmware/efi/efivars")

            self.update_progress(8, "Установка завершена!")
            self.log_message("🎉 Reaven OS успешно установлена!")

            self.installation_completed = True
            # Переходим к финальному экрану
            self.root.after(1000, lambda: self.show_step(5))

        except Exception as e:
            self.log_message(f"💥 Критическая ошибка: {str(e)}")
            messagebox.showerror("Ошибка", f"Установка прервана: {str(e)}")
            self.installation_completed = False
            self.root.after(1000, lambda: self.show_step(5)) # Показать экран ошибки

    def finish_installation(self):
        # --- ИЗМЕНЕНО ---
        # Сохраняем данные пользователя для final_screen.py
        try:
            with open("/tmp/user.info", "w") as f:
                f.write(f"{self.username.get()}\n")
                f.write(f"{self.password.get()}\n")
        except Exception as e:
            print(f"Не удалось сохранить user.info: {e}")
            
        # Запускаем финальный экран
        self.root.destroy()
        os.system("python3 /usr/local/bin/final_screen.py")
        # --- КОНЕЦ ИЗМЕНЕНИЙ ---
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    if not os.path.exists("/run/archiso") and "DISPLAY" not in os.environ:
        print("❌ Запускайте только из Live среды Arch!")
        # sys.exit(1) # Разкомментируйте для релиза
    
    app = RavenOSInstaller()
    app.run()
