#!/usr/bin/python
import argparse
from htmlcanvas import convert_all_alphabet_strokes_to_images

parser = argparse.ArgumentParser(description='Convert stokes from all of the accepted alphabets to png files')
parser.add_argument('--thickness', '--linewidth', dest='line_width',
                    type=float, default=5,
                    help='the thickness of the line in the new images')
parser.add_argument('--max-dimen', '--size', '-s', dest='new_max_dimen',
                    type=int, default=100,
                    help='the new maximum dimension of the image')
parser.add_argument('--quiet', '-q', action='store_const', dest='verbose',
                    default=True, const=False,
                    help='causes status messages to not be shown')

if __name__ == '__main__':
    args = parser.parse_args()
    convert_all_alphabet_strokes_to_images(line_width=args.line_width, new_max_dimen=args.new_max_dimen,
                                           verbose=args.verbose)
