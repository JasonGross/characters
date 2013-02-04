#!/usr/bin/python
from __future__ import with_statement
import math
from glob import glob
import os, sys
import base64
import urllib
from warnings import warn

bad = False

try:
    import argparse
except ImportError:
    sys.stderr.write('Error: This script requires the argparse module.')
    bad = True
try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.stderr.write('Error: This script requires the PIL (Python Image Library)')
    bad = True
try:
    import cairo
except ImportError:
    sys.stderr.write('Error: This script requires the cairo module.')
    bad = True

if bad:
    if __name__ == '__main__':
        sys.exit(1)
    else:
        raise ImportError

##################################################################################
## stroke compression

def stroke_to_list(stroke, very_slow=False, parsed_to_int=False, strip_minus=True):
##        stroke = stroke.replace("'x':", "(x`").replace("'x':", "(x`").replace("'x':", "(x`").replace("'x':", "(x`")
##        stroke = stroke.replace(",'", "|'")
##        stroke = stroke.replace("'x':", '').replace("'y':", '').replace("'t':", '')
    if strip_minus: stroke = stroke.replace('-', '') # because minus signs are bad
    if very_slow: return eval(stroke)
    strokes = [cur_stroke[1:-1].split('},{') for cur_stroke in stroke.strip()[2:-2].split('],[')]
    for stroke in strokes:
        for point_i in range(len(stroke)):
            point = stroke[point_i]
            if point[5] == ',':
                if point[11] == ',':
                    stroke[point_i] = {'x':point[4:5], 'y':point[10:11], 't':point[16:]}
                elif point[12] == ',':
                    stroke[point_i] = {'x':point[4:5], 'y':point[10:12], 't':point[17:]}
                elif point[13] == ',':
                    stroke[point_i] = {'x':point[4:5], 'y':point[10:13], 't':point[18:]}
            elif point[6] == ',':
                if point[12] == ',':
                    stroke[point_i] = {'x':point[4:6], 'y':point[11:12], 't':point[17:]}
                elif point[13] == ',':
                    stroke[point_i] = {'x':point[4:6], 'y':point[11:13], 't':point[18:]}
                elif point[14] == ',':
                    stroke[point_i] = {'x':point[4:6], 'y':point[11:14], 't':point[19:]}
            elif point[7] == ',':
                if point[13] == ',':
                    stroke[point_i] = {'x':point[4:7], 'y':point[12:13], 't':point[18:]}
                elif point[14] == ',':
                    stroke[point_i] = {'x':point[4:7], 'y':point[12:14], 't':point[19:]}
                elif point[15] == ',':
                    stroke[point_i] = {'x':point[4:7], 'y':point[12:15], 't':point[20:]}
            else:
                print('Slow')
                stroke[point_i] = point.replace("'x':", '').replace("'y':", '').replace("'t':", '').split(',')
                point = stroke[point_i]
                stroke[point_i] = {'x':point[0], 'y':point[1], 't':point[2]}
    if parsed_to_int:
        strokes = [[{'x':int(point['x']), 'y':int(point['y']), 't':int(point['t'])} for point in stroke] for stroke in strokes]
    return strokes

BIG_BYTE_PLUS_ONE = 1 << 8

def uint_encode(number, total_bytes=0):
    rtn = []
    while number:
        rtn.append(chr(number % BIG_BYTE_PLUS_ONE))
        number >>= 8
    while total_bytes > len(rtn):
        rtn.append('\x00')
    return ''.join(reversed(rtn))

def uint_decode(number):
    rtn = 0
    for character in number:
        rtn <<= 8
        if isinstance(character, int):
            rtn += character
        else:
            rtn += ord(character)
    return rtn

def sint_encode(number, total_bytes=0):
    return uint_encode(sint_encode_to_uint(number), total_bytes=total_bytes)
    

def sint_decode(number):
    return sint_decode_from_uint(uint_decode(number))

def sint_encode_to_uint(number):
    if number > 0:
        return 2 * number - 1
    else:
        return -2 * number

def sint_decode_from_uint(number):
    if number % 2 == 0:
        return -number / 2
    else:
        return (number + 1) / 2

def compress_stroke(stroke, version=2, safe=True):
    # lower bits are xs, upper bits are ys
    original_stroke = stroke
    stroke_list = stroke_to_list(stroke)
    xs, ys, ts = [], [], []
    if version >= 1:
        last_t = 0
    for stroke_part in stroke_list:
        xs.append([int(point['x'])+1 for point in stroke_part])
        ys.append([int(point['y'])+1 for point in stroke_part])
        if version == 0:
            ts.append([int(point['t'])+1 for point in stroke_part])
        else:
            ts.append([])
            for point in stroke_part:
                if last_t > int(point['t']): return compress_stroke(original_stroke, version=0, safe=safe)
                if version >= 2 and last_t == int(point['t']) and last_t > 0: return compress_stroke(original_stroke, version=1, safe=safe)
                ts[-1].append((int(point['t']) - last_t) + 1)
                last_t = int(point['t'])

    strokes = {'xs':xs, 'ys':ys, 'ts':ts}
    mins, maxes = {}, {}
    bits = {}
    for key in strokes:
        maxes[key] = max(map(max, strokes[key]))
        mins[key] = min(map(min, strokes[key]))
        
        if maxes[key] < 0:
            mins[key], maxes[key] = -maxes[key], -mins[key]
            strokes[key] = [[-s for s in part] for part in strokes[key]]
            
        if mins[key] <= 0:
            strokes[key] = [[s - mins[key] + 1 for s in part] for part in strokes[key]]
            mins[key], maxes[key] = 1, maxes[key] - mins[key] + 1

        if version < 2 or key == 'ts':
            bits[key] = int(1 + math.floor(math.log(max((1, maxes[key]))) / math.log(2)))

    
    if version >= 2:
        for key in ('xs', 'ys'):
            for stroke_i, stroke in enumerate(strokes[key]):
                last = 0
                for point_i in range(len(stroke)):
                    last, stroke[point_i] = stroke[point_i], stroke[point_i] - last
                    if point_i != 0:
                        stroke[point_i] = sint_encode_to_uint(stroke[point_i])
            maxes[key] = max(map(max, strokes[key]))
            mins[key] = min(map(min, strokes[key]))
            bits[key] = int(1 + math.floor(math.log(max((1, maxes[key]))) / math.log(2)))
        if bits['xs'] + bits['ys'] <= 8: return compress_stroke(original_stroke, version=1, safe=safe)
            
                
    def default_make_first_line(bits, version, points):
        if bits['xs'] + bits['ys'] <= 8:
            first_line = str(version) + '\x00' + chr(bits['xs']) + '\x00' + chr(bits['ys'])
        elif bits['xs'] <= 8 and bits['ys'] <= 8:
            first_line = str(version) + '\x00' + chr(bits['xs']) + '\x00' + chr(bits['ys'])
        else:
            if bits['xs'] <= 8:
                first_line = str(version) + '\x00' + chr(bits['xs'])
            else:
                if bits['xs'] < BIG_BYTE_PLUS_ONE:
                    first_line = str(version) + '\x00u' + chr(bits['xs'])
                else:
                    first_line = str(version) + '\x00ul' + str(bits['xs'])
            
            if bits['ys'] <= 8:
                first_line += '\x00' + chr(bits['ys'])
            else:
                if bits['ys'] < BIG_BYTE_PLUS_ONE:
                    first_line += '\x00u' + chr(bits['ys'])
                else:
                    first_line += '\x00ul' + str(bits['ys'])
        if bits['ts'] <= 8:
            first_line += '\x00' + chr(bits['ts'])
        else:
            if bits['ts'] < BIG_BYTE_PLUS_ONE:
                first_line += '\x00u' + chr(bits['ts'])
            else:
                first_line += '\x00ul' + str(bits['ts'])
        first_line += '\x00'
        return first_line

    def empty_make_first_line(*args, **kargs):
        return ''

    def make_encode_point_by_scheme(bits):
        if bits['xs'] + bits['ys'] <= 8:
            if bits['ts'] <= 8:
                def encode_point_by_scheme(point):
                    return chr(point[0] + (point[1] << bits['xs'])) + chr(point[2])
            else:
                total_bytes = int(1 + (bits['ts'] - 1) / 8)
                def encode_point_by_scheme(point):
                    return chr(point[0] + (point[1] << bits['xs'])) + uint_encode(point[2], total_bytes=total_bytes)
        else:
            if bits['xs'] <= 8: 
                if bits['ys'] <= 8:
                    if bits['ts'] <= 8:
                        def encode_point_by_scheme(point):
                            return chr(point[0]) + chr(point[1]) + chr(point[2])
                    else:
                        total_bytes = int(1 + (bits['ts'] - 1) / 8)
                        def encode_point_by_scheme(point):
                            return chr(point[0]) + chr(point[1]) + uint_encode(point[2], total_bytes=total_bytes)
                else:
                    total_bytes_ys = int(1 + (bits['ys'] - 1) / 8)
                    if bits['ts'] <= 8:
                        def encode_point_by_scheme(point):
                            return chr(point[0]) + uint_encode(point[1], total_bytes=total_bytes_ys) + chr(point[2])
                    else:
                        total_bytes_ts = int(1 + (bits['ts'] - 1) / 8)
                        def encode_point_by_scheme(point):
                            return chr(point[0]) + uint_encode(point[1], total_bytes=total_bytes_ys) + uint_encode(point[2], total_bytes=total_bytes_ts)
            else:
                total_bytes_xs = int(1 + (bits['xs'] - 1) / 8)
                if bits['ys'] <= 8:
                    if bits['ts'] <= 8:
                        def encode_point_by_scheme(point):
                            return uint_encode(point[0], total_bytes=total_bytes_xs) + chr(point[1]) + chr(point[2])
                    else:
                        total_bytes = int(1 + (bits['ts'] - 1) / 8)
                        def encode_point_by_scheme(point):
                            return uint_encode(point[0], total_bytes=total_bytes_xs) + chr(point[1]) + uint_encode(point[2], total_bytes=total_bytes)
                else:
                    total_bytes_ys = int(1 + (bits['ys'] - 1) / 8)
                    if bits['ts'] <= 8:
                        def encode_point_by_scheme(point):
                            return uint_encode(point[0], total_bytes=total_bytes_xs) + uint_encode(point[1], total_bytes=total_bytes_ys) + chr(point[2])
                    else:
                        total_bytes_ts = int(1 + (bits['ts'] - 1) / 8)
                        def encode_point_by_scheme(point):
                            return uint_encode(point[0], total_bytes=total_bytes_xs) + uint_encode(point[1], total_bytes=total_bytes_ys) + uint_encode(point[2], total_bytes=total_bytes_ts)
        return encode_point_by_scheme
    
    def encode_stroke_part(bits, version, points, make_first_line=default_make_first_line):
        encode_point_by_scheme = make_encode_point_by_scheme(bits)
        first_line = make_first_line(bits=bits, version=version, points=points)
        points = [encode_point_by_scheme(point) for point in points]
        return first_line + ''.join(points)

    
    if version < 2:
        points = []
        for stroke_i in range(len(stroke_list)):
            points += [(strokes['xs'][stroke_i][point_i], strokes['ys'][stroke_i][point_i], strokes['ts'][stroke_i][point_i])
                       for point_i in range(len(stroke_list[stroke_i]))]
            points.append((0, 0, 0))
        points = points[:-1]

        return encode_stroke_part(bits, version, points)
    else:
        first_line = default_make_first_line(bits=bits, version=version, points=[(xs[0], ys[0], ts[0]) for xs, ys, ts in \
                                                                                 zip(strokes['xs'], strokes['ys'], strokes['ts'])])
        rtn = [first_line]
        stroke_parts = [{'xs':xs, 'ys':ys, 'ts':ts} for xs, ys, ts in zip(strokes['xs'], strokes['ys'], strokes['ts'])]
        default_encode_point_by_scheme = make_encode_point_by_scheme(bits)
        encoded_zeros = default_encode_point_by_scheme((0, 0, 0))
        for stroke_i, stroke in enumerate(stroke_parts):
            first, rest = dict((key, stroke[key][0]) for key in stroke), dict((key, stroke[key][1:]) for key in stroke)
            if rest['xs']: # not a single point
                stroke_bits = {'ts':bits['ts']}
                stroke_maxes = {}
                for key in ('xs', 'ys'):
                    stroke_maxes[key] = max(rest[key])
                    stroke_bits[key] = int(1 + math.floor(math.log(max((1, maxes[key]))) / math.log(2)))
            if rest['xs'] and stroke_bits['xs'] + stroke_bits['ys'] <= 8:
                rtn.append(default_encode_point_by_scheme((stroke_bits['xs'], stroke_bits['ys'], 0)))
                rtn.append(default_encode_point_by_scheme((first['xs'], first['ys'], first['ts'])))
                rtn.append(encode_stroke_part(stroke_bits, version, zip(rest['xs'], rest['ys'], rest['ts']), make_first_line=empty_make_first_line))
                rtn.append(encode_stroke_part(stroke_bits, version, [(0,0,0)], make_first_line=empty_make_first_line))
            else:
                rtn.append(encode_stroke_part(bits, version, zip(stroke['xs'], stroke['ys'], stroke['ts']), make_first_line=empty_make_first_line))
                rtn.append(encoded_zeros)
        rtn = ''.join(rtn[:-1])
        return rtn
    

def decompress_stroke(cstroke, to_string=True, point_to_string=False):
    # lower bits are xs, upper bits are ys
##    print(cstroke)
    if isinstance(cstroke, str): cstroke = map(ord, cstroke)
    else: cstroke = list(cstroke)
    version = int(''.join(map(chr, cstroke[:cstroke.index(0)])))
    cstroke = cstroke[cstroke.index(0)+1:]
    bits = {}
    for key in ('xs', 'ys', 'ts'):
        if cstroke[0] != ord('u') or (cstroke[1] == 0 and cstroke[2] != 0):
            bits[key] = cstroke[0]
            cstroke = cstroke[2:]
        elif cstroke[0] == ord('u'):
            if cstroke[1] != ord('l') or (cstroke[2] == 0 and cstroke[3] != 0):
                bits[key] = cstroke[1]
                cstroke = cstroke[3:]
            elif cstroke[1] == ord('l'):
                bits[key] = int(cstroke[2:cstroke.index(0)])
                cstroke = cstroke[cstroke.index(0)+1:]
            else:
                raise ValueError('cstroke must have l for key ' + key) # todo: make this less cryptic
        else:
            raise ValueError('cstroke must have u for key ' + key) # todo: make this less cryptic

    stroke = []

    x_bytes = int(1 + (bits['xs'] - 1) / 8)
    y_bytes = int(1 + (bits['ys'] - 1) / 8)
    t_bytes = int(1 + (bits['ts'] - 1) / 8)
##    print(bits)
    
    while cstroke:
        point = {}
        if bits['xs'] + bits['ys'] <= 8:
            xs_and_ys = cstroke[0]
            cstroke = cstroke[1:]
            point['xs'], point['ys'] = (xs_and_ys % (1 << bits['xs'])), (xs_and_ys >> bits['xs'])
        else:
            point['xs'] = uint_decode(cstroke[:x_bytes])
            cstroke = cstroke[x_bytes:]

            point['ys'] = uint_decode(cstroke[:y_bytes])
            cstroke = cstroke[y_bytes:]

        point['ts'] = uint_decode(cstroke[:t_bytes])
        cstroke = cstroke[t_bytes:]

        if version >= 2:
            if point['ts'] == 0:
                cur_bits = point
                if cur_bits['xs'] + cur_bits['ys'] > 8:
                    raise ValueError('Per-stroke compression is only implemented for a strokes with points which each fit into a single byte.')
                cur_bits['ts'] = bits['ts']

                # decode the first point, which goes according to the old scheme
                point = {}
                if bits['xs'] + bits['ys'] <= 8:
                    xs_and_ys = cstroke[0]
                    cstroke = cstroke[1:]
                    point['xs'], point['ys'] = (xs_and_ys % (1 << bits['xs'])), (xs_and_ys >> bits['xs'])
                else:
                    point['xs'] = uint_decode(cstroke[:x_bytes])
                    cstroke = cstroke[x_bytes:]

                    point['ys'] = uint_decode(cstroke[:y_bytes])
                    cstroke = cstroke[y_bytes:]

                point['ts'] = uint_decode(cstroke[:t_bytes])
                cstroke = cstroke[t_bytes:]
                stroke.append(point)
            else:
                cur_bits = bits
                stroke.append(point)

            

            while cstroke and (point['xs'] != 0 or point['ys'] != 0 or point['ts'] != 0): # keep going until we get to (0, 0, 0), where we revert back to the old scheme.
                point = {}
                
                if cur_bits['xs'] + cur_bits['ys'] <= 8:
                    xs_and_ys = cstroke[0]
                    cstroke = cstroke[1:]
                    point['xs'], point['ys'] = (xs_and_ys % (1 << cur_bits['xs'])), (xs_and_ys >> cur_bits['xs'])
                else:
                    point['xs'] = uint_decode(cstroke[:x_bytes])
                    cstroke = cstroke[x_bytes:]

                    point['ys'] = uint_decode(cstroke[:y_bytes])
                    cstroke = cstroke[y_bytes:]
                
                point['ts'] = uint_decode(cstroke[:t_bytes])
                cstroke = cstroke[t_bytes:]
                stroke.append(point)
        else:
            stroke.append(point)

    stroke_list = []
    cur_stroke = []
    if version >= 1:
        last_t = 0
        if version >= 2:
            last_x = 0
            last_y = 0
    is_first_in_stroke_part = True
    for point in stroke:
        if point['xs'] != 0 or point['ys'] != 0 or point['ts'] != 0:
            cur_t = point['ts'] - 1
            cur_x = point['xs']
            cur_y = point['ys']
            if version >= 1:
                cur_t += last_t
                last_t = cur_t
                if version >= 2:
                    if not is_first_in_stroke_part:
                        cur_x = last_x + sint_decode_from_uint(cur_x)
                        cur_y = last_y + sint_decode_from_uint(cur_y)
                    last_x = cur_x
                    last_y = cur_y
            cur_stroke.append({'x':cur_x-1, 'y':cur_y-1, 't':cur_t})
            is_first_in_stroke_part = False
        else:
            stroke_list.append(cur_stroke)
            cur_stroke = []
            is_first_in_stroke_part = True
    if cur_stroke:
        stroke_list.append(cur_stroke)
        cur_stroke = []
    if to_string:
        return '[' + ','.join('[' + ','.join("{'x':%(x)d,'y':%(y)d,'t':%(t)d}" % point for point in stroke_part) + ']' for stroke_part in stroke_list) + ']'
    else:
        if point_to_string:
            stroke_list = [[{'x':str(point['x']), 'y':str(point['y']), 't':str(point['t'])} for point in stroke] for stroke in stroke_list]
        return stroke_list

################################################################################
## Stroke conversion


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
                                   scale_factor=1, offset=None, tuple_to_dict=(lambda t: {'x':t[0], 'y':t[1]}),
                                   smooth=2, name=None, ctx=None, clear=True):
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
        os.system('echo "%s: Image size %s too small for stroke size %s.  Scale factor is %s." >> %s' % \
                  (name, size, (x_max, y_max), scale_factor, os.path.join(RESULTS_PATH, 'image_warnings.log')))
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
    if not ctx:
        ctx = cairo.Context(image)

    ctx.set_antialias(cairo.ANTIALIAS_NONE)

    if clear:
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
    is_empty = True
    for src, dest in paths:
        if verbose: print("I'm in %s" % src)
        strokes = list(glob(os.path.join(src, glob_name)))
        dest_images = [os.path.join(dest, os.path.splitext(os.path.split(file_name)[-1])[0] + new_ext) for file_name in strokes]
        if len(strokes) > 0: is_empty = False
        convert_strokes_to_images(strokes, dest_images, verbose=verbose, **kargs)
    if is_empty:
        print('Run %s --help for description and usage information.' % ' '.join(sys.argv))


parser = argparse.ArgumentParser(description="""Convert all strokes in a given directory to png files.

Strokes may be either compressed or uncompressed.

This script requires PIL, cairo, and argparse.""")

parser.add_argument('--src', '--source-directory', metavar='DIR', nargs='+', dest='src',
                    type=str, default='.',
                    help='the directories containing the input stroke files')
parser.add_argument('--dest', '--destination-directory', metavar='DIR', nargs='+', dest='dest',
                    type=str, default='.',
                    help='the directories to write converted image files to; if there is more than one, there must be one for each source directory')
parser.add_argument('--quiet', '-q', action='store_const', dest='verbose',
                    default=True, const=False,
                    help='causes status messages to not be shown')
parser.add_argument('--thickness', '--linewidth', dest='line_width',
                    type=float, default=5,
                    help='the thickness of the line in the new images')
parser.add_argument('--max-dimen', '--size', '-s', dest='new_max_dimen',
                    type=int, default=100,
                    help='the new maximum dimension of the image')

if __name__ == '__main__':
    args = parser.parse_args()
    convert_all_strokes_to_images(src=args.src, dest=args.dest, verbose=args.verbose, line_width=args.line_width, new_max_dimen=args.new_max_dimen)
