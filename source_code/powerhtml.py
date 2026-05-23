import os
import json
import shutil
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from tkinter.font import Font
from tkinterweb import HtmlFrame
import math

# ==================== 图形类定义 ====================
class Shape:
    def __init__(self):
        self.color = [255, 0, 0]  # 默认红色
        self.borderwidth = 1
        self.bordercolor = [0, 0, 0]
    
    def to_html(self):
        pass

class Circle(Shape):
    def __init__(self, cx, cy, r):
        super().__init__()
        self.cx = cx
        self.cy = cy
        self.r = r
    
    def to_html(self):
        return f'<circle cx="{self.cx}" cy="{self.cy}" r="{self.r}" fill="rgb({self.color[0]},{self.color[1]},{self.color[2]})" stroke="rgb({self.bordercolor[0]},{self.bordercolor[1]},{self.bordercolor[2]})" stroke-width="{self.borderwidth}"/>'

class Rect(Shape):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        self.x1 = min(x1, x2)
        self.y1 = min(y1, y2)
        self.x2 = max(x1, x2)
        self.y2 = max(y1, y2)
    
    def to_html(self):
        return f'<rect x="{self.x1}" y="{self.y1}" width="{self.x2-self.x1}" height="{self.y2-self.y1}" fill="rgb({self.color[0]},{self.color[1]},{self.color[2]})" stroke="rgb({self.bordercolor[0]},{self.bordercolor[1]},{self.bordercolor[2]})" stroke-width="{self.borderwidth}"/>'

class Triangle(Shape):
    def __init__(self, x1, y1, x2, y2, x3, y3):
        super().__init__()
        self.points = [(x1, y1), (x2, y2), (x3, y3)]
    
    def to_html(self):
        points_str = " ".join([f"{p[0]},{p[1]}" for p in self.points])
        return f'<polygon points="{points_str}" fill="rgb({self.color[0]},{self.color[1]},{self.color[2]})" stroke="rgb({self.bordercolor[0]},{self.bordercolor[1]},{self.bordercolor[2]})" stroke-width="{self.borderwidth}"/>'

class TextBox(Shape):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        self.x1 = min(x1, x2)
        self.y1 = min(y1, y2)
        self.x2 = max(x1, x2)
        self.y2 = max(y1, y2)
        self.text = "click twice to input"
        self.font_name = "Arial"
        self.font_size = 16
    
    def to_html(self):
        return f'''<input type="text" 
                    style="position: absolute;
                           left: {self.x1}px;
                           top: {self.y1}px;
                           width: {self.x2-self.x1}px;
                           height: {self.y2-self.y1}px;
                           background: transparent;
                           border: 1px solid black;
                           font-family: '{self.font_name}';
                           font-size: {self.font_size}px;"
                    placeholder="{self.text}">'''

# ==================== 主应用 ====================
class PowerHTML:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PowerHTML 1.0 - 主菜单")
        self.root.geometry("400x300")
        
        self.data_folder = "data"
        self.current_project = None
        self.shapes = []
        self.drawing_mode = None
        self.temp_points = []
        
        # 确保 data 文件夹存在
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        
        self.create_main_menu()
    
    def create_main_menu(self):
        tk.Label(self.root, text="PowerHTML 1.0", font=("Arial", 20)).pack(pady=30)
        tk.Button(self.root, text="新建草稿", width=20, height=2, command=self.new_draft).pack(pady=10)
        tk.Button(self.root, text="打开我的草稿", width=20, height=2, command=self.open_draft).pack(pady=10)
        tk.Button(self.root, text="退出", width=20, height=2, command=self.root.quit).pack(pady=10)
    
    def new_draft(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("新建草稿")
        dialog.geometry("300x150")
        
        tk.Label(dialog, text="文件名（不需要加.html）:").pack(pady=10)
        entry = tk.Entry(dialog, width=30)
        entry.pack(pady=5)
        
        def on_confirm():
            name = entry.get().strip()
            if not name:
                messagebox.showerror("错误", "文件名不能为空")
                return
            
            project_path = os.path.join(self.data_folder, name)
            img_path = os.path.join(project_path, "img")
            html_path = os.path.join(project_path, f"{name}.html")
            temp_path = os.path.join(project_path, f"temp_{name}.html")
            
            if os.path.exists(project_path):
                messagebox.showerror("错误", "草稿已存在")
                return
            
            os.makedirs(img_path)
            
            default_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>我的页面</title>
    <style>
        body { margin: 0; min-height: 100vh; background: white; position: relative; }
        svg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }
    </style>
</head>
<body>
    <svg></svg>
</body>
</html>"""
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(default_html)
            shutil.copy(html_path, temp_path)
            
            self.current_project = project_path
            dialog.destroy()
            self.open_editor()
        
        tk.Button(dialog, text="确定", command=on_confirm).pack(side=tk.LEFT, padx=30, pady=20)
        tk.Button(dialog, text="取消", command=dialog.destroy).pack(side=tk.RIGHT, padx=30, pady=20)
    
    def open_draft(self):
        """打开草稿对话框"""
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)
        
        drafts = [d for d in os.listdir(self.data_folder) if os.path.isdir(os.path.join(self.data_folder, d))]
        
        dialog = tk.Toplevel(self.root)
        dialog.title("选择草稿")
        dialog.geometry("450x400")
        
        # 标题
        tk.Label(dialog, text="我的草稿", font=("Arial", 14)).pack(pady=10)
        
        # 列表框（带滚动条）
        listbox_frame = tk.Frame(dialog)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        if drafts:
            for d in drafts:
                listbox.insert(tk.END, d)
        else:
            listbox.insert(tk.END, "（暂无草稿）")
        
        # 按钮框架
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=20)
        
        def on_open():
            if not drafts:
                messagebox.showinfo("提示", "暂无草稿，请先新建")
                return
            
            sel = listbox.curselection()
            if sel:
                selected = listbox.get(sel)
                if selected != "（暂无草稿）":
                    self.current_project = os.path.join(self.data_folder, selected)
                    dialog.destroy()
                    self.open_editor()
            else:
                messagebox.showwarning("警告", "请先选择一个草稿")
        
        def on_cancel():
            dialog.destroy()
        
        def on_import():
            """从其他文件夹导入HTML文件作为草稿"""
            file_path = filedialog.askopenfilename(
                title="选择HTML文件",
                filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
            )
            
            if file_path:
                # 获取文件名（不含扩展名）
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                
                # 创建草稿文件夹
                project_path = os.path.join(self.data_folder, base_name)
                img_path = os.path.join(project_path, "img")
                html_path = os.path.join(project_path, f"{base_name}.html")
                temp_path = os.path.join(project_path, f"temp_{base_name}.html")
                
                # 检查是否已存在
                if os.path.exists(project_path):
                    result = messagebox.askyesno("确认", f"草稿 '{base_name}' 已存在，是否覆盖？")
                    if not result:
                        return
                    shutil.rmtree(project_path)
                
                # 创建新文件夹
                os.makedirs(img_path)
                
                # 复制导入的HTML文件
                shutil.copy(file_path, html_path)
                shutil.copy(file_path, temp_path)
                
                # 打开编辑器
                self.current_project = project_path
                dialog.destroy()
                self.open_editor()
                messagebox.showinfo("成功", f"已导入草稿: {base_name}")
        
        tk.Button(button_frame, text="打开", width=10, command=on_open).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="从其他文件夹导入", width=15, command=on_import).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="取消", width=10, command=on_cancel).pack(side=tk.LEFT, padx=5)
    
    def open_editor(self):
        self.root.withdraw()
        
        self.editor = tk.Toplevel()
        self.editor.title("PowerHTML 编辑器")
        self.editor.geometry("1024x768")
        self.editor.protocol("WM_DELETE_WINDOW", self.on_editor_close)
        
        # 工具栏
        toolbar = tk.Frame(self.editor, height=128, bg="lightblue")
        toolbar.pack(fill=tk.X)
        toolbar.pack_propagate(False)
        
        # 左侧功能按钮
        left_frame = tk.Frame(toolbar, bg="lightblue")
        left_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Button(left_frame, text="文本框", width=10, command=self.add_textbox_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(left_frame, text="矩形", width=10, command=self.add_rect_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(left_frame, text="圆形", width=10, command=self.add_circle_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(left_frame, text="三角形", width=10, command=self.add_triangle_dialog).pack(side=tk.LEFT, padx=5)
        
        # 右侧导出/退出
        right_frame = tk.Frame(toolbar, bg="lightblue")
        right_frame.pack(side=tk.RIGHT, padx=10)
        
        tk.Button(right_frame, text="导出", width=10, command=self.export_html).pack(side=tk.LEFT, padx=5)
        tk.Button(right_frame, text="退出", width=10, command=self.on_editor_close).pack(side=tk.LEFT, padx=5)
        
        # 画布区（HTML 浏览器）
        canvas_frame = tk.Frame(self.editor)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建 HTML 浏览器控件
        try:
            self.browser = HtmlFrame(canvas_frame)
            self.browser.pack(fill="both", expand=True)
            
            # 加载当前的 HTML 文件
            html_path = os.path.join(self.current_project, f"temp_{os.path.basename(self.current_project)}.html")
            if os.path.exists(html_path):
                self.browser.load_file(html_path)
        except Exception as e:
            # 如果 tkinterweb 不可用，显示错误信息
            label = tk.Label(canvas_frame, text=f"无法加载浏览器控件: {e}\n请运行: pip install tkinterweb", fg="red")
            label.pack(expand=True)
        
        # 加载现有图形
        self.shapes = []
    
    def save_to_html(self):
        """根据 self.shapes 生成完整 HTML 并刷新浏览器"""
        temp_path = os.path.join(self.current_project, f"temp_{os.path.basename(self.current_project)}.html")
        
        body_style = "margin: 0; min-height: 100vh; background: white; position: relative;"
        svg_elements = "\n        ".join([s.to_html() for s in self.shapes if not isinstance(s, TextBox)])
        text_elements = "\n        ".join([s.to_html() for s in self.shapes if isinstance(s, TextBox)])
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>PowerHTML 页面</title>
    <style>
        body {{ {body_style} }}
        svg {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }}
    </style>
</head>
<body>
    <svg>
        {svg_elements}
    </svg>
    {text_elements}
</body>
</html>"""
        
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # 刷新浏览器显示
        if hasattr(self, 'browser') and self.browser:
            try:
                self.browser.load_file(temp_path)
            except:
                pass
    
    def add_textbox_dialog(self):
        """弹出对话框添加文本框"""
        dialog = tk.Toplevel(self.editor)
        dialog.title("添加文本框")
        dialog.geometry("300x250")
        
        tk.Label(dialog, text="左上角 X:").pack(pady=5)
        x1_entry = tk.Entry(dialog)
        x1_entry.insert(0, "100")
        x1_entry.pack(pady=5)
        
        tk.Label(dialog, text="左上角 Y:").pack(pady=5)
        y1_entry = tk.Entry(dialog)
        y1_entry.insert(0, "100")
        y1_entry.pack(pady=5)
        
        tk.Label(dialog, text="右下角 X:").pack(pady=5)
        x2_entry = tk.Entry(dialog)
        x2_entry.insert(0, "300")
        x2_entry.pack(pady=5)
        
        tk.Label(dialog, text="右下角 Y:").pack(pady=5)
        y2_entry = tk.Entry(dialog)
        y2_entry.insert(0, "200")
        y2_entry.pack(pady=5)
        
        def on_confirm():
            try:
                x1 = int(x1_entry.get())
                y1 = int(y1_entry.get())
                x2 = int(x2_entry.get())
                y2 = int(y2_entry.get())
                
                textbox = TextBox(x1, y1, x2, y2)
                self.shapes.append(textbox)
                self.save_to_html()
                dialog.destroy()
                messagebox.showinfo("成功", "文本框已添加")
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字")
        
        tk.Button(dialog, text="确定", command=on_confirm).pack(pady=10)
    
    def add_rect_dialog(self):
        """弹出对话框添加矩形"""
        dialog = tk.Toplevel(self.editor)
        dialog.title("添加矩形")
        dialog.geometry("300x250")
        
        tk.Label(dialog, text="左上角 X:").pack(pady=5)
        x1_entry = tk.Entry(dialog)
        x1_entry.insert(0, "100")
        x1_entry.pack(pady=5)
        
        tk.Label(dialog, text="左上角 Y:").pack(pady=5)
        y1_entry = tk.Entry(dialog)
        y1_entry.insert(0, "100")
        y1_entry.pack(pady=5)
        
        tk.Label(dialog, text="右下角 X:").pack(pady=5)
        x2_entry = tk.Entry(dialog)
        x2_entry.insert(0, "300")
        x2_entry.pack(pady=5)
        
        tk.Label(dialog, text="右下角 Y:").pack(pady=5)
        y2_entry = tk.Entry(dialog)
        y2_entry.insert(0, "200")
        y2_entry.pack(pady=5)
        
        def on_confirm():
            try:
                x1 = int(x1_entry.get())
                y1 = int(y1_entry.get())
                x2 = int(x2_entry.get())
                y2 = int(y2_entry.get())
                
                rect = Rect(x1, y1, x2, y2)
                self.shapes.append(rect)
                self.save_to_html()
                dialog.destroy()
                messagebox.showinfo("成功", "矩形已添加")
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字")
        
        tk.Button(dialog, text="确定", command=on_confirm).pack(pady=10)
    
    def add_circle_dialog(self):
        """弹出对话框添加圆形"""
        dialog = tk.Toplevel(self.editor)
        dialog.title("添加圆形")
        dialog.geometry("300x200")
        
        tk.Label(dialog, text="圆心 X:").pack(pady=5)
        cx_entry = tk.Entry(dialog)
        cx_entry.insert(0, "200")
        cx_entry.pack(pady=5)
        
        tk.Label(dialog, text="圆心 Y:").pack(pady=5)
        cy_entry = tk.Entry(dialog)
        cy_entry.insert(0, "200")
        cy_entry.pack(pady=5)
        
        tk.Label(dialog, text="半径:").pack(pady=5)
        r_entry = tk.Entry(dialog)
        r_entry.insert(0, "50")
        r_entry.pack(pady=5)
        
        def on_confirm():
            try:
                cx = int(cx_entry.get())
                cy = int(cy_entry.get())
                r = int(r_entry.get())
                
                circle = Circle(cx, cy, r)
                self.shapes.append(circle)
                self.save_to_html()
                dialog.destroy()
                messagebox.showinfo("成功", "圆形已添加")
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字")
        
        tk.Button(dialog, text="确定", command=on_confirm).pack(pady=10)
    
    def add_triangle_dialog(self):
        """弹出对话框添加三角形"""
        dialog = tk.Toplevel(self.editor)
        dialog.title("添加三角形")
        dialog.geometry("300x350")
        
        tk.Label(dialog, text="顶点1 X:").pack(pady=2)
        x1_entry = tk.Entry(dialog)
        x1_entry.insert(0, "200")
        x1_entry.pack(pady=2)
        
        tk.Label(dialog, text="顶点1 Y:").pack(pady=2)
        y1_entry = tk.Entry(dialog)
        y1_entry.insert(0, "100")
        y1_entry.pack(pady=2)
        
        tk.Label(dialog, text="顶点2 X:").pack(pady=2)
        x2_entry = tk.Entry(dialog)
        x2_entry.insert(0, "100")
        x2_entry.pack(pady=2)
        
        tk.Label(dialog, text="顶点2 Y:").pack(pady=2)
        y2_entry = tk.Entry(dialog)
        y2_entry.insert(0, "300")
        y2_entry.pack(pady=2)
        
        tk.Label(dialog, text="顶点3 X:").pack(pady=2)
        x3_entry = tk.Entry(dialog)
        x3_entry.insert(0, "300")
        x3_entry.pack(pady=2)
        
        tk.Label(dialog, text="顶点3 Y:").pack(pady=2)
        y3_entry = tk.Entry(dialog)
        y3_entry.insert(0, "300")
        y3_entry.pack(pady=2)
        
        def on_confirm():
            try:
                x1 = int(x1_entry.get())
                y1 = int(y1_entry.get())
                x2 = int(x2_entry.get())
                y2 = int(y2_entry.get())
                x3 = int(x3_entry.get())
                y3 = int(y3_entry.get())
                
                triangle = Triangle(x1, y1, x2, y2, x3, y3)
                self.shapes.append(triangle)
                self.save_to_html()
                dialog.destroy()
                messagebox.showinfo("成功", "三角形已添加")
            except ValueError:
                messagebox.showerror("错误", "请输入有效的数字")
        
        tk.Button(dialog, text="确定", command=on_confirm).pack(pady=10)
    
    def export_html(self):
        temp_path = os.path.join(self.current_project, f"temp_{os.path.basename(self.current_project)}.html")
        final_path = os.path.join(self.current_project, f"{os.path.basename(self.current_project)}.html")
        
        # 显示确认窗口
        confirm = tk.Toplevel(self.editor)
        confirm.title("确认导出")
        confirm.geometry("600x400")
        
        tk.Label(confirm, text="是否保存以下代码？", font=("Arial", 12)).pack(pady=10)
        text_preview = tk.Text(confirm)
        text_preview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        with open(temp_path, 'r', encoding='utf-8') as f:
            content = f.read()
            text_preview.insert(tk.END, content)
        
        def on_yes():
            shutil.copy(temp_path, final_path)
            confirm.destroy()
            self.editor.destroy()
            self.root.deiconify()
            messagebox.showinfo("成功", "已保存并返回主菜单")
        
        def on_no():
            confirm.destroy()
        
        tk.Button(confirm, text="是", width=10, command=on_yes).pack(side=tk.LEFT, padx=50, pady=20)
        tk.Button(confirm, text="否", width=10, command=on_no).pack(side=tk.RIGHT, padx=50, pady=20)
    
    def on_editor_close(self):
        temp_path = os.path.join(self.current_project, f"temp_{os.path.basename(self.current_project)}.html")
        if messagebox.askyesno("退出", "你要保存文件再退出吗？"):
            final_path = os.path.join(self.current_project, f"{os.path.basename(self.current_project)}.html")
            shutil.copy(temp_path, final_path)
        else:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        self.editor.destroy()
        self.root.deiconify()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PowerHTML()
    app.run()