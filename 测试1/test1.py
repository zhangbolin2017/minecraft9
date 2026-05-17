import tkinter as tk
from PIL import Image, ImageTk

# 创建主窗口
root = tk.Tk()
】










root.title("点击我 Window")
# 设置窗口大小为 400x300
root.geometry("400x300")

# 创建标签并显示文本
label = tk.Label(root, text="吃掉它")
label.pack()

# 加载苹果图像和被咬过的苹果图像，这里假设图片名为 apple.png 和 bitten_apple.png 且在当前目录下
try:
    image = Image.open("apple.png")
    photo = ImageTk.PhotoImage(image)
    bitten_image = Image.open("bitten_apple.png")
    bitten_photo = ImageTk.PhotoImage(bitten_image)
except FileNotFoundError:
    print("未找到苹果图像文件，请确保 apple.png 和 bitten_apple.png 在当前目录下。")
    photo = None
    bitten_photo = None

# 用于显示图像的标签
image_label = tk.Label(root)
image_label.pack()

# 标记苹果是否被咬
is_bitten = False

# 定义按钮点击事件
def show_image():
    global is_bitten
    if photo and bitten_photo:
        if is_bitten:
            image_label.config(image=photo)
            image_label.image = photo
        else:
            image_label.config(image=bitten_photo)
            image_label.image = bitten_photo
        is_bitten = not is_bitten

# 创建按钮并设置点击事件
button = tk.Button(root, text="点击我", command=show_image)
button.pack()

# 进入主事件循环
root.mainloop()