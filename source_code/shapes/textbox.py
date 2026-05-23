from .shape import Shape

class TextBox(Shape):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        self.x1 = min(x1, x2)
        self.y1 = min(y1, y2)
        self.x2 = max(x1, x2)
        self.y2 = max(y1, y2)
        self.text = "请输入文本"
        self.font_name = "微软雅黑"
        self.font_size = 16
        self.font_color = [0, 0, 0]
        self.color = [255, 255, 255]
    
    def to_html(self):
        width = self.x2 - self.x1
        height = self.y2 - self.y1
        return f'''<input type="text" 
                    value="{self.text}"
                    style="position: absolute;
                           left: {self.x1}px;
                           top: {self.y1}px;
                           width: {width}px;
                           height: {height}px;
                           background: rgba({self.color[0]},{self.color[1]},{self.color[2]},0.5);
                           border: {self.borderwidth}px solid rgb({self.bordercolor[0]},{self.bordercolor[1]},{self.bordercolor[2]});
                           font-family: '{self.font_name}';
                           font-size: {self.font_size}px;
                           color: rgb({self.font_color[0]},{self.font_color[1]},{self.font_color[2]});
                           padding: 5px;
                           box-sizing: border-box;"
                    data-type="textbox"
                    data-id="{id(self)}">'''
    
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