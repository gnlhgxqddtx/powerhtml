from .shape import Shape

class Rect(Shape):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        self.x1 = min(x1, x2)
        self.y1 = min(y1, y2)
        self.x2 = max(x1, x2)
        self.y2 = max(y1, y2)
    
    def to_html(self):
        width = self.x2 - self.x1
        height = self.y2 - self.y1
        return f'<div style="position: absolute; left: {self.x1}px; top: {self.y1}px; width: {width}px; height: {height}px; background: rgb({self.color[0]},{self.color[1]},{self.color[2]}); border: {self.borderwidth}px solid rgb({self.bordercolor[0]},{self.bordercolor[1]},{self.bordercolor[2]});" data-type="rect" data-id="{id(self)}"></div>'
    
    def contains(self, x, y):
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2
    
    def move(self, dx, dy):
        self.x1 += dx
        self.x2 += dx
        self.y1 += dy
        self.y2 += dy
    
    def resize(self, x, y, start_x, start_y):
        new_x1, new_y1 = start_x, start_y
        new_x2, new_y2 = x, y
        self.x1 = min(new_x1, new_x2)
        self.y1 = min(new_y1, new_y2)
        self.x2 = max(new_x1, new_x2)
        self.y2 = max(new_y1, new_y2)