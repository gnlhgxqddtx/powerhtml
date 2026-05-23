import tkinter as tk
from tkinter import messagebox
from ui import MainMenu, EditorWindow, NewDraftDialog, OpenDraftDialog
from core import ProjectManager

class PowerHTML:
    def __init__(self):
        self.root = tk.Tk()
        self.project_manager = ProjectManager()
        self.current_editor = None
        
        self.main_menu = MainMenu(
            self.root,
            on_new_draft=self.new_draft,
            on_open_draft=self.open_draft,
            on_quit=self.quit_app
        )
    
    def new_draft(self):
        """新建草稿"""
        def do_new_draft(name):
            def open_editor():
                self.open_editor()
            
            if self.project_manager.new_draft(name, open_editor):
                messagebox.showinfo("成功", f"草稿 '{name}' 已创建")
        
        NewDraftDialog(self.root, do_new_draft)
    
    def open_draft(self):
        """打开草稿"""
        drafts = self.project_manager.get_drafts()
        
        def do_open_draft(name):
            def open_editor():
                self.open_editor()
            
            if self.project_manager.open_draft(name, open_editor):
                messagebox.showinfo("成功", f"已打开草稿 '{name}'")
        
        def do_import():
            def open_editor():
                self.open_editor()
            
            if self.project_manager.import_from_file(open_editor):
                messagebox.showinfo("成功", "已导入草稿")
        
        OpenDraftDialog(self.root, drafts, do_open_draft, do_import)
    
    def open_editor(self):
        """打开编辑器"""
        self.root.withdraw()
        self.current_editor = EditorWindow(
            self.project_manager.current_project,
            self.on_editor_closed
        )
    
    def on_editor_closed(self):
        """编辑器关闭回调"""
        self.root.deiconify()
        self.current_editor = None
    
    def quit_app(self):
        """退出应用"""
        if messagebox.askyesno("退出", "确定要退出吗？"):
            self.root.quit()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PowerHTML()
    app.run()