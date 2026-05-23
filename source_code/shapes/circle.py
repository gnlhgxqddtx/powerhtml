import math
from .shape import Shape

class Circle(Shape):
    def __init__(self, cx, cy, r):
        super().__init__()
        self.cx = cx
        self.cy = cy
        self.r = r
    
    def to_html(self):
        return f'<svg style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;"><circle cx="{self.cx}" cy="{self.cy}" r="{self.r}" fill="rgb({self.color[0]},{self.color[1]},{self.color[2]})" stroke="rgb({self.bordercolor[0]},{self.bordercolor[1]},{self.bordercolor[2]})" stroke-width="{self.borderwidth}" data-type="circle" data-id="{id(self)}"/></svg>'
    
    def contains(self, x, y):
        return math.sqrt((x - self.cx)**2 + (y - self.cy)**2) <= self.r
    
    def move(self, dx, dy):
        self.cx += dx
        self.cy += dy
    
    def resize(self, x, y, start_x, start_y):
        self.r = math.sqrt((x - self.cx)**2 + (y - self.cy)**2)