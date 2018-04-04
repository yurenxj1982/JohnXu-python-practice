#! /usr/bin/env python3
# -*- coding: utf-8 -*-

r'''
这是一个图片转字符画的练习
问题描述：
    1) 程序的使用方法:
    $ image-to-text  [-h | --help] [--scale scale] [--char-set "char_set"] image
        -h                     show this
            --scale            scale to scale px
            --char-set         the transform character set
                               default is "$@B%8&WM#*oahkbdpqwm
                               ZO0QLCJUYXzcvunxrjft/\|()1{}
                               []?-_+~<>i!lI;:,\"^`'."

        image                  image file
目的:
    熟悉pillow(PIL)库

'''

__author__ = 'xujun'

from PIL import Image

def usage(name):

    ''' print usage '''

    helpstr = '''usage:
{0}  [-h | --help] [--scale scale] [--char-set "char_set"] image...
        -h  --help             show this
            --scale            scale to scale px
            --char-set         the transform character set
                               default is " $@B%8&WM#*oahkbdpqwm
                               ZO0QLCJUYXzcvunxrjft/\\|()1{}
                               []?-_+~<>i!lI;:,\"^`'."

        image...               image files
    '''.format(name)
    print(helpstr)


class TextImageConvertor(object):
    r'''
    TextImageConvertor
    '''

    def __init__(self):
        self._scale = -1
        self._gray_str = " $@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'."
        self._r_coeffficient = 0.229
        self._g_coeffficient = 0.587
        self._b_coeffficient = 0.114


    @property
    def scale(self):
        '''
        scale
        '''
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale


    @property
    def gray_string(self):
        '''
        gray string
        '''
        return self._gray_str

    @gray_string.setter
    def gray_string(self, string):
        self._gray_str = string

    def _convert_L(self, L):
        r'''
            trans gray L to char
        '''
        return self._gray_str[int(L / 256 * len(self._gray_str))]


    def _rgba_to_L(self, r, g, b, alpha=256):
        r'''
            trans rgba to level
        '''
        if alpha == 0:
            return 0
        gray = self._r_coeffficient * r  + self._g_coeffficient * g + self._b_coeffficient * b

        return gray


    def _convert(self, image, pixel_convert_l_func):
        buf = []
        width, height = image.size
        for y in range(height):
            for x in range(width):
                data = image.getpixel((x, y))
                pixel_l = pixel_convert_l_func(data)
                buf.append(self._convert_L(pixel_l))
            buf.append('\n')

        return buf


    def convert(self, image):
        r'''
            convert image to string
        '''
        buf = []
        op_im = image.copy()
        if self._scale > 0:
            op_im.thumbnail((self._scale, self._scale))

        if op_im.mode == "RGBA":
            buf = self._convert(op_im, lambda rgba: self._rgba_to_L(rgba[0], rgba[1], rgba[2], rgba[3]))
        elif op_im.mode == "RGB":
            buf = self._convert(op_im, lambda rgb:  self._rgba_to_L(rgb[0], rgb[1], rgb[2]))
        elif op_im.mode == "LA":
            buf = self._convert(op_im, lambda la:   la[0])
        elif op_im.mode == "L":
            buf = self._convert(op_im, lambda l:    l[0])
        else:
            pass


        return "".join(buf)



if __name__ == '__main__':
    import sys
    import os
    import getopt
    dirname, filename = os.path.split(sys.argv[0])

    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "h", ["help", "char-set=", "scale="])
    except getopt.GetoptError as err:
        print(err)
        usage(filename)
        sys.exit(2)

    textConvertor = TextImageConvertor()

    for o, a in opts:
        if o in ('-h', '--help'):
            usage(filename)
            sys.exit()
        elif o == '--char-set':
            textConvertor.gray_string = a
        elif o == '--scale':
            textConvertor.scale = int(a)


    for image_file in args:
        with Image.open(image_file) as im:
            print(textConvertor.convert(im))
