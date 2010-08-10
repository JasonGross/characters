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
                                   scale_factor=1, offset=None, tuple_to_dict=(lambda (x, y): {'x':x, 'y':y})):
    if isinstance(strokes, str):
        strokes = stroke_to_list(strokes, parsed_to_int=True)

    if isinstance(scale_factor, int): scale_factor = (scale_factor, scale_factor)
    if isinstance(offset, int): offset = (offset, offset)
    if isinstance(size, int): size = (size, size)

    if image and not size:
        size = (image.get_height(), image.get_width())

    if not isinstance(scale_factor, dict): scale_factor = tuple_to_dict(tuple(scale_factor))
    if not isinstance(offset, dict): offset = tuple_to_dict(tuple(offset))
    if size is not None and not isinstance(size, dict): size = tuple_to_dict(tuple(size))

    strokes = [[{'x':point['x']*scale_factor['x'] + offset['x'], 'y':point['y']*scale_factor['y'] + offset['y']} \
                for point in stroke] for stroke in strokes]
    
    if size is None: 
        x_max = max(max(point['x'] for point in stroke) for stroke in strokes)
        y_max = max(max(point['y'] for point in stroke) for stroke in strokes)
        size = {'x':x_max + 5 + math.ceil(line_width), 'y':y_max + 5 + math.ceil(line_width)}
    if offset is None:
        offset = {'x':5 + math.ceil(line_width), 'y':5 + math.ceil(line_width)}

    width, height = size['x'], size['y']
    
    if not image:
        image = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
    ctx = cairo.Context(image)

    # Make the background white
    ctx.set_source_rgb(1.0, 1.0, 1.0)
    ctx.rectangle(0, 0, width, height)
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

def strokes_to_image(strokes, fobj, *args, **kargs):
    image, ctx = paint_image_with_strokes_cairo(strokes, *args, **kargs)
    image.write_to_png(fobj)

def get_image_size(file_name):
    """
    Returns the size of the image at the location on disk specified
    by file_name, as (width, height).
    """
    return Image.open(file_name).size

def convert_strokes_to_images(stroke_list, dest_images, original_image_sizes=None, 
                              line_width=5, uncompressed_ext='.stroke', compressed_ext='.cstroke',
                              verbose=True, auto_resize=False, new_max_dimen=100, pad=10, scale_factor=1, **kargs):
    if original_images is None: original_images = [None for i in stroke_list]
    for stroke_name, original_image_size, new_image in zip(stroke_list, original_image_sizes, dest_images):
        if verbose: print("I'm saving %s..." % stroke_name)
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
        offset = None
        if auto_resize and original_image_size:
            original_width, original_height = original_image_size
            if original_width > original_height:
                scale_factor = float(original_height) / new_max_dimen
            else:
                scale_factor = float(original_width) / new_max_dimen
            width, height = new_max_dimen, new_max_dimen
            if pad:
                width += 2 * pad
                height += 2 * pad
                offset = pad
            size = {'x':width, 'y':height}
        strokes_to_image(stroke, new_image, size=size, line_width=line_width, scale_factor=scale_factor, offset=offset)


def convert_all_alphabet_strokes_to_images(strokes=None, original_images=None, dest_images=None, verbose=True,
                                           auto_resize=True, new_max_dimen=100, **kargs):
    if strokes is None or dest_images is None or original_images is None:
        if verbose: print('Getting list of alphabets, images, and strokes...')
        if strokes is None:
            if verbose: print('Getting list of accepted strokes...')
            strokes = get_accepted_stroke_list(from_path='.')
        if dest_images is None: 
            if verbose: print('Getting list of accepted images...')
            dest_images = get_accepted_image_list(from_path='.')
        if original_images is None: 
            if verbose: print('Getting list of original images...')
            actual_original_images = get_original_image_list(from_path='.')
        if verbose: print('Done getting list of alphabets, images, and strokes.')
    for alphabet in strokes:
        if verbose: print("Alphabet: %s" % alphabet)
        for uid in strokes[alphabet]:
            if verbose: print(" Id: %s" % uid)
            if original_images is None:
                cur_original_image_sizes = [Image.open(image).size for image in actual_original_images[alphabet]]
                cur_original_image_sizes = [(width * 100.0 / height, 100) for width, height in cur_original_image_sizes]
            else:
                cur_original_image_sizes = original_image_sizes[alphabet][uid]
            raw_input(cur_original_image_sizes)
            convert_strokes_to_images(stroke_list[alphabet][uid], dest_images[alphabet][uid], original_image_sizes=cur_original_image_sizes,
                                      verbose=verbose, auto_resize=auto_resize, new_max_dimen=new_max_dimen, **kargs)

def convert_all_strokes_to_images(src='.', dest='.',
                                  uncompressed_ext='.stroke', compressed_ext='.cstroke', glob_name='*.*stroke',
                                  verbose=True, new_ext='.png', **kargs):
    if isinstance(src, str): src = [src]
    if isinstance(dest, str): dest = [dest]
    if len(dest) != 1 and len(dest) != len(src):
        raise ValueError("Argument `dest' has an invalid number of entries.")
    if len(dest) == 1 and len(src) > 1:
        dest = [dest[0] for i in src]
    paths = zip(src, dest)
    for src, dest in paths:
        if verbose: print("I'm in %s" % src)
        strokes = list(glob(os.path.join(src, glob_name)))
        dest_images = [os.path.join(dest, os.path.splitext(os.path.split(file_name)[-1])[0] + new_ext) for file_name in strokes]
        convert_strokes_to_images(strokes, dest_images, verbose=verbose, **kargs)

with open('../../results/accepted-strokes/angelic/angelic_01_a1j8s7giuyto4a.cstroke', 'r') as f:
    stroke = decompress_stroke(f.read(), to_string=False)
strokes_to_image(stroke, os.path.expanduser('~/Desktop/temp.png'), size=200, offset=10, line_width=1, scale_factor=2)
