import random
import skimage.transform
import skimage
from glob import glob
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import tensorflow.compat.v1 as tf
import os
import cv2
import numpy as np
tf.disable_v2_behavior()

sess = tf.Session()
all_images_cropped = '../../UND 2D cropped face data/cropped_data/*.ppm'



def crop_img(img):
    original_size = list(img.shape)
    x = img
    """crop_size = [int(0.8*original_size[0]),
                 int(0.5*original_size[1]), original_size[2]]"""
    x = tf.image.central_crop(x, 0.95)
    output = tf.image.resize_images(
        x, size=[original_size[0], original_size[1]])
    tf.cast(output, dtype=tf.uint8)
    return output


def rotate_img(img):
    #rot = skimage.transform.rotate(img, angle = random.randint(1,5), mode='constant', cval=1)
    rot = skimage.transform.rotate(
        img, angle=random.randint(1, 5), mode='reflect')
    return rot

def noise_img(img):
    original_size = list(img.shape)
    x = img
    #tf.cast(x, dtype=tf.float32)
    noise = tf.random_normal(shape=original_size, mean=0.0, stddev=1.0, dtype=tf.float32)
    output = tf.add(x, noise)
    tf.cast(output, dtype=tf.uint8)
    return output


sess.run(tf.initialize_all_variables())

def DA_handler(path,folder):
    img_names = glob(path)
    print("Total number of images = ",len(img_names))
    os.makedirs(folder,exist_ok=True)
    #img_num=0
    for fn in img_names:
        #img_num=img_num+1
        #img = cv2.imread(fn)
        #img = load_img(fn)
        #img = np.array(img)
        img = load_img(fn)
        # print(img.shape)
        img = img_to_array(img)
        #cv2.imshow('img',img)
        #images.append(img)
        name = fn.split("/")[-1]
        cropped = crop_img(img)
        cropped = 255*(cropped-tf.math.reduce_min(cropped))/(tf.math.reduce_max(cropped)-tf.math.reduce_min(cropped))
        cropped = tf.cast(cropped, dtype=tf.uint8)
        cropped_img = tf.image.encode_jpeg(cropped)
        crop_write = tf.write_file(folder+'/'+name.replace('.ppm', '_cropped.ppm'), cropped_img)
        rotated = rotate_img(img)
        rotated = 255*(rotated-tf.math.reduce_min(rotated))/(tf.math.reduce_max(rotated)-tf.math.reduce_min(rotated))
        rotated = tf.cast(rotated, dtype=tf.uint8)
        rotated_img = tf.image.encode_jpeg(rotated)
        rotate_write = tf.write_file(folder+'/'+name.replace('.ppm', '_rotated.ppm'), rotated_img)
        noised = noise_img(img)
        noised = 255*(noised-tf.math.reduce_min(noised))/(tf.math.reduce_max(noised)-tf.math.reduce_min(noised))
        noised = tf.cast(noised, dtype=tf.uint8)
        noised_img = tf.image.encode_jpeg(noised)
        noise_write = tf.write_file(folder+'/'+name.replace('.ppm', '_noise.ppm'), noised_img)
        sess.run(crop_write)
        sess.run(rotate_write)
        sess.run(noise_write)
    return

DA_handler(all_images_cropped,'../../UND 2D cropped face data/cropped_data_DA')

print('done')