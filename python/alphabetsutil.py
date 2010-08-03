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
    if number > 0:
        return uint_encode(2 * number - 1, total_bytes=total_bytes)
    else:
        return uint_encode(-2 * number, total_bytes=total_bytes)

def sint_decode(number):
    rtn = uint_decode(number)
    if rtn % 2 == 0:
        return -rtn / 2
    else:
        return (rtn + 1) / 2

def compress_stroke(stroke, version=1, safe=True):
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

        bits[key] = int(1 + math.floor(math.log(maxes[key]) / math.log(2)))
    points = []
    for stroke_i in range(len(stroke_list)):
        points += [(strokes['xs'][stroke_i][point_i], strokes['ys'][stroke_i][point_i], strokes['ts'][stroke_i][point_i])
                   for point_i in range(len(stroke_list[stroke_i]))]
        points.append((0, 0, 0))
    points = points[:-1]

    if bits['xs'] + bits['ys'] <= 8:
        first_line = str(version) + '\x00' + chr(bits['xs']) + '\x00' + chr(bits['ys'])
        points = [(chr(point[0] + (point[1] << bits['xs'])), point[2]) for point in points]
    elif bits['xs'] <= 8 and bits['ys'] <= 8:
        first_line = str(version) + '\x00' + chr(bits['xs']) + '\x00' + chr(bits['ys'])
        points = [(chr(point[0]) + chr(point[1]), point[2]) for point in points]
    else:
        if bits['xs'] <= 8:
            first_line = str(version) + '\x00' + chr(bits['xs'])
            points = [(chr(point[0]), point[1], point[2]) for point in points]
        else:
            if bits['xs'] < BIG_BYTE_PLUS_ONE:
                first_line = str(version) + '\x00u' + chr(bits['xs'])
            else:
                first_line = str(version) + '\x00ul' + str(bits['xs'])
            total_bytes = int(1 + (bits['xs'] - 1) / 8)
            points = [(uint_encode(point[0], total_bytes=total_bytes), point[1], point[2]) for point in points]
        
        if bits['ys'] <= 8:
            first_line += '\x00' + chr(bits['ys'])
            points = [(point[0] + chr(point[1]), point[2]) for point in points]
        else:
            if bits['ys'] < BIG_BYTE_PLUS_ONE:
                first_line += '\x00u' + chr(bits['ys'])
            else:
                first_line += '\x00ul' + str(bits['ys'])
            total_bytes = int(1 + (bits['ys'] - 1) / 8)
            points = [(point[0] + uint_encode(point[1], total_bytes=total_bytes), point[2]) for point in points]
    if bits['ts'] <= 8:
        first_line += '\x00' + chr(bits['ts'])
        points = [point[0] + chr(point[1]) for point in points]
    else:
        if bits['ts'] < BIG_BYTE_PLUS_ONE:
            first_line += '\x00u' + chr(bits['ts'])
        else:
            first_line += '\x00ul' + str(bits['ts'])
        total_bytes = int(1 + (bits['ts'] - 1) / 8)
        points = [point[0] + uint_encode(point[1], total_bytes=total_bytes) for point in points]

    first_line += '\x00'
    return first_line + ''.join(points)

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

        stroke.append(point)

    stroke_list = []
    cur_stroke = []
    if version >= 1:
        last_t = 0
    for point in stroke:
        if point['xs'] != 0 or point['ys'] != 0 or point['ts'] != 0:
            cur_t = point['ts']-1
            if version >= 1:
                cur_t += last_t
                last_t = cur_t
            cur_stroke.append({'x':point['xs']-1, 'y':point['ys']-1, 't':cur_t})
        else:
            stroke_list.append(cur_stroke)
            cur_stroke = []
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
        

