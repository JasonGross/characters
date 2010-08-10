from __future__ import with_statement
##from PIL import Image, ImageDraw
import math
from glob import glob
import os
import cairo
from PIL import Image
from alphabetspaths import *
from alphabetsutil import decompress_stroke, compress_stroke, stroke_to_list

_LINE_CAPS = {'butt':cairo.LINE_CAP_BUTT,
              'round':cairo.LINE_CAP_ROUND,
              'square':cairo.LINE_CAP_SQUARE
              }
_LINE_JOINS = {'miter':cairo.LINE_JOIN_MITER,
               'round':cairo.LINE_CAP_ROUND,
               'bevel':cairo.LINE_JOIN_BEVEL
               }

def paint_image_with_strokes(strokes, line_width=5, line_cap='round', image=None, size=None, line_join='miter',
                             scale_factor=(0,0), offset=(0,0), tuple_to_dict=(lambda (x, y): {'x':x, 'y':y})):
    if isinstance(strokes, str):
        strokes = stroke_to_list(strokes, parsed_to_int=True)
    line_color = 'black'

    if isinstance(scale_factor, int): scale_factor = (scale_factor, scale_factor)
    if isinstance(offset, int): offset = (offset, offset)

    if not isinstance(scale_factor, dict):
        scale_factor = tuple_to_dict(tuple(scale_factor))
    if not isinstance(offset, dict):
        offset = tuple_to_dict(tuple(offset))
    if not isinstance(size, dict):
        size = tuple_to_dict(tuple(size))

    strokes = [[{'x':point['x']*scale_factor['x']+offset['x'], 'y':point['y']*scale_factor['y'] + offset['y']} \
                for point in stroke] for stroke in strokes]

    if size is None: 
        x_max = max(max(point['x'] for point in stroke) for stroke in strokes)
        y_max = max(max(point['y'] for point in stroke) for stroke in strokes)
        size = {'x':x_max+20+line_width, 'y':y_max+20+line_width}
    
    if not image:
        image = cairo.ImageSurface(cairo.FORMAT_RGB24, size['x'], size['y'])
    ctx = cairo.Context(image)
    ctx.set_line_cap(_LINE_CAPS[line_cap])
    ctx.set_line_join(_LINE_JOINS[line_join])
    ctx.set_line_width(line_width)
    for stroke in strokes:
        x, y = stroke[0]['x'], stroke[0]['y']

        ctx.rectangle(x - line_width / 2.0, y - line_width / 2.0, line_width, line_width)
        ctx.move_to(x, y)
        for point in stroke:
            x, y = point['x'], point['y']
            ctx.line_to(x, y)
        ctx.stroke()
    return image, ctx

def strokes_to_image(strokes, fobj, line_width=5, line_cap='round', size=None, line_join='miter',
                             scale_factor=(0,0), offset=(0,0), tuple_to_dict=(lambda (x, y): {'x':x, 'y':y})):
    image, ctx = paint_image_with_strokes(strokes, line_width=line_width, line_cap=line_cap,
                                          size=size, line_join=line_join, scale_factor=scale_factor,
                                          offset=offset, tuple_to_dict=tuple_to_dict)
    image.write_to_png(fobj)

def get_image_size(file_name):
    """
    Returns the size of the image at the location on disk specified
    by file_name, as (width, height).
    """
    return Image.open(file_name).size


def convert_all_strokes_to_images(strokes=get_accepted_stroke_list(), original_images=get_accepted_image_list(),
                                  dest_images=get_accepted_image_list(),
                                  line_width=5, uncompressed_ext='.stroke', compressed_ext='.cstroke',
                                  verbose=True, resize=True, new_max_dimen=100):
    for alphabet in strokes:
        if verbose: print("Alphabet: %s" % alphabet)
        for uid in stroke_list[alphabet]:
            if verbose: print("  Id: %s" % uid)
            for stroke_name, original_image, new_image in zip(stroke_list[alphabet][uid],
                                                              original_images[alphabet][uid],
                                                              dest_images[alphabet][uid]):
                if stroke_name[-len(uncompressed_ext):].lower() == uncompressed_ext.lower():
                    with open(stroke_name, 'r') as f:
                        stroke = f.read().strip()
                elif stroke_name[-len(compressed_ext):].lower() == compressed_ext.lower():
                    with open(stroke_name, 'rb') as f:
                        cstroke = f.read()
                    stroke = decompress_stroke(cstroke, to_string=False)
                else:
                    print('Malformed file name: ' + stroke_name)
                    continue
                size = None
                if resize:
                    width, height = get_image_size(original_image)
                    if width > height:
                        width, height = new_max_dimen, float(height) * new_max_dimen / width
                    elif width < height:
                        width, height = float(width) * new_max_dimen / height, new_max_dimen
                    else:
                        width, height = new_max_dimen, new_max_dimen
                    size = {'x':width, 'y':height}
                strokes_to_image(stroke, new_image, size=size, line_width=line_width)
