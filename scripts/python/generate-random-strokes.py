#!/usr/bin/python
from __future__ import with_statement
import argparse
import os
import random
from alphabetspaths import *
from htmlcanvas import strokes_to_image

def make_noise(path, stroke_count=5, points_per_stroke=(20,30),
               width=100, height=100, max_dist=5,
               line_width=5, line_cap='round', line_join='miter',smooth=5):
    if isinstance(stroke_count, int): stroke_count = (stroke_count, stroke_count+1)
    if isinstance(points_per_stroke, int): points_per_stroke = (points_per_stroke, points_per_stroke+1)
    stroke_count = random.randrange(stroke_count[0], stroke_count[1])
    strokes = []
    while stroke_count > 0:
        stroke_count -= 1
        cur_points_per_stroke = random.randrange(points_per_stroke[0], points_per_stroke[1])
        stroke = [{'x':random.randrange(3, width-3),
                   'y':random.randrange(3, height-3)}]
        while cur_points_per_stroke > 0:
            cur_points_per_stroke -= 1
            stroke.append({'x':(min((width-3, max((3, stroke[-1]['x'] + random.randrange(-max_dist, max_dist+1)))))),
                           'y':(min((height-3, max((3, stroke[-1]['y'] + random.randrange(-max_dist, max_dist+1))))))})
        strokes.append(stroke)
    strokes_to_image(strokes, path, line_width=line_width,
                     line_cap=line_cap, size=(100,100), line_join=line_join, smooth=smooth)



parser = argparse.ArgumentParser(description='NMake a new random stroke noise image.')
parser.add_argument('--thickness', '--linewidth', dest='line_width',
                    type=float, default=5,
                    help='the thickness of the line in the new images')
parser.add_argument('--output', '--path', '-o', dest='path',
                    type=str, default='images/strokeNoise.png',
                    help='the relative path to store the image (default: "images/strokeNoise.png")')
parser.add_argument('--prefix', dest='prefix',
                    type=str, default=None,
                    help='the prefix for the path to store the image')
parser.add_argument('--stroke-count', '-s', dest='stroke_count',
                    type=int, default=25,
                    help='the number of strokes')
parser.add_argument('--stroke-count-range', dest='stroke_count_range',
                    type=int, default=1,
                    help='the range for the number of strokes')
parser.add_argument('--point-count', '-p', dest='point_count',
                    type=int, default=25,
                    help='the average number of points per stroke')
parser.add_argument('--point-count-range', dest='point_count_range',
                    type=int, default=10,
                    help='the range for the number of points per stroke (this controls how variable the length of the strokes are)')
parser.add_argument('--width', dest='width',
                    type=int, default=100,
                    help='the width of the image')
parser.add_argument('--height', dest='height',
                    type=int, default=100,
                    help='the height of the image')
parser.add_argument('--max-distance', '-d', dest='max_distance',
                    type=int, default=5,
                    help='the maximum distance between successive points')
parser.add_argument('--line-cap', '-c', dest='line_cap',
                    type=str, default='round', choices=("butt", "round", "square"),
                    help='the line cap (see HTML5 canvas documentation)')
parser.add_argument('--line-join', '-j', dest='line_join',
                    type=str, default='miter', choices=("round", "bevel", "miter"),
                    help='the line join (see HTML5 canvas documentation)')
parser.add_argument('--smooth', dest='smooth',
                    type=int, default=5,
                    help='how much to smooth the strokes')

if __name__ == '__main__':
    args = parser.parse_args()
    if args.prefix is None:
        from alphabetspaths import BASE_PATH
        args.prefix = BASE_PATH
    make_noise(os.path.join(args.prefix, args.path), line_width=args.line_width,
               stroke_count=(args.stroke_count - int(args.stroke_count_range/2), args.stroke_count + int(args.stroke_count_range/2) + 1),
               points_per_stroke=(args.point_count - int(args.point_count_range/2), args.point_count + int(args.point_count_range/2) + 1),
               width=args.width, height=args.height, max_dist=args.max_distance,
               line_cap=args.line_cap, line_join=args.line_join, smooth=args.smooth)
