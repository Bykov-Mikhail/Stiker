import tkinter as tk
from PIL import Image, ImageTk
import os
import sys

# === Функция для поиска файлов внутри .exe или в папке с программой ===
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# === Путь к папке с изображениями ===
images_folder = resource_path("images")

# === Автоматический поиск Screenshot_N.png в папке images ===
available_images = []
for i in range(1, 10):  # Ищем до Screenshot_9.png
    img_name = f"Screenshot_{i}.png"
    img_path = os.path.join(images_folder, img_name)
    if os.path.exists(img_path):
        available_images.append(img_path)
        print(f"✅ Найдено: {img_path}")
    else:
        print(f"❌ Не найдено: {img_path}")

if not available_images:
    print("❌ Не найдено ни одного изображения.")
    sys.exit("Ошибка: не найдены изображения для отображения")

current_index = 0

# === Создаем главное окно ===
root = tk.Tk()
root.title("Sticker")

# Убираем рамку окна
root.overrideredirect(True)
root.attributes("-topmost", True)

# === Переменные для перетаскивания окна ===
dragging = False
x_click = 0
y_click = 0

# === Функции управления окном ===
def start_move(event):
    global dragging, x_click, y_click
    dragging = True
    x_click = event.x_root
    y_click = event.y_root

def move_window(event):
    global x_click, y_click
    if dragging:
        dx = event.x_root - x_click
        dy = event.y_root - y_click
        new_x = root.winfo_x() + dx
        new_y = root.winfo_y() + dy
        root.geometry(f"+{new_x}+{new_y}")
        x_click = event.x_root
        y_click = event.y_root

def stop_move(event):
    global dragging
    dragging = False

# === Загрузка изображения ===
def load_image(index):
    global current_index, photo
    current_index = index
    image_path = available_images[current_index]

    try:
        image = Image.open(image_path).convert("RGBA")
        width, height = image.size
        photo = ImageTk.PhotoImage(image)
        canvas.config(width=width, height=height)
        canvas.delete("all")
        canvas.create_image(width // 2, height // 2, anchor="center", image=photo)
        root.geometry(f"{width}x{height}")
        print(f"🖼️ Открыто: {image_path}")
    except Exception as e:
        print(f"Ошибка при загрузке изображения: {e}")

# === Функции сворачивания/разворачивания ===
def minimize_window(event=None):
    root.withdraw()

def restore_window(event=None):
    root.deiconify()
    root.focus_force()

# === Переключение изображений стрелками ← → ===
def next_image(event=None):
    if current_index < len(available_images) - 1:
        load_image(current_index + 1)

def prev_image(event=None):
    if current_index > 0:
        load_image(current_index - 1)

# === Закрытие программы по ПКМ ===
def exit_app(event=None):
    root.quit()
    root.destroy()

# === Canvas для изображения ===
canvas = tk.Canvas(root, highlightthickness=0, bg='black')
canvas.pack(fill="both", expand=True)

# Привязка событий
canvas.bind("<ButtonPress-1>", start_move)
canvas.bind("<B1-Motion>", move_window)
canvas.bind("<ButtonRelease-1>", stop_move)

# Привязка горячих клавиш
root.bind("<Control-Alt-h>", lambda e: minimize_window())
root.bind("<Control-Alt-s>", lambda e: restore_window())
root.bind("<Right>", lambda e: next_image())
root.bind("<Left>", lambda e: prev_image())

# Привязка ПКМ — закрытие
canvas.bind("<Button-3>", exit_app)  # ПКМ на картинке
root.bind("<Button-3>", exit_app)    # ПКМ по окну

# === Первое изображение ===
load_image(current_index)

# Делаем окно фокусируемым (для работы горячих клавиш)
root.after(100, lambda: root.focus_force())

# === Запуск главного цикла ===
root.mainloop()