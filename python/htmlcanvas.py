from __future__ import with_statement
from PIL import Image, ImageDraw
import math
from glob import glob
import os
import cairo
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

def paint_image_with_strokes_cairo(strokes, line_width=5, line_cap='round', image=None, size=None, line_join='miter',
                                   scale_factor=1, offset=0, tuple_to_dict=(lambda (x, y): {'x':x, 'y':y})):
    if isinstance(strokes, str):
        strokes = stroke_to_list(strokes, parsed_to_int=True)

    if isinstance(scale_factor, int): scale_factor = (scale_factor, scale_factor)
    if isinstance(offset, int): offset = (offset, offset)
    if isinstance(size, int): size = (size, size)

    if not isinstance(scale_factor, dict):
        scale_factor = tuple_to_dict(tuple(scale_factor))
    if not isinstance(offset, dict):
        offset = tuple_to_dict(tuple(offset))
    if size and not isinstance(size, dict):
        size = tuple_to_dict(tuple(size))

    strokes = [[{'x':point['x']*scale_factor['x']+offset['x'], 'y':point['y']*scale_factor['y'] + offset['y']} \
                for point in stroke] for stroke in strokes]
    
    if size is None: 
        x_max = max(max(point['x'] for point in stroke) for stroke in strokes)
        y_max = max(max(point['y'] for point in stroke) for stroke in strokes)
        size = {'x':x_max+20+line_width, 'y':y_max+20+line_width}

    WIDTH, HEIGHT = size['x'], size['y']
    
    if not image:
        image = cairo.ImageSurface(cairo.FORMAT_RGB24, WIDTH, HEIGHT)
    ctx = cairo.Context(image)

    # Make the background white
    ctx.set_source_rgb(1.0, 1.0, 1.0)
    ctx.rectangle(0, 0, WIDTH, HEIGHT)
    ctx.fill()

    ctx.set_line_cap(_LINE_CAPS[line_cap])
    ctx.set_line_join(_LINE_JOINS[line_join])
    ctx.set_line_width(line_width)

    ctx.set_source_rgb(0, 0, 0) # make the stroke color black



    for stroke in strokes:
        x, y = stroke[0]['x'], stroke[0]['y']

        ctx.rectangle(x - line_width / 2.0, y - line_width / 2.0, line_width, line_width)
        ctx.fill()

##        image.write_to_png(os.path.expanduser('~/Desktop/temp.png')); raw_input()
        
        ctx.move_to(x, y)
        for point in stroke:
            x, y = point['x'], point['y']
            ctx.line_to(x, y)
        ctx.stroke()
##        image.write_to_png(os.path.expanduser('~/Desktop/temp.png')); raw_input()
    return image, ctx

def strokes_to_image(strokes, fobj, line_width=5, line_cap='round', size=None, line_join='miter',
                     scale_factor=1, offset=0, tuple_to_dict=(lambda (x, y): {'x':x, 'y':y})):
    image, ctx = paint_image_with_strokes_cairo(strokes, line_width=line_width, line_cap=line_cap,
                                                size=size, line_join=line_join, scale_factor=scale_factor,
                                                offset=offset, tuple_to_dict=tuple_to_dict)
    image.write_to_png(fobj)

def get_image_size(file_name):
    """
    Returns the size of the image at the location on disk specified
    by file_name, as (width, height).
    """
    return Image.open(file_name).size


def convert_all_alphabet_strokes_to_images(strokes=None, original_images=None,
                                           dest_images=None,
                                           line_width=5, uncompressed_ext='.stroke', compressed_ext='.cstroke',
                                           verbose=True, resize=True, new_max_dimen=100, pad=10):
    if strokes is None: strokes = get_accepted_stroke_list()
    if original_images is None: original_images = get_accepted_image_list()
    if dest_images is None: dest_images = get_accepted_image_list()
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
                offset = 0
                if resize:
                    width, height = get_image_size(original_image)
                    if width > height:
                        scale_factor = float(height) / new_max_dimen
                    else:
                        scale_factor = float(width) / new_max_dimen
                    width, height = new_max_dimen, new_max_dimen
                    if pad:
                        width += 2 * pad
                        height += 2 * pad
                        offset = pad
                    size = {'x':width, 'y':height}
                strokes_to_image(stroke, new_image, size=size, line_width=line_width, scale_factor=scale_factor)

##################################################### PIL ##########################################################

def paint_image_with_strokes_PIL(strokes, line_width=1, image=None, size=None, **kargs):
    if isinstance(strokes, str):
        strokes = stroke_to_list(strokes, parsed_to_int=True)
    line_color = 'black'

    if size is None: 
        x_max = max(max(point['x'] for point in stroke) for stroke in strokes)
        y_max = max(max(point['y'] for point in stroke) for stroke in strokes)
        size = (x_max+20+line_width, y_max+20+line_width)
    
    if not image:
        image = Image.new(mode='1', size=size, color='white')
    draw = ImageDraw.Draw(image)
    
    draw.rectangle((0, 0) + image.size, fill='white')
    for stroke in strokes:
        x, y = stroke[0]['x'], stroke[0]['y']

        draw.rectangle((x - float(line_width) / 2, y - float(line_width) / 2,
                        x + float(line_width) / 2, y + float(line_width) / 2),
                       fill=line_color)

##        do_line_end
        for point in stroke:
            last_x, last_y = x, y
            x, y = point['x'], point['y']
            draw.line((last_x, last_y, x, y), fill='black', width=line_width)
    return image

def strokes_to_image_PIL(strokes, file_name, line_width=1, format=None):
    image = paint_image_with_strokes_PIL(strokes, line_width=line_width)
    if format:
        image.save(file_name, format=format)
    else:
        image.save(file_name)

def convert_all_strokes_to_images(src='.', dest='.', format=None, line_width=1,
                                  uncompressed_ext='.stroke', compressed_ext='.cstroke', glob_name='*.*stroke',
                                  verbose=True, new_ext='.png'):
    if isinstance(src, str): src = [src]
    if isinstance(dest, str): dest = [dest]
    if len(dest) != 1 and len(dest) != len(src):
        raise ValueError("Argument `dest' has an invalid number of entries.")
    if len(dest) == 1 and len(src) > 1:
        dest = [dest[0] for i in src]
    paths = zip(src, dest)
    for src, dest in paths:
        print("I'm in %s" % src)
        for file_name in glob(os.path.join(src, glob_name)):
            if verbose: print("I'm saving " + file_name)
            if file_name[-len(uncompressed_ext):].lower() == uncompressed_ext.lower():
                with open(file_name, 'r') as f:
                    stroke = f.read().strip()
            elif file_name[-len(compressed_ext):].lower() == compressed_ext.lower():
                with open(file_name, 'rb') as f:
                    cstroke = f.read()
                stroke = decompress_stroke(cstroke)
            else:
                print('Malformed file name: ' + file_name)
                continue
            new_file_name = os.path.join(dest, os.path.splitext(os.path.split(file_name)[-1])[0] + new_ext)
            strokes_to_image_PIL(strokes=stroke, file_name=new_file_name, format=format, line_width=line_width)

with open('../../results/accepted-strokes/angelic/angelic_01_a1j8s7giuyto4a.cstroke', 'r') as f:
    stroke = decompress_stroke(f.read(), to_string=False)
strokes_to_image(stroke, os.path.expanduser('~/Desktop/temp.png'), size=200, offset=10, line_width=1, scale_factor=2)
