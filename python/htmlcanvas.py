from __future__ import with_statement
from PIL import Image, ImageDraw
import math
from glob import glob
import os
import cairo
from warnings import warn
from alphabetspaths import *
from alphabetsutil import decompress_stroke, compress_stroke, stroke_to_list, compress_images

_LINE_CAPS = {'butt':cairo.LINE_CAP_BUTT,
              'round':cairo.LINE_CAP_ROUND,
              'square':cairo.LINE_CAP_SQUARE
              }
_LINE_JOINS = {'miter':cairo.LINE_JOIN_MITER,
               'round':cairo.LINE_CAP_ROUND,
               'bevel':cairo.LINE_JOIN_BEVEL
               }

def average(seq):
    seq = list(seq)
    return float(sum(seq)) / len(seq)

def paint_image_with_strokes_cairo(strokes, line_width=5, line_cap='round', image=None, size=None, line_join='miter',
                                   scale_factor=1, offset=None, tuple_to_dict=(lambda (x, y): {'x':x, 'y':y}),
                                   smooth=2, name=None):
##    import cPickle
##    print(list(map(repr, [strokes, line_width, line_cap, image, size, line_join, scale_factor, offset])))
##    cPickle.dump('paint_image_with_strokes_cairo' + repr((strokes, line_width, line_cap, image, size, line_join, scale_factor, offset)),
##                 open(os.path.expanduser('~/Desktop/temp.args'), 'wb'))
    if isinstance(strokes, str):
        strokes = stroke_to_list(strokes, parsed_to_int=True)

    if isinstance(scale_factor, (int, float)): scale_factor = (scale_factor, scale_factor)
    if isinstance(offset, (int, float)): offset = (offset, offset)
    if isinstance(size, (int, float)): size = (size, size)

    if image and not size:
        size = (image.get_height(), image.get_width())

    if not isinstance(scale_factor, dict): scale_factor = tuple_to_dict(tuple(scale_factor))
    if offset is not None and not isinstance(offset, dict): offset = tuple_to_dict(tuple(offset))
    if size is not None and not isinstance(size, dict): size = tuple_to_dict(tuple(size))
    
    if offset is None:
        offset = {'x':math.ceil(line_width / 2.0), 'y':math.ceil(line_width / 2.0)}

    strokes = [[{'x':point['x']*scale_factor['x'] + offset['x'], 'y':point['y']*scale_factor['y'] + offset['y']} \
                for point in stroke] for stroke in strokes]
    
    x_max = max(max(point['x'] for point in stroke) for stroke in strokes)
    y_max = max(max(point['y'] for point in stroke) for stroke in strokes)
    if size is None:
        size = {'x':x_max + 1 + math.ceil(line_width / 2.0), 'y':y_max + 1 + math.ceil(line_width / 2.0)}
    elif size['x'] < x_max or size['y'] < y_max:
        os.system('echo %s: Image size %s too small for stroke size %s.  Scale factor is %s. >> %s/image_warnings.log' % \
                  (name, size, (x_max, y_max), scale_factor, RESULTS_PATH))
        warn('Image size %s too small for stroke size %s.  Scale factor is %s.' % (size, (x_max, y_max), scale_factor))
##        raw_input('Press enter to adjust the scale factor...')
        scale_factor = max((size['x'], size['y'])) / float(max((x_max, y_max)))
        strokes = [[{'x':(point['x'] - offset['x']) * scale_factor + offset['x'],
                     'y':(point['y'] - offset['y']) * scale_factor + offset['y']} \
                    for point in stroke] for stroke in strokes]

    if smooth:
        strokes = [[stroke[0]] + \
                   [{'x':average(pt['x'] for pt in stroke[i:i+smooth]),
                     'y':average(pt['y'] for pt in stroke[i:i+smooth])} for i in range(len(stroke) - smooth)] + \
                   [stroke[-1]] for stroke in strokes]
##    import cPickle
##    cPickle.dump(strokes, open(os.path.expanduser('~/Desktop/temp.strokes'), 'wb'))
    
    width, height = int(math.ceil(size['x'])), int(math.ceil(size['y']))
    
    if not image:
        image = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
    ctx = cairo.Context(image)

    ctx.set_antialias(cairo.ANTIALIAS_NONE)

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
    image.write_to_png(os.path.abspath(fobj))

def get_image_size(file_name):
    """
    Returns the size of the image at the location on disk specified
    by file_name, as (width, height).
    """
    return Image.open(file_name).size

def convert_strokes_to_images(stroke_list, dest_images, original_image_sizes=None, 
                              line_width=5, uncompressed_ext='.stroke', compressed_ext='.cstroke',
                              verbose=True, auto_resize=False, new_max_dimen=100, pad=2.5, scale_factor=1, **kargs):
    if original_image_sizes is None: original_image_sizes = [None for i in stroke_list]
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
                scale_factor = new_max_dimen / float(original_width)
                width, height = new_max_dimen, original_height * scale_factor
            else:
                scale_factor = new_max_dimen / float(original_height)
                width, height = original_width * scale_factor, new_max_dimen
            if pad:
                width += math.ceil(2 * pad)
                height += math.ceil(2 * pad)
                offset = pad
            if width != height:
                offset = [offset, offset]
            if width > height:
                offset[1] += (width - height) / 2.0
                height = width
            elif height > width:
                offset[0] += (height - width) / 2.0
                width = height
            size = {'x':width, 'y':height}
        strokes_to_image(stroke, new_image, size=size, line_width=line_width, scale_factor=scale_factor, offset=offset, name=stroke_name)


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
                cur_original_image_sizes = [(int(math.ceil(width * 100.0 / height)), 100) for width, height in cur_original_image_sizes]
            else:
                cur_original_image_sizes = original_image_sizes[alphabet][uid]
            convert_strokes_to_images(strokes[alphabet][uid], dest_images[alphabet][uid], original_image_sizes=cur_original_image_sizes,
                                      verbose=verbose, auto_resize=auto_resize, new_max_dimen=new_max_dimen, **kargs)
            compress_images(image_list=dest_images[alphabet][uid], do_color_change=False)
##            import cProfile
##            cProfile.run('compress_images(image_list=dest_images["' + alphabet + '"]["' + uid + '"], do_color_change=False)')

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

##with open('../../results/accepted-strokes/angelic/angelic_01_a1j8s7giuyto4a.cstroke', 'r') as f:
##    stroke = decompress_stroke(f.read(), to_string=False)
##strokes_to_image(stroke, os.path.expanduser('~/Desktop/temp.png'), size=200, offset=10, line_width=1, scale_factor=2)


##im,ctx=paint_image_with_strokes_cairo([[{'y': 40, 'x': 35, 't': 0}, {'y': 40, 'x': 35, 't': 20}, {'y': 41, 'x': 35, 't': 61}, {'y': 42, 'x': 35, 't': 74}, {'y': 43, 'x': 35, 't': 86}, {'y': 45, 'x': 35, 't': 97}, {'y': 48, 'x': 35, 't': 107}, {'y': 52, 'x': 35, 't': 118}, {'y': 57, 'x': 33, 't': 129}, {'y': 59, 'x': 33, 't': 139}, {'y': 64, 'x': 31, 't': 149}, {'y': 68, 'x': 28, 't': 160}, {'y': 71, 'x': 28, 't': 171}, {'y': 71, 'x': 29, 't': 182}, {'y': 72, 'x': 30, 't': 191}, {'y': 73, 'x': 28, 't': 231}, {'y': 74, 'x': 27, 't': 315}], [{'y': 37, 'x': 40, 't': 1746}, {'y': 38, 'x': 41, 't': 1877}, {'y': 39, 'x': 42, 't': 1888}, {'y': 41, 'x': 44, 't': 1898}, {'y': 42, 'x': 45, 't': 1908}, {'y': 45, 'x': 47, 't': 1919}, {'y': 46, 'x': 48, 't': 1930}, {'y': 46, 'x': 49, 't': 1940}, {'y': 47, 'x': 49, 't': 1969}, {'y': 48, 'x': 49, 't': 1981}, {'y': 48, 'x': 50, 't': 1992}, {'y': 49, 'x': 51, 't': 2011}, {'y': 50, 'x': 51, 't': 2022}, {'y': 51, 'x': 51, 't': 2031}, {'y': 53, 'x': 52, 't': 2042}, {'y': 55, 'x': 54, 't': 2053}, {'y': 56, 'x': 54, 't': 2064}, {'y': 57, 'x': 54, 't': 2097}, {'y': 58, 'x': 55, 't': 2108}, {'y': 59, 'x': 56, 't': 2187}, {'y': 60, 'x': 57, 't': 2335}, {'y': 62, 'x': 58, 't': 2454}, {'y': 63, 'x': 58, 't': 2468}, {'y': 63, 'x': 59, 't': 2479}, {'y': 65, 'x': 61, 't': 2489}, {'y': 66, 'x': 62, 't': 2629}]], 0.01, 'round', None, {'y': 120, 'x': 120}, 'miter', 0.91946308724832226, 10)

##import cProfile
##strokes = get_accepted_stroke_list(from_path='.')
##dest_images = get_accepted_image_list(from_path='.')
##use_strokes = {'earlyaramaic':strokes['earlyaramaic']}
##convert_all_alphabet_strokes_to_images(use_strokes, dest_images=dest_images)
##cProfile.run('convert_all_alphabet_strokes_to_images(use_strokes, dest_images=dest_images)')
