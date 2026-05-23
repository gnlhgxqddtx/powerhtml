import tkinter as tk
from tkinter import messagebox
import math
import json
import os
import shutil
from shapes import Rect, Circle, Triangle, TextBox
from core import ProjectManager

class EditorWindow:
    def __init__(self, project_path, on_close_callback):
        self.project_path = project_path
        self.on_close_callback = on_close_callback
        self.shapes = []
        self.drawing_mode = None
        self.drawing_points = []
        self.start_x = None
        self.start_y = None
        self.selected_shape = None
        self.is_moving = False  # 是否正在移动
        self.drag_start_x = None
        self.drag_start_y = None
        self.project_manager = ProjectManager()
        self.project_manager.current_project = project_path
        self.editing_textbox = None  # 正在编辑的文本框
        self.text_entry = None
        
        self.create_window()
        self.load_shapes_from_temp()
        self.refresh_canvas()
    
    def load_shapes_from_temp(self):
        """从 temp_shapes.json 加载图形"""
        shapes_data = self.project_manager.load_shapes_from_temp()
        self.shapes = []
        
        for data in shapes_data:
            if data["type"] == "rect":
                shape = Rect(data["x1"], data["y1"], data["x2"], data["y2"])
                shape.color = data["color"]
                shape.bordercolor = data["bordercolor"]
                shape.borderwidth = data["borderwidth"]
                self.shapes.append(shape)
                
            elif data["type"] == "circle":
                shape = Circle(data["cx"], data["cy"], data["r"])
                shape.color = data["color"]
                shape.bordercolor = data["bordercolor"]
                shape.borderwidth = data["borderwidth"]
                self.shapes.append(shape)
                
            elif data["type"] == "triangle":
                shape = Triangle(data["points"])
                shape.color = data["color"]
                shape.bordercolor = data["bordercolor"]
                shape.borderwidth = data["borderwidth"]
                self.shapes.append(shape)
                
            elif data["type"] == "textbox":
                shape = TextBox(data["x1"], data["y1"], data["x2"], data["y2"])
                shape.text = data.get("text", "请输入文本")
                shape.font_name = data.get("font_name", "微软雅黑")
                shape.font_size = data.get("font_size", 16)
                shape.font_color = data.get("font_color", [0, 0, 0])
                shape.color = data["color"]
                shape.bordercolor = data["bordercolor"]
                shape.borderwidth = data["borderwidth"]
                self.shapes.append(shape)
        
        print(f"从 temp_shapes.json 加载了 {len(self.shapes)} 个图形")
    
    def save_shapes_to_temp(self):
        """保存图形到 temp_shapes.json 并更新 temp.html"""
        shapes_data = []
        for shape in self.shapes:
            if isinstance(shape, Rect):
                shapes_data.append({
                    "type": "rect",
                    "x1": shape.x1, "y1": shape.y1,
                    "x2": shape.x2, "y2": shape.y2,
                    "color": shape.color,
                    "bordercolor": shape.bordercolor,
                    "borderwidth": shape.borderwidth
                })
            elif isinstance(shape, Circle):
                shapes_data.append({
                    "type": "circle",
                    "cx": shape.cx, "cy": shape.cy, "r": shape.r,
                    "color": shape.color,
                    "bordercolor": shape.bordercolor,
                    "borderwidth": shape.borderwidth
                })
            elif isinstance(shape, Triangle):
                shapes_data.append({
                    "type": "triangle",
                    "points": shape.points,
                    "color": shape.color,
                    "bordercolor": shape.bordercolor,
                    "borderwidth": shape.borderwidth
                })
            elif isinstance(shape, TextBox):
                shapes_data.append({
                    "type": "textbox",
                    "x1": shape.x1, "y1": shape.y1,
                    "x2": shape.x2, "y2": shape.y2,
                    "text": shape.text,
                    "font_name": shape.font_name,
                    "font_size": shape.font_size,
                    "font_color": shape.font_color,
                    "color": shape.color,
                    "bordercolor": shape.bordercolor,
                    "borderwidth": shape.borderwidth
                })
        
        # 保存到 temp_shapes.json
        self.project_manager.save_shapes_to_temp(shapes_data)
        
        # 生成并保存到 temp.html
        html_content = self.generate_html()
        self.project_manager.generate_html_to_temp(html_content)
        
        print(f"保存了 {len(self.shapes)} 个图形到 temp 文件")
    
    def generate_html(self):
        """生成 HTML 内容"""
        body_elements = "\n    ".join([s.to_html() for s in self.shapes])
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>PowerHTML 页面</title>
    <style>
        body {{
            margin: 0;
            min-height: 100vh;
            background: white;
            position: relative;
        }}
        * {{
            user-select: none;
        }}
    </style>
</head>
<body>
    {body_elements}
</body>
</html>"""
    
    def create_window(self):
        self.window = tk.Toplevel()
        self.window.title("PowerHTML 编辑器")
        self.window.geometry("1280x800")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # 工具栏
        toolbar = tk.Frame(self.window, height=100, bg="#2c3e50")
        toolbar.pack(fill=tk.X)
        toolbar.pack_propagate(False)
        
        left_frame = tk.Frame(toolbar, bg="#2c3e50")
        left_frame.pack(side=tk.LEFT, padx=20, pady=10)
        
        btn_style = {"width": 12, "height": 2, "font": ("微软雅黑", 10), "bg": "#3498db", "fg": "white"}
        
        tk.Button(left_frame, text="📝 文本框", command=lambda: self.enable_mode("textbox"), **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(left_frame, text="⬛ 矩形", command=lambda: self.enable_mode("rect"), **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(left_frame, text="● 圆形", command=lambda: self.enable_mode("circle"), **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(left_frame, text="▲ 三角形", command=lambda: self.enable_mode("triangle"), **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(left_frame, text="🗑 删除", command=self.delete_selected_shape, **btn_style).pack(side=tk.LEFT, padx=5)
        
        right_frame = tk.Frame(toolbar, bg="#2c3e50")
        right_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        tk.Button(right_frame, text="💾 导出", command=self.export, **btn_style).pack(side=tk.LEFT, padx=5)
        tk.Button(right_frame, text="❌ 退出", command=self.on_close, **btn_style).pack(side=tk.LEFT, padx=5)
        
        # 状态栏
        self.status_label = tk.Label(
            self.window, 
            text="就绪 | 提示: 单击选中图形，按住拖拽移动，按 Delete 删除", 
            bg="#ecf0f1", 
            anchor="w", 
            font=("微软雅黑", 10)
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 画布
        canvas_frame = tk.Frame(self.window)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="white", cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 绑定事件
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.canvas.bind("<Button-3>", self.cancel_drawing)
        self.canvas.bind("<Delete>", self.delete_selected_shape)
        self.window.bind("<Delete>", self.delete_selected_shape)
    
    def refresh_canvas(self):
        """刷新画布显示"""
        self.canvas.delete("all")
        
        for shape in self.shapes:
            fill_color = f"#{shape.color[0]:02x}{shape.color[1]:02x}{shape.color[2]:02x}"
            outline_color = f"#{shape.bordercolor[0]:02x}{shape.bordercolor[1]:02x}{shape.bordercolor[2]:02x}"
            
            if isinstance(shape, Rect):
                self.canvas.create_rectangle(
                    shape.x1, shape.y1, shape.x2, shape.y2,
                    outline=outline_color, width=shape.borderwidth, fill=fill_color
                )
            elif isinstance(shape, Circle):
                self.canvas.create_oval(
                    shape.cx - shape.r, shape.cy - shape.r,
                    shape.cx + shape.r, shape.cy + shape.r,
                    outline=outline_color, width=shape.borderwidth, fill=fill_color
                )
            elif isinstance(shape, Triangle):
                self.canvas.create_polygon(
                    shape.points, outline=outline_color,
                    width=shape.borderwidth, fill=fill_color
                )
            elif isinstance(shape, TextBox):
                self.canvas.create_rectangle(
                    shape.x1, shape.y1, shape.x2, shape.y2,
                    outline=outline_color, width=shape.borderwidth, fill="#f0f0f0"
                )
                self.canvas.create_text(
                    (shape.x1 + shape.x2) / 2, (shape.y1 + shape.y2) / 2,
                    text=shape.text, font=(shape.font_name, shape.font_size), fill="black"
                )
            
            if self.selected_shape == shape:
                self.draw_handles(shape)
    
    def draw_handles(self, shape):
        """绘制关键点"""
        if isinstance(shape, Rect):
            points = [
                (shape.x1, shape.y1), (shape.x2, shape.y1),
                (shape.x2, shape.y2), (shape.x1, shape.y2)
            ]
            for x, y in points:
                self.canvas.create_oval(x-4, y-4, x+4, y+4, fill="blue", outline="white", width=2)
        elif isinstance(shape, Circle):
            self.canvas.create_oval(shape.cx-5, shape.cy-5, shape.cx+5, shape.cy+5, fill="blue", outline="white", width=2)
        elif isinstance(shape, Triangle):
            for x, y in shape.points:
                self.canvas.create_oval(x-4, y-4, x+4, y+4, fill="blue", outline="white", width=2)
        elif isinstance(shape, TextBox):
            points = [
                (shape.x1, shape.y1), (shape.x2, shape.y1),
                (shape.x2, shape.y2), (shape.x1, shape.y2)
            ]
            for x, y in points:
                self.canvas.create_oval(x-4, y-4, x+4, y+4, fill="blue", outline="white", width=2)
    
    def find_shape_at(self, x, y):
        for shape in reversed(self.shapes):
            if shape.contains(x, y):
                return shape
        return None
    
    def enable_mode(self, mode):
        self.drawing_mode = mode
        self.drawing_points = []
        mode_names = {"rect": "矩形", "circle": "圆形", "triangle": "三角形", "textbox": "文本框"}
        self.status_label.config(text=f"{mode_names[mode]}模式：拖动鼠标或点击确定位置")
    
    def on_mouse_down(self, event):
        x, y = event.x, event.y
        
        # 如果正在编辑文本框，先保存编辑内容
        if self.editing_textbox:
            self.finish_text_editing()
            return
        # ↑↑↑ 添加上面几行
        
        # 检查是否点击到图形
        shape = self.find_shape_at(x, y)
        
        if shape:
            # 在这里添加双击检测 ↓↓↓
            # 如果是文本框，检测双击
            if isinstance(shape, TextBox):
                import time
                if hasattr(self, '_last_click_time'):
                    current_time = time.time()
                    if current_time - self._last_click_time < 0.3:
                        # 双击：进入文字编辑模式
                        self.start_text_editing(shape)
                        self._last_click_time = None
                        return
                self._last_click_time = time.time()
            # ↑↑↑ 添加上面这些
            
            # 点击到图形
            if self.selected_shape == shape:
                # ... 原有代码
                # 已经是选中的图形，开始移动
                self.is_moving = True
                self.drag_start_x = x
                self.drag_start_y = y
                self.status_label.config(text=f"移动中: {type(shape).__name__}")
            else:
                # 选中新图形
                self.selected_shape = shape
                self.status_label.config(text=f"已选中: {type(shape).__name__}")
                self.refresh_canvas()
            return
        
        # 没有点击到图形，取消选中
        self.selected_shape = None
        self.refresh_canvas()
        
        # 处理绘制模式
        if self.drawing_mode:
            if self.drawing_mode == "triangle":
                self.drawing_points.append((x, y))
                self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="red")
                self.status_label.config(text=f"三角形: 已选择 {len(self.drawing_points)}/3 个点")
                if len(self.drawing_points) == 3:
                    triangle = Triangle(self.drawing_points.copy())
                    self.shapes.append(triangle)
                    self.save_shapes_to_temp()
                    self.refresh_canvas()
                    self.drawing_mode = None
                    self.drawing_points = []
                    self.status_label.config(text="三角形已添加")
            else:
                # 矩形、圆形、文本框：开始绘制
                self.start_x = x
                self.start_y = y
                self.drawing_points = [(x, y)]
                self.temp_rect = self.canvas.create_rectangle(x, y, x, y, outline="red", dash=(4,2))
        else:
            self.status_label.config(text="就绪")
    
    def on_mouse_drag(self, event):
        # 移动模式：拖拽移动选中的图形
        if self.is_moving and self.selected_shape:
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y
            self.selected_shape.move(dx, dy)
            self.drag_start_x = event.x
            self.drag_start_y = event.y
            self.refresh_canvas()
            return
        
        # 绘制模式：显示临时矩形
        if self.drawing_mode and self.drawing_mode != "triangle" and self.start_x is not None:
            self.canvas.coords(self.temp_rect, self.start_x, self.start_y, event.x, event.y)
    
    def on_mouse_up(self, event):
        # 结束移动模式
        if self.is_moving and self.selected_shape:
            self.is_moving = False
            self.save_shapes_to_temp()
            self.status_label.config(text=f"移动完成，已保存")
            return
        
        # 绘制模式：完成绘制
        if self.drawing_mode and self.drawing_mode != "triangle" and self.start_x is not None:
            x2, y2 = event.x, event.y
            x1, y1 = self.start_x, self.start_y
            
            # 处理两次点击模式
            if x1 == x2 and y1 == y2 and len(self.drawing_points) == 1:
                self.drawing_points.append((x2, y2))
                self.start_x = None
                return
            elif len(self.drawing_points) == 1 and x1 == x2 and y1 == y2:
                return
            
            if len(self.drawing_points) == 2:
                x1, y1 = self.drawing_points[0]
            
            shape = None
            if self.drawing_mode == "rect":
                shape = Rect(x1, y1, x2, y2)
            elif self.drawing_mode == "circle":
                r = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                shape = Circle(x1, y1, r)
            elif self.drawing_mode == "textbox":
                shape = TextBox(x1, y1, x2, y2)
            
            if shape:
                self.shapes.append(shape)
                self.save_shapes_to_temp()
                self.refresh_canvas()
                self.status_label.config(text=f"{self.drawing_mode}已添加")
            
            # 清理绘制状态
            self.drawing_mode = None
            self.start_x = None
            self.drawing_points = []
            if hasattr(self, 'temp_rect'):
                self.canvas.delete(self.temp_rect)
    
    def cancel_drawing(self, event):
        self.drawing_mode = None
        self.start_x = None
        self.drawing_points = []
        if hasattr(self, 'temp_rect'):
            self.canvas.delete(self.temp_rect)
        self.status_label.config(text="已取消")
    
    def delete_selected_shape(self, event=None):
        """删除选中的图形"""
        if self.selected_shape:
            self.shapes.remove(self.selected_shape)
            self.save_shapes_to_temp()
            self.selected_shape = None
            self.refresh_canvas()
            self.status_label.config(text="已删除图形")
            print(f"已删除图形，当前还有 {len(self.shapes)} 个图形")
        else:
            self.status_label.config(text="没有选中的图形，请先点击选中一个图形")
    
    def start_text_editing(self, textbox):
        """开始编辑文本框文字"""
        if self.editing_textbox:
            self.finish_text_editing()
        
        self.editing_textbox = textbox
        
        width = textbox.x2 - textbox.x1
        height = textbox.y2 - textbox.y1
        
        self.text_entry = tk.Entry(
            self.canvas,
            font=(textbox.font_name, textbox.font_size),
            bg="white",
            fg="black",
            relief="solid",
            borderwidth=1
        )
        
        self.text_entry.place(x=textbox.x1, y=textbox.y1, width=width, height=height)
        self.text_entry.insert(0, textbox.text)
        self.text_entry.select_range(0, tk.END)
        self.text_entry.focus()
        
        self.text_entry.bind("<Return>", lambda e: self.finish_text_editing())
        self.text_entry.bind("<FocusOut>", lambda e: self.finish_text_editing())
        self.text_entry.bind("<Escape>", lambda e: self.cancel_text_editing())
        
        self.status_label.config(text="编辑文字中: 输入后按回车确认")

    def finish_text_editing(self):
        """完成文字编辑，保存修改"""
        if self.editing_textbox and self.text_entry:
            new_text = self.text_entry.get()
            if new_text.strip():
                self.editing_textbox.text = new_text
            
            self.text_entry.destroy()
            self.text_entry = None
            self.save_shapes_to_temp()
            self.refresh_canvas()
            self.editing_textbox = None
            self.status_label.config(text="文字已更新")

    def cancel_text_editing(self):
        """取消文字编辑，不保存"""
        if self.text_entry:
            self.text_entry.destroy()
            self.text_entry = None
        self.editing_textbox = None
        self.status_label.config(text="已取消文字编辑")
    def export(self):
        """导出功能：保存并退出"""
        self.save_shapes_to_temp()
        html_content = self.generate_html()
        
        from ui.dialogs import ExportConfirmDialog
        
        def on_yes():
            self.project_manager.save_changes()
            messagebox.showinfo("成功", "已保存草稿")
            self.window.destroy()
            if self.on_close_callback:
                self.on_close_callback()
        
        def on_no():
            self.project_manager.discard_changes()
            self.window.destroy()
            if self.on_close_callback:
                self.on_close_callback()
        
        ExportConfirmDialog(self.window, html_content, on_yes, on_no)
    
    def on_close(self):
        """关闭编辑器"""
        result = messagebox.askyesno("退出", "你要保存文件再退出吗？")
        
        if result:
            print("用户选择保存")
            self.save_shapes_to_temp()
            self.project_manager.save_changes()
            messagebox.showinfo("成功", "已保存草稿")
        else:
            print("用户选择不保存，删除临时文件")
            self.project_manager.discard_changes()
        
        self.window.destroy()
        if self.on_close_callback:
            self.on_close_callback()