import tkinter as tk
from tkinter import messagebox

class MainMenu:
    def __init__(self, root, on_new_draft, on_open_draft, on_quit):
        self.root = root
        self.on_new_draft = on_new_draft
        self.on_open_draft = on_open_draft
        self.on_quit = on_quit
        self.create_ui()
    
    def create_ui(self):
        self.root.title("PowerHTML 1.0 - 主菜单")
        self.root.geometry("400x300")
        
        tk.Label(self.root, text="PowerHTML 1.0", font=("Arial", 20)).pack(pady=30)
        tk.Button(self.root, text="新建草稿", width=20, height=2, command=self.on_new_draft).pack(pady=10)
        tk.Button(self.root, text="打开我的草稿", width=20, height=2, command=self.on_open_draft).pack(pady=10)
        tk.Button(self.root, text="退出", width=20, height=2, command=self.on_quit).pack(pady=10)