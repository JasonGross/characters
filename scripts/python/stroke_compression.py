#!/usr/bin/python
# Filename: stroke_compression.py
from __future__ import with_statement
import os
from alphabetsutil import decompress_stroke, compress_stroke, stroke_to_list

def compress_all_strokes_in_current_directory(uncompressed_ext='.stroke', compressed_ext='.cstroke', remove_old=True, verbose=True, show_compression=True):
    for base, dirs, files in os.walk(os.getcwd()):
        if verbose: print("I'm in " + base)
        for file_name in files:
            if file_name[-len(uncompressed_ext):] == uncompressed_ext:
                if not show_compression: print('Compressing %s...' % file_name)
                with open(os.path.join(base, file_name), 'rb') as f:
                    stroke = f.read()
                new_stroke = compress_stroke(stroke)
                with open(os.path.join(base, file_name.replace(uncompressed_ext, compressed_ext)), 'wb') as f:
                    f.write(new_stroke)
                if show_compression: print('Compressed %s at\t\t%.2f%%' % (file_name, 100.0 * len(new_stroke) / len(stroke)))
                if remove_old:
                    os.rename(os.path.join(base, file_name), os.path.join(base, file_name + '.bak'))
                    # Testing to make sure that we can actually decompress the new file correctly before deleting the old file
                    with open(os.path.join(base, file_name + '.bak'), 'rb') as f:
                        old_stroke = f.read()
                    with open(os.path.join(base, file_name.replace(uncompressed_ext, compressed_ext)), 'rb') as f:
                        new_stroke = f.read()
                    new_old_stroke = decompress_stroke(new_stroke)
                    if new_old_stroke.strip() != old_stroke.strip() and stroke_to_list(new_old_stroke) != stroke_to_list(old_stroke):
                        os.rename(os.path.join(base, file_name + '.bak'), os.path.join(base, file_name))
                        os.remove(os.path.join(base, file_name.replace(uncompressed_ext, compressed_ext)))
                        print('Error on stroke %s in %s' % (file_name, base))
                        print('I wanted:')
                        print(stroke_to_list(old_stroke))
                        print('I got:')
                        print(stroke_to_list(new_old_stroke))
                        print('The compressed version is:')
                        print(repr(new_stroke))
                        raw_input('Press enter or ^C')
                    else:
                        os.remove(os.path.join(base, file_name + '.bak'))


def decompress_all_strokes_in_current_directory(uncompressed_ext='.stroke', compressed_ext='.cstroke', remove_old=True, verbose=True, show_compression=True):
    for base, dirs, files in os.walk(os.getcwd()):
        if verbose: print("I'm in " + base)
        for file_name in files:
            if file_name[-len(compressed_ext):] == compressed_ext:
                if not show_compression: print('Decompressing %s...' % file_name)
                with open(os.path.join(base, file_name), 'rb') as f:
                    stroke = f.read()
                new_stroke = decompress_stroke(stroke)
                with open(os.path.join(base, file_name.replace(compressed_ext, uncompressed_ext)), 'wb') as f:
                    f.write(new_stroke)
                if show_compression: print('Decompressed %s at\t\t%.2f%%' % (file_name, 100.0 * len(stroke) / len(new_stroke)))
                
                if remove_old:
                    os.rename(os.path.join(base, file_name), os.path.join(base, file_name + '.bak'))
                    # Testing to make sure that we can actually decompress the new file correctly before deleting the old file
                    with open(os.path.join(base, file_name + '.bak'), 'rb') as f:
                        old_stroke = f.read()
                    with open(os.path.join(base, file_name.replace(compressed_ext, uncompressed_ext)), 'rb') as f:
                        new_stroke = f.read()
                    new_old_stroke = compress_stroke(new_stroke)
                    if new_old_stroke != old_stroke and stroke_to_list(new_old_stroke) != stroke_to_list(old_stroke):
                        os.rename(os.path.join(base, file_name + '.bak'), os.path.join(base, file_name))
                        os.remove(os.path.join(base, file_name.replace(uncompressed_ext, compressed_ext)))
                        print('Error on stroke %s in %s' % (file_name, base))
                        print('I wanted:')
                        print(repr(old_stroke))
                        print('I got:')
                        print(repr(new_old_stroke))
                        print('The uncompressed version is:')
                        print(new_stroke)
                        raw_input('Press enter or ^C')
                    else:
                        os.remove(os.path.join(base, file_name + '.bak'))



                    
if __name__ == '__main__':
    os.system('python make-stroke-compression.py')
