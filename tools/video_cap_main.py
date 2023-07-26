import tkinter as tk
from tkinter import filedialog, messagebox

import os

initial_dir = os.path.join(os.getcwd(), "..", "sim_scenes")


def browse_file():
    if len(output_entry.get()) == 0:
        open_dir = initial_dir
    else:
        open_dir = os.path.dirname(input_entry.get())
    file_path = filedialog.askopenfilename(initialdir=open_dir, filetypes=[("场景模拟Python文件", "*.py")])
    if len(file_path) == 0:
        return
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)
    output_entry.delete(0, tk.END)
    output_entry.insert(0, file_path[0:-3] + ".mp4")
    check3d()


def browse_save():
    if len(output_entry.get()) == 0:
        save_dir = initial_dir
    else:
        save_dir = os.path.dirname(output_entry.get())
    save_path = filedialog.asksaveasfilename(initialdir=save_dir, filetypes=[("MP4视频文件", "*.mp4")])
    if len(save_path) > 4:
        if not save_path.endswith(".mp4"):
            save_path += ".mp4"
    else:
        return

    output_entry.delete(0, tk.END)
    output_entry.insert(0, save_path)
    check3d()


def generate():
    input = input_entry.get()
    output = output_entry.get()
    inputs = os.path.normpath(input).split(os.sep)
    # outputs = os.path.normpath(output).split(os.sep)
    if checkbox3d_var.get() == 1:
        # sim_video_3d_cap.bat fiction transformed_mars_ani_3d
        m_file = "sim_video_3d_cap"
    else:
        # sim_video_cap.bat science jupiter_moon_protects_earth
        m_file = "sim_video_cap"

    shell = u"%s %s %s \"%s\"" % (m_file, inputs[-2], inputs[-1][:-3], output)
    # shell = u"%s %s %s" % (m_file, inputs[-2], inputs[-1][:-3])
    import subprocess
    import sys

    # subprocess.Popen(shell, shell=True)
    # shell =shell.encode(sys.getfilesystemencoding())
    print(shell)
    subprocess.call(shell, shell=True)


def open_output_dir():
    output_file = output_entry.get()
    if len(output_file) == 0:
        return
    # filedialog.askdirectory(initialdir=output_dir)
    output_dir = os.path.dirname(output_file)
    os.system('start ' + output_dir)


def start():
    input = input_entry.get()
    output = output_entry.get()

    err_msg = ""

    if len(input) == 0:
        err_msg = "“模拟代码文件”不能为空\n"

    if len(output) == 0:
        err_msg += "“视频保存文件”不能为空\n"

    if len(err_msg) > 0:
        messagebox.showwarning("消息", err_msg)
        return

    if messagebox.askyesno("确认", "是否开始生成视频？"):
        generate()


def check3d():
    save_file = output_entry.get()
    if checkbox3d_var.get() == 1:
        if not save_file.endswith("_3d.mp4") and save_file.endswith(".mp4"):
            output_entry.delete(0, tk.END)
            output_entry.insert(0, save_file[:-4] + "_3d.mp4")
    else:
        if save_file.endswith("_3d.mp4"):
            output_entry.delete(0, tk.END)
            output_entry.insert(0, save_file[:-7] + ".mp4")


root = tk.Tk()
root.title("模拟器视频生成工具")

input_entry = tk.Entry(root, width=80)
input_entry.grid(row=0, column=2)
browse_button = tk.Button(root, text="模拟代码文件", command=browse_file)
browse_button.grid(row=0, column=1)

output_entry = tk.Entry(root, width=80)
output_entry.grid(row=1, column=2)
browse_save_button = tk.Button(root, text="视频保存文件", command=browse_save)
browse_save_button.grid(row=1, column=1)
open_output_dir_button = tk.Button(root, text="...", command=open_output_dir)
open_output_dir_button.grid(row=1, column=3)

checkbox3d_var = tk.IntVar()
checkbox3d = tk.Checkbutton(root, text="生成3D视频", command=check3d, variable=checkbox3d_var)
checkbox3d.grid(row=2, column=1)
generate_button = tk.Button(root, text="点击开始", width=20, command=start)
generate_button.grid(row=2, column=2)

# root.withdraw()  # 隐藏主窗口
screen_width = 680
screen_height = 200
x = (screen_width / 2) - (root.winfo_width() / 2)
y = (screen_height / 2) - (root.winfo_height() / 2)

root.geometry("%dx%d+%d+%d" % (screen_width, screen_height, x, y))
root.mainloop()
