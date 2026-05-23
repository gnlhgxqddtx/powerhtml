from .shape import Shape

class Triangle(Shape):
    def __init__(self, points):
        super().__init__()
        self.points = points
    
    def to_html(self):
        points_str = " ".join([f"{p[0]},{p[1]}" for p in self.points])
        return f'<svg style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;"><polygon points="{points_str}" fill="rgb({self.color[0]},{self.color[1]},{self.color[2]})" stroke="rgb({self.bordercolor[0]},{self.bordercolor[1]},{self.bordercolor[2]})" stroke-width="{self.borderwidth}" data-type="triangle" data-id="{id(self)}"/></svg>'
    
    def contains(self, x, y):
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        
        b1 = sign((x, y), self.points[0], self.points[1]) < 0.0
        b2 = sign((x, y), self.points[1], self.points[2]) < 0.0
        b3 = sign((x, y), self.points[2], self.points[0]) < 0.0
        return (b1 == b2) and (b2 == b3)
    
    def move(self, dx, dy):
        self.points = [(p[0] + dx, p[1] + dy) for p in self.points]