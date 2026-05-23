import os
import shutil
import json
from tkinter import messagebox, filedialog

class ProjectManager:
    def __init__(self, data_folder="data"):
        self.data_folder = data_folder
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
        self.current_project = None
    
    def new_draft(self, name, open_callback):
        """新建草稿"""
        project_path = os.path.join(self.data_folder, name)
        img_path = os.path.join(project_path, "img")
        html_path = os.path.join(project_path, f"{name}.html")
        temp_html_path = os.path.join(project_path, f"temp_{name}.html")
        shapes_path = os.path.join(project_path, "shapes.json")
        temp_shapes_path = os.path.join(project_path, f"temp_shapes.json")
        
        if os.path.exists(project_path):
            messagebox.showerror("错误", "草稿已存在")
            return False
        
        os.makedirs(img_path)
        
        default_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>我的页面</title>
    <style>
        body { margin: 0; min-height: 100vh; background: #f0f0f0; position: relative; }
        * { user-select: none; }
    </style>
</head>
<body>
</body>
</html>"""
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(default_html)
        shutil.copy(html_path, temp_html_path)
        
        # 初始化空的 shapes.json 和 temp_shapes.json
        with open(shapes_path, 'w', encoding='utf-8') as f:
            json.dump([], f)
        shutil.copy(shapes_path, temp_shapes_path)
        
        self.current_project = project_path
        open_callback()
        return True
    
    def get_drafts(self):
        """获取所有草稿"""
        if not os.path.exists(self.data_folder):
            return []
        return [d for d in os.listdir(self.data_folder) 
                if os.path.isdir(os.path.join(self.data_folder, d))]
    
    def open_draft(self, name, open_callback):
        """打开草稿 - 创建临时文件"""
        project_path = os.path.join(self.data_folder, name)
        if not os.path.exists(project_path):
            return False
        
        self.current_project = project_path
        
        # 确保临时文件存在（从原始文件复制）
        html_path = self.get_html_path()
        temp_html_path = self.get_temp_html_path()
        shapes_path = self.get_shapes_path()
        temp_shapes_path = self.get_temp_shapes_path()
        
        if os.path.exists(html_path) and not os.path.exists(temp_html_path):
            shutil.copy(html_path, temp_html_path)
        
        if os.path.exists(shapes_path) and not os.path.exists(temp_shapes_path):
            shutil.copy(shapes_path, temp_shapes_path)
        elif not os.path.exists(shapes_path):
            # 如果 shapes.json 不存在，创建空的
            with open(shapes_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
            shutil.copy(shapes_path, temp_shapes_path)
        
        open_callback()
        return True
    
    def import_from_file(self, open_callback):
        """从文件导入"""
        file_path = filedialog.askopenfilename(
            title="选择HTML文件",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        
        if file_path:
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            project_path = os.path.join(self.data_folder, base_name)
            img_path = os.path.join(project_path, "img")
            html_path = os.path.join(project_path, f"{base_name}.html")
            temp_html_path = os.path.join(project_path, f"temp_{base_name}.html")
            shapes_path = os.path.join(project_path, "shapes.json")
            temp_shapes_path = os.path.join(project_path, f"temp_shapes.json")
            
            if os.path.exists(project_path):
                result = messagebox.askyesno("确认", f"草稿 '{base_name}' 已存在，是否覆盖？")
                if not result:
                    return False
                shutil.rmtree(project_path)
            
            os.makedirs(img_path)
            shutil.copy(file_path, html_path)
            shutil.copy(file_path, temp_html_path)
            
            # 创建空的 shapes.json
            with open(shapes_path, 'w', encoding='utf-8') as f:
                json.dump([], f)
            shutil.copy(shapes_path, temp_shapes_path)
            
            self.current_project = project_path
            open_callback()
            return True
        return False
    
    def load_shapes_from_temp(self):
        """从 temp_shapes.json 加载图形数据"""
        temp_shapes_path = self.get_temp_shapes_path()
        if os.path.exists(temp_shapes_path):
            with open(temp_shapes_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_shapes_to_temp(self, shapes_data):
        """保存图形数据到 temp_shapes.json 和 temp.html"""
        temp_shapes_path = self.get_temp_shapes_path()
        with open(temp_shapes_path, 'w', encoding='utf-8') as f:
            json.dump(shapes_data, f, indent=2)
    
    def generate_html_to_temp(self, html_content):
        """保存 HTML 到 temp.html"""
        temp_html_path = self.get_temp_html_path()
        with open(temp_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def save_changes(self):
        """保存修改：将临时文件复制到原始文件"""
        temp_html_path = self.get_temp_html_path()
        html_path = self.get_html_path()
        temp_shapes_path = self.get_temp_shapes_path()
        shapes_path = self.get_shapes_path()
        
        # 复制 HTML
        if os.path.exists(temp_html_path):
            shutil.copy(temp_html_path, html_path)
        
        # 复制 shapes.json
        if os.path.exists(temp_shapes_path):
            shutil.copy(temp_shapes_path, shapes_path)
        
        # 删除临时文件
        self.cleanup_temp_files()
        
        return True
    
    def discard_changes(self):
        """放弃修改：直接删除临时文件"""
        self.cleanup_temp_files()
        return True
    
    def cleanup_temp_files(self):
        """删除所有临时文件"""
        temp_html_path = self.get_temp_html_path()
        temp_shapes_path = self.get_temp_shapes_path()
        
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)
        if os.path.exists(temp_shapes_path):
            os.remove(temp_shapes_path)
    
    def get_html_path(self):
        return os.path.join(self.current_project, f"{os.path.basename(self.current_project)}.html")
    
    def get_temp_html_path(self):
        return os.path.join(self.current_project, f"temp_{os.path.basename(self.current_project)}.html")
    
    def get_shapes_path(self):
        return os.path.join(self.current_project, "shapes.json")
    
    def get_temp_shapes_path(self):
        return os.path.join(self.current_project, "temp_shapes.json")
    
    def get_html_content(self):
        """获取 temp.html 的内容"""
        temp_html_path = self.get_temp_html_path()
        if os.path.exists(temp_html_path):
            with open(temp_html_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""