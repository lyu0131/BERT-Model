# Todo @
# -------------------------------- parser ---------------------------------------
import argparse
my_parser = argparse.ArgumentParser()

my_parser.add_argument('--input_dir',type=str, default='./data/', help='the path to the folder containing jpg,png,svg')
my_parser.add_argument('--output_dir',type=str, default='./image/', help='the path to store the image foler')

args = my_parser.parse_args()

input_dir = args.input_dir
output_dir = args.output_dir
#/usr0/home/siyaol/quizlet7/png/L0C04FOSH.png
# ------------------------------- convert func ------------------------------------
from PIL import Image
def PNGToJPG(path,outpath):
    im = Image.open(path)
    bg = Image.new("RGB", im.size, (255,255,255))
    try:
        bg.paste(im,im)
    except ValueError:
        bg.paste(im)
    bg.save(outpath)
# PNGToJPG("png/K0C03N6VE.png","colors.jpg")

from cairosvg import svg2png
def SVGToPNG(path,outpath):
    svg_code = open(path, 'rt').read()
    svg2png(bytestring=svg_code,write_to=outpath)
# SVGToJPG("svg/L0C04FKLN.svg","colors.png")

def GIFToJPG(infile,outpath):
    image = Image.open(infile)

    frames = []

    disposal_method_last = 0

    try:
        while True:
            disposal_method = disposal_method_last
            disposal_method_last = image.__dict__.get('disposal_method', 0)
            if disposal_method == 2 or (disposal_method == 1 and frames == []):
                frame = Image.new('RGBA', image.size, color=(255,0,0,0))
                frame.paste(image.crop(image.dispose_extent), box=(image.dispose_extent[0],image.dispose_extent[1]))
            elif disposal_method == 1:
                newStuff = image.crop(image.dispose_extent)
                frame = frames[-1].copy()
                frame.paste(newStuff, image.dispose_extent, newStuff.convert("RGBA"))
            else:
                frame = image.copy()
            frames.append(frame)
            image.seek(image.tell() + 1)
    except EOFError:
        pass

    for i in range(len(frames)):
        im = frames[i].convert(mode='RGBA')
        bg = Image.new("RGB", im.size, (255,255,255))
        try:
            bg.paste(im,im)
        except ValueError:
            bg.paste(im)
        bg.save(outpath + f'{i+1:06d}' + '.jpg')  
        
    with open(outpath + 'frame_indices.txt', 'w') as f:
        for i in range(len(frames)):
            if i == len(frames) - 1:
                f.write(str(i+1))
            else:
                f.write(str(i+1) + '\n')
# GIFToJPG('gif/L0C04FOSG.gif', 'gif/')

# -------------------------------- main() ---------------------------------------
import os
if not os.path.exists(output_dir): os.makedirs(output_dir)
gifs = [f for f in os.listdir(input_dir+'gif') if f[0] != '.']
for gif in gifs:
    output_dir_gif = output_dir + gif[:-4] + '/'
    if not os.path.exists(output_dir_gif): os.makedirs(output_dir_gif)
    GIFToJPG(input_dir + 'gif/' + gif, output_dir_gif)

pngs = [f for f in os.listdir(input_dir+'png') if f[0] != '.']
for png in pngs:
    output_dir_png = output_dir + png[:-4] + '/'
    if not os.path.exists(output_dir_png): os.makedirs(output_dir_png)
    PNGToJPG(input_dir + 'png/' + png, output_dir_png+'000001.jpg')

svgs = [f for f in os.listdir(input_dir+'svg') if f[0] != '.']
svgpngs = []
for svg in svgs:
    output_dir_svg = output_dir + svg[:-4] + '/'
    if not os.path.exists(output_dir_svg): os.makedirs(output_dir_svg)
    SVGToPNG(input_dir + 'svg/' + svg, output_dir_svg+'000001.png')
    svgpngs.append(output_dir_svg+'000001.png')
for png in svgpngs:
    PNGToJPG(png, png[:-4] + ".jpg")
    os.remove(png)


import shutil
jpgs = [f for f in os.listdir(input_dir+'jpg') if f[0] != '.']
for jpg in jpgs:
    output_dir_jpg = output_dir + jpg.split('.')[0] + '/'
    if not os.path.exists(output_dir_jpg): os.makedirs(output_dir_jpg)
    shutil.copyfile(input_dir + 'jpg/' + jpg,output_dir_jpg+'000001.jpg')

