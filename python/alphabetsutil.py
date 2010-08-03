#!/usr/bin/python
# Filename: alphabetsutil.py
from __future__ import with_statement
from alphabetspaths import *
import math
import os, sys
import base64
try:
    from htmlcanvas import *
except ImportError:
    pass

def png_to_uri(name):
    with open(name, 'rb') as f:
        png = f.read()
    return 'data:image/png;base64,' + base64.b64encode(png)

def compress_images(folder=None, image_list=None, image_magick=True, big_size=2000):
    submission_log_path = SUBMISSION_LOG_PATH
    mogrify_path = MOGRIFY_PATH
    if folder: push_dir(folder)
    if not image_list: image_list = [image for image in sorted(os.listdir(os.getcwd())) if image[-4:].lower() == '.png']
##    print('<br>%s<br>' % os.getcwd())
##    print(MOGRIFY_PATH + ' -background "#FFFFFF" -flatten *.png<br>') # because if I use white, it gives lt-mogrify: UnableToOpenConfigureFile `colors.xml' @ warning/configure.c/GetConfigureOptions/589.
##    print(MOGRIFY_PATH + ' -threshold 50% *.png<br>')
    image_list_str = ' '.join(image_list)
    if image_magick:
        os.system('%(mogrify_path)s -background "#FFFFFF" -flatten %(image_list_str)s >> %(submission_log_path)s' % locals()) # because if I use white, it gives lt-mogrify: UnableToOpenConfigureFile `colors.xml' @ warning/configure.c/GetConfigureOptions/589.
        os.system('%(mogrify_path)s -threshold 50%% %(image_list_str)s >> %(submission_log_path)s' % locals())
##    else:
##        image_list_xbm_str = image_list_str.replace('.png', '.xbm')
##        os.system('mogrify -format xbm %(image_list_str)s > %(submission_log_path)s' % locals()) # because if I use white, it gives lt-mogrify: UnableToOpenConfigureFile `colors.xml' @ warning/configure.c/GetConfigureOptions/589.
##        os.system('mogrify -format png %(image_list_xbm_str)s >> %(submission_log_path)s' % locals())
##        os.system('rm %(image_list_xbm_str)s >> %(submission_log_path)s' % locals())
    for image in image_list:
        if not image_magick:
##            image_pbm = image.replace('.png', '.pbm')
            os.system('convert %(image)s -size %(big_size)s xc:white %(image)s -flatten -threshold 50%% %(image)s >> %(submission_log_path)s' % locals())
            os.system('convert %(image)s -size %(big_size)s xc:white %(image)s -flatten -threshold 50%% %(image)s >> %(submission_log_path)s' % locals())
        for params in ('',):# '-c0 -f0', '-c0 -f5', '-c3 -f0', '-c3 -f5'):
##            print('<br>before: %d - %s %s -v "%s"<br>' % (os.path.getsize(image), PNGOUT_PATH, params, image))
            os.system(('%s %s -v "%s" >> ' + SUBMISSION_LOG_PATH) % (PNGOUT_PATH, params, image))
    if folder: pop_dir()

##        for x_len in (1,2,3):
##            if x_len != 1: print 'elif',
##            else: print 'if',
##            print 'point[' + str(4 + x_len) + "] == ',':"
##            for y_len in (1,2,3):
##		if y_len != 1: print '    elif',
##		else: print '    if',
##		print 'point[' + str(4 + x_len + 1 + 4 + y_len) + "] == ',':"
##		print "        stroke[point_i] = {'x':point[4:" + str(4 + x_len) + "], 'y':point[" + str(4 + 4 + x_len + 1) + ':' + str(4 + x_len + 4 + y_len + 1) + "], 't':point[" + str(4 + x_len + 4 + y_len + 2 + 4) + ':]}'

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
                if last_t > int(point['t']): return compress_stroke(stroke, version=0, safe=safe)
                if version >= 2 and last_t == int(point['t']) and last_t > 0: return compress_stroke(stroke, version=1, safe=safe)
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
            bits[key] = int(1 + math.floor(math.log(maxes[key]) / math.log(2)))

    
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
            bits[key] = int(1 + math.floor(math.log(maxes[key]) / math.log(2)))
        if bits['xs'] + bits['ys'] <= 8: return compress_stroke(stroke, version=1, safe=safe)
            
                
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
                    stroke_bits[key] = int(1 + math.floor(math.log(stroke_maxes[key]) / math.log(2)))
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
    
        
def get_stroke(file_name, uncompressed_ext='.stroke', compressed_ext='.cstroke', parsed=True, parsed_to_int=None):
    do_uncompressed = file_name[-len(uncompressed_ext):] == uncompressed_ext
    do_compressed = file_name[-len(compressed_ext):] == compressed_ext
    if not (do_uncompressed ^ do_compressed):
        with open(file_name, 'rb') as f:
            rtn = f.read()
            if not isinstance(rtn[0], str):
                rtn = ''.join(map(chr, rtn))
            if rtn[:3] == '[[{':
                do_uncompressed = True
                do_compressed = not do_uncompressed
            if not (do_uncompressed ^ do_compressed):
                raise ValueError('Invalid stroke format.')
    if do_uncompressed:
        with open(file_name, 'r') as f:
            rtn = f.read()
        if parsed:
            if parsed_to_int is not None:
                return stroke_to_list(rtn, parsed_to_int=parsed_to_int)
            else:
                return stroke_to_list(rtn)
        else:
            return rtn
    else:
        with open(file_name, 'rb') as f:
            rtn = f.read()
        if parsed_to_int is not None:
            return decompress_stroke(rtn, to_string=(not parsed), point_to_string=(not parsed_to_int))
        else:
            return decompress_stroke(rtn, to_string=(not parsed))
        
