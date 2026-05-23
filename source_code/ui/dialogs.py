import tkinter as tk
from tkinter import messagebox, filedialog

class NewDraftDialog:
    """新建草稿对话框"""
    def __init__(self, parent, on_confirm):
        self.parent = parent
        self.on_confirm = on_confirm
        self.dialog = None
        self.create()
    
    def create(self):
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("新建草稿")
        self.dialog.geometry("300x150")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        tk.Label(self.dialog, text="文件名（不需要加.html）:").pack(pady=10)
        self.entry = tk.Entry(self.dialog, width=30)
        self.entry.pack(pady=5)
        
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="确定", command=self.confirm).pack(side=tk.LEFT, padx=20)
        tk.Button(button_frame, text="取消", command=self.dialog.destroy).pack(side=tk.LEFT, padx=20)
        
        self.entry.focus()
        self.dialog.bind("<Return>", lambda e: self.confirm())
    
    def confirm(self):
        name = self.entry.get().strip()
        if name:
            self.dialog.destroy()
            self.on_confirm(name)
        else:
            messagebox.showerror("错误", "文件名不能为空")

class OpenDraftDialog:
    """打开草稿对话框"""
    def __init__(self, parent, drafts, on_open, on_import):
        self.parent = parent
        self.drafts = drafts
        self.on_open = on_open
        self.on_import = on_import
        self.dialog = None
        self.create()
    
    def create(self):
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("选择草稿")
        self.dialog.geometry("450x400")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        tk.Label(self.dialog, text="我的草稿", font=("Arial", 14)).pack(pady=10)
        
        listbox_frame = tk.Frame(self.dialog)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        if self.drafts:
            for d in self.drafts:
                self.listbox.insert(tk.END, d)
        else:
            self.listbox.insert(tk.END, "（暂无草稿）")
        
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="打开", width=10, command=self.open_draft).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="从其他文件夹导入", width=15, command=self.import_draft).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="取消", width=10, command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        self.listbox.bind("<Double-Button-1>", lambda e: self.open_draft())
    
    def open_draft(self):
        if not self.drafts:
            messagebox.showinfo("提示", "暂无草稿，请先新建")
            return
        
        sel = self.listbox.curselection()
        if sel:
            selected = self.listbox.get(sel)
            if selected != "（暂无草稿）":
                self.dialog.destroy()
                self.on_open(selected)
    
    def import_draft(self):
        self.dialog.destroy()
        self.on_import()

class ExportConfirmDialog:
    """导出确认对话框"""
    def __init__(self, parent, html_content, on_yes, on_no):
        self.parent = parent
        self.html_content = html_content
        self.on_yes = on_yes
        self.on_no = on_no
        self.create()
    
    def create(self):
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("确认导出")
        self.dialog.geometry("600x500")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        tk.Label(self.dialog, text="是否保存以下代码？", font=("Arial", 12)).pack(pady=10)
        
        text_frame = tk.Frame(self.dialog)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_preview = tk.Text(text_frame, yscrollcommand=scrollbar.set, wrap=tk.WORD)
        self.text_preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_preview.yview)
        
        self.text_preview.insert(tk.END, self.html_content)
        self.text_preview.config(state=tk.DISABLED)
        
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="是", width=10, command=self.on_yes).pack(side=tk.LEFT, padx=20)
        tk.Button(button_frame, text="否", width=10, command=self.on_no).pack(side=tk.LEFT, padx=20)