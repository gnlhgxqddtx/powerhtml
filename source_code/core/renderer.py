import tkinter as tk
from shapes import Rect, Circle, Triangle, TextBox

class CanvasRenderer:
    def __init__(self, canvas, status_label):
        self.canvas = canvas
        self.status_label = status_label
        self.shapes = []
        self.selected_shape = None
        self.editing_mode = None
        self.drag_start_x = None
        self.drag_start_y = None
    
    def refresh(self):
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
    
    def select_shape(self, shape):
        self.selected_shape = shape
        if shape:
            self.status_label.config(text=f"已选中: {type(shape).__name__}")
        else:
            self.status_label.config(text="就绪")
        self.refresh()