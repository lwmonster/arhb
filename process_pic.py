# coding:utf8

from PIL import Image
from math import fabs
import sys

if len(sys.argv) < 2:
    print "Usage: python %s image_file" % sys.argv[0]
    sys.exit(-1)

image_file = sys.argv[1]

im = Image.open(image_file)

mean_thr = 100
color_thr = 20

indice = []
'''
box = (0,10,im.size[0],30)
cut = im.crop(box)
cut.show()
'''
cut = im.convert('RGB')

for i in range(cut.size[1]):
    # red yellow blue mean
    r_mean = 0
    y_mean = 0
    b_mean = 0 

    # Standard deviation
    r_sd = 0
    y_sd = 0
    b_sd = 0
    
    for j in range(cut.size[0]):
        p = cut.getpixel((j,i))
        r_mean += p[0]
        y_mean += p[1]
        b_mean += p[2]
        #print p,
    ## calc mean
    r_mean = 1.0*r_mean / cut.size[0]
    y_mean = 1.0*y_mean / cut.size[0]
    b_mean = 1.0*b_mean / cut.size[0]
    ## calc sd
    for j in range(cut.size[0]):
        p = cut.getpixel((j,i))
        r_sd += fabs(p[0] - r_mean) 
        y_sd += fabs(p[1] - y_mean) 
        b_sd += fabs(p[2] - b_mean) 
    
    r_sd = 1.0*r_sd / cut.size[0]
    y_sd = 1.0*y_sd / cut.size[0]
    b_sd = 1.0*b_sd / cut.size[0]
    
    if r_sd < color_thr and y_sd < color_thr and b_sd < color_thr and r_mean < mean_thr and y_mean < mean_thr and b_mean < mean_thr:
        if len(indice) > 0 and indice[-1][-1] == i - 1:
            indice[-1].append(i)
        else:
            indice.append([i])

    print "r_mean:%f y_mean:%f b_mean:%f r_sd:%f y_sd:%f b_sd:%f" % (r_mean, y_mean, b_mean, r_sd, y_sd, b_sd)
    print indice


for cluster in indice:
    start = cluster[0] - 1
    end = cluster[-1] + 1
    if start - 2 < 0 or end + 2 > cut.size[1] - 1:
        continue
    
    for i in range(cut.size[0]):
        s_pixel = cut.getpixel((i, start-1))
        e_pixel = cut.getpixel((i, end + 1))
        
        r_epoch = (e_pixel[0] - s_pixel[0]) / (len(cluster) + 2)
        y_epoch = (e_pixel[1] - s_pixel[1]) / (len(cluster) + 2)
        b_epoch = (e_pixel[2] - s_pixel[2]) / (len(cluster) + 2)

        for j in range(start, end + 1):
            r_value = s_pixel[0] + r_epoch * (j - start + 1)
            y_value = s_pixel[1] + y_epoch * (j - start + 1)
            b_value = s_pixel[2] + b_epoch * (j - start + 1)
            cut.putpixel((i,j), (r_value, y_value, b_value))


cut.show()


