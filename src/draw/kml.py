# coding=utf-8

import random
import colour

from src.draw.json_drawer import JSONDrawer
from src.draw.kml_drawer import KMLDrawer
from src.draw.shapes import Poly


#  TODO use colour package
def _random_color():
    r = lambda: random.randint(0, 255)
    return '50%02X%02X%02X' % (r(), r(), r())


#  TODO use colour package
def get_spaced_colors(n):
    max_value = 16581375  # 255**3
    interval = int(max_value / n)
    colors = [hex(I)[2:].zfill(6) for I in range(0, max_value, interval)]

    return colors

# TODO: see https://github.com/FlightControl-Master/MOOSE/blob/eab81a2bf9b793c83691c0cac2006a729f32bc6a/Moose%20Development/Moose/Core/Database.lua#L898 for points management

if __name__ == '__main__':
    from utils import Path
    p = Path(r'c:\users\bob\desktop\export.coord')
    from src.draw.services.coord_file_parser import CoordFileParser

    shapes = CoordFileParser(skip_points_regex_str_list=['.*(NE|SE|SW|NW)']).parse_file_into_shapes(p)
    for x in sorted(shapes, key=lambda x: x.name):
        print(x)
    exit(0)




    import json

    # color = colour.Color('red')
    # color.set_hue(0.5)
    # print(color.get_hex_l()[1:])
    # exit(0)

    t = KMLDrawer('test')
    j = JSONDrawer('test')

    polys = []
    points = []


    for l in p.lines():
        if l:
            d = json.loads(l.strip())
            if d['type'] == 'POLY':
                polys.append(d)
            elif d['type'] == 'POINT':
                if d['name'][-2:] in ['NE', 'SE', 'NW', 'SW']:
                    continue
                points.append(d)
    polys.sort(key=lambda x:x['name'])
    points.sort(key=lambda x:x['name'])

    for d in polys + points:
    # for d in polys:
        j.add_shape(dict(d))
        t.add_shape(dict(d))
    t.save('./test.kml')
    j.save('./test.json')

    exit(0)
    # exit(0)
    # print(get_spaced_colors(20)[1:])
    # exit(0)
#     l = r'MOA_A-A_SOUTH|42.24150611832, 42.010711944801, 2000|42.087541069392, 40.920969682081, 2519|43.791445751723, 40.777584772319, 2519|43.97569721989, 41.86374199029, 2519|42.241536695988, 42.01068388203, 2519'
#     l = '''TIANETI_RANGE|45.334010253098, 41.864413173918, 2000|45.177200245711, 41.781945809259, 2000|44.755023143246, 41.999172667628, 2000|44.84242545295, 42.072674939054, 2000|44.837698844095, 42.222991602396, 2000|44.883529894699, 42.317817121144, 2000|45.328345948285, 42.318336671956, 2000|45.177200245711, 41.781945809259, 2000
# MOA_A-A_SOUTH|42.24150611832, 42.010711944801, 2000|42.087541069392, 40.920969682081, 2519|43.791445751723, 40.777584772319, 2519|43.97569721989, 41.86374199029, 2519|42.241536695988, 42.01068388203, 2519
# MOA_NORTH|43.975708861364, 41.863748449142, 2000|43.979433565813, 42.221011297504, 2000|43.348996968161, 42.321684703684, 2000|43.082374256286, 42.098181175234, 2000|42.8354942002, 42.151572706993, 2000|42.778942787537, 41.96793200928, 2000|43.975707569565, 41.863740988883, 2000
# TETRA|44.143720105125, 41.719257763502, 2000|44.245774464599, 41.455481728236, 2000|44.198169180408, 41.688890085994, 2000|44.709502722663, 41.655848911615, 2000|44.713993403202, 41.445854397192, 2000|44.504603720499, 41.334293182313, 2000|44.245763333163, 41.455516252279, 2000
# MARNUELI_RANGE|45.061929127875, 41.300503937719, 2000|45.072442426814, 41.32999927885, 2000|44.89091794792, 41.222189910623, 2000|44.676325944545, 41.299223553312, 2000|44.841006918962, 41.467070132481, 2000|45.072435853811, 41.329999978718, 2000
# DUSHETI_RANGE|44.318344595122, 42.105893750229, 2000|44.412275051214, 41.995924662274, 2000|44.482186996642, 42.176983642685, 2000|44.678170499349, 42.250004771351, 2000|44.837708750804, 42.222988036908, 2000|44.842429150036, 42.072674552001, 2000|44.755030255411, 41.999174456867, 2000|44.617658400539, 41.960620101077, 2000|44.412281708262, 41.995923991532, 2000
# TKIBULI_RANGE|42.753688511376, 42.298744493742, 2000|42.898653944573, 42.542535525397, 2000|43.28031938944, 42.563819448169, 2000|43.348996968161, 42.321684703684, 2000|43.082373857091, 42.09817868135, 2000|42.8354942002, 42.151572706993, 2000|42.75430191141, 42.299303438258, 2000
# KUTAISI MOA|42.428899927627, 42.390718999854, 2000|42.241536695988, 42.01068388203, 2000|42.778942787537, 41.96793200928, 2000|42.8354942002, 42.151572706993, 2000|42.754308636663, 42.299302860604, 2000|42.428898397029, 42.390708866388, 2000'''


    colors = get_spaced_colors(len(polys) + 6)
    for poly_str, color in zip(polys, colors[3:-3]):
        poly = Poly(poly_str)
        t.add_poly(poly, color)
        j.add_poly(poly, color)
