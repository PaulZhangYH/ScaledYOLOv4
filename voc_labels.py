import os
import json
import numpy as np
from os import listdir, getcwd
sets = ['train', 'test', 'val']
classes = ["palm"]

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)
def convert_annotation(image_id):
    """
    TO DO !!! 根据json文本更改下述代码 label格式: 0 x, y, w, h
    :param image_id:
    :return:
    """
    in_file = open('data/Annotations/%s.json' % (image_id), 'r')
    json_file = json.load(in_file)
    out_file = open('data/labels/%s.txt' % (image_id), 'w')

    if 'points' in json_file:
        coord = json_file['points']
        x_min, y_min, x_max, y_max = int(coord[0][0]), int(coord[0][1]), int(coord[1][0]), int(coord[1][1])
        width = np.abs(x_max - x_min)
        height = np.abs(y_max - y_min)
        txt_file_content = '0' + ' ' + str(x_min) + ' ' + str(y_min) + ' ' + str(width) + ' ' + str(height)

        out_file.write(txt_file_content)
        out_file.write('\n')

    elif 'hands_cord' in json_file:
        info = json_file['hands_cord']
        num_hand = len(info)
        all_txt_file_content = ''
        for i in range(num_hand):
            x_min, y_min, x_max, y_max = info[i]
            width = np.abs(x_max - x_min)
            height = np.abs(y_max - y_min)

            json_file_content = '0' + ' ' + str(x_min) + ' ' + str(y_min) + ' ' + str(width) + ' ' + str(height) + '\n'
            all_txt_file_content += json_file_content
        out_file.write(all_txt_file_content)

    else:
        info = json_file['shapes']
        if len(info) == 1:
            points = info[0]['points']
            x_min, y_min, x_max, y_max = int(points[0][0]), int(points[0][1]), int(points[1][0]), int(points[1][1])
            width = np.abs(x_max - x_min)
            height = np.abs(y_max - y_min)
            txt_file_content = '0' + ' ' + str(x_min) + ' ' + str(y_min) + ' ' + str(width) + ' ' + str(height)

            out_file.write(txt_file_content)
            out_file.write('\n')
        if len(info) == 2:
            points_1 = info[0]['points']
            points_2 = info[1]['points']
            if len(points_1) == 2 and len(points_2) == 2:
                x1_min, y1_min, x1_max, y1_max = int(points_1[0][0]), int(points_1[0][1]), int(points_1[1][0]), int(
                    points_1[1][1])
                width1 = np.abs(x1_max - x1_min)
                height1 = np.abs(y1_max - y1_min)

                x2_min, y2_min, x2_max, y2_max = int(points_2[0][0]), int(points_2[0][1]), int(points_2[1][0]), int(
                    points_2[1][1])
                width2 = np.abs(x2_max - x2_min)
                height2 = np.abs(y2_max - y2_min)

                txt_file_content = '0' + ' '  + str(x1_min) + ' ' + str(y1_min) \
                                   + ' ' + str(width1) + ' ' + str(height1) + '\n' \
                                   '0' + ' ' + str(x2_min) + ' ' + str(y2_min) \
                                   + ' ' + str(width2) + ' ' + str(height2)
                out_file.write(txt_file_content)
                out_file.write('\n')



wd = getcwd()
print(wd)

for image_set in sets:
    if not os.path.exists('data/labels/'):
        os.makedirs('data/labels/')
    image_ids = open('data/ImageSets/%s.txt' % (image_set)).read().strip().split()
    list_file = open('data/%s.txt' % (image_set), 'w')
    for image_id in image_ids:
        list_file.write('data/ImageSets/%s.jpg\n' % (image_id))
        convert_annotation(image_id)
    list_file.close()
