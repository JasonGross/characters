from __future__ import with_statement
from PIL import Image, ImageDraw
import math
from glob import glob
import os
from alphabetsutil import decompress_stroke, compress_stroke, stroke_to_list

def paint_image_with_strokes(strokes, line_width=1, line_cap='round', image=None, size=None, line_join='miter'):
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
    
    if line_cap == 'butt':
        def do_line_end(x, y, *args, **kargs):
            pass
    elif line_cap == 'round':
        def do_line_end(x, y, *args, **kargs):
            draw.ellipse((x - float(line_width) / 2, y - float(line_width) / 2,
                          x + float(line_width) / 2, y + float(line_width) / 2),
                         fill=line_color)
    elif line_cap == 'square':
        def do_line_end(x, y, last_x=None, last_y=None, *args, **kargs):
            if last_x is None and last_y is None:
                draw.rectangle((x - float(line_width) / 2, y - float(line_width) / 2,
                                x + float(line_width) / 2, y + float(line_width) / 2),
                               fill=line_color)
            elif last_x is None or last_y is None:
                raise ValueError
            elif x == last_x:
                direction = (1 if y > last_y else -1)
                draw.line((x, y,
                           x, y + direction*float(line_width)/2),
                          fill=line_color, width=line_width)
            elif y == last_y:
                direction = (1 if x > last_x else -1)
                draw.line((x, y,
                           x + direction*float(line_width)/2, y),
                          fill=line_color, width=line_width)
            else:
                x_direction = (1 if x > last_x else -1)
                y_direction = (1 if y > last_y else -1)
                dx = abs(math.sqrt((float(line_width) / 2) ** 2 / (1 + slope) ** 2))
                dy = abs(slope * dx)
                draw.line((x, y,
                           x + x_direction*dx, y + y_direction*dy),
                          fill=line_color, width=line_width)
    else:
        raise ValueError
    
    if line_join == 'bevel':
        NotImplemented
    elif line_join == 'round':
        NotImplemented
    elif line_join == 'miter':
        NotImplemented
    else:
        raise ValueError
  
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

def strokes_to_image(strokes, file_name, line_width=1, format=None):
    image = paint_image_with_strokes(strokes, line_width=line_width)
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
            strokes_to_image(strokes=stroke, file_name=new_file_name, format=format, line_width=line_width)
