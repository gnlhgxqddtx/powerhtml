import math

def rgb_to_hex(rgb):
    """将RGB列表转换为十六进制颜色"""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def hex_to_rgb(hex_color):
    """将十六进制颜色转换为RGB列表"""
    hex_color = hex_color.lstrip('#')
    return [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

def distance(x1, y1, x2, y2):
    """计算两点之间的距离"""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def point_in_rect(x, y, x1, y1, x2, y2):
    """检查点是否在矩形内"""
    return x1 <= x <= x2 and y1 <= y <= y2

def point_in_circle(x, y, cx, cy, r):
    """检查点是否在圆形内"""
    return distance(x, y, cx, cy) <= r

def point_in_triangle(x, y, p1, p2, p3):
    """检查点是否在三角形内（重心坐标法）"""
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    
    b1 = sign((x, y), p1, p2) < 0.0
    b2 = sign((x, y), p2, p3) < 0.0
    b3 = sign((x, y), p3, p1) < 0.0
    return (b1 == b2) and (b2 == b3)

def normalize_rect(x1, y1, x2, y2):
    """标准化矩形坐标（确保x1<=x2, y1<=y2）"""
    return (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))