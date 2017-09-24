from math import cos, sin


def pairs(lst):
    i = iter(lst)
    item = next(i)
    first = item
    prev = item
    for item in i:
        yield prev, item
        prev = item
    yield item, first


def centroid(points):
    center_x = 0.0
    center_y = 0.0
    for x, y in points:
        center_x += x
        center_y += y
    center_y /= len(points)
    center_x /= len(points)
    return center_x, center_y


def rotate_point(rotation_point, x, y, angle):
    center_x, center_y = rotation_point
    rotated_x = center_x + (x - center_x) * cos(angle) - (y - center_y) * sin(angle)
    rotated_y = center_y + (y - center_y) * cos(angle) + (x - center_x) * sin(angle)
    return rotated_x, rotated_y
