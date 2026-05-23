class Shape:
    """所有图形的基类"""
    def __init__(self):
        self.color = [0, 0, 255]  # 默认蓝色
        self.borderwidth = 2
        self.bordercolor = [0, 0, 0]
        self.text = ""
    
    def to_html(self):
        """生成HTML代码"""
        pass
    
    def contains(self, x, y):
        """检查点是否在图形内"""
        return False
    
    def move(self, dx, dy):
        """移动图形"""
        pass
    
    def resize(self, x, y, start_x, start_y):
        """调整大小"""
        pass