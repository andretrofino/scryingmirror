import cv2
import numpy as np
import scipy.fftpack
import os
from imagehash import *

crop_x = 18
crop_width = 204
crop_y = 36
crop_height = 172


def hamming(x, y, base=2):
    'Calculates the hamming distance'
    count = 0
    z = int(x, base) ^ int(y, base)
    while z:
        count += 1
        z &= z - 1  # magic!

    return count


def dct_hash(image, resize=32, block_size=8, crop=True, dct_type=2):
    '''
    Calculates the image hash
    First it calculates the dct over the image, then the mean value of the top left block.
    The hash is create by checking if each value of the top left block is
    above or below the overall mean.
    '''
    if type(image) is str:
        image = cv2.imread(image)

    if crop:
        image = image[crop_y:crop_height, crop_x:crop_width]

    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    image = cv2.resize(image, (resize, resize)).astype('float')

    dct = scipy.fftpack.dct(scipy.fftpack.dct(image, axis=0, type=dct_type), axis=1, type=dct_type)
    top_dct = dct[:block_size, :block_size]

    total_block_size = block_size * block_size
    # Average of the DCT, ignoring the first value
    mean = ((top_dct.mean() * total_block_size) - top_dct[0][0]) / (total_block_size - 1)

    top_dct[0][0] = mean
    image_hash = top_dct > mean

    return ImageHash(image_hash)


def block_dct_hash(image, resize=32, top_left=8, crop=True, dct_type=3):
    if type(image) is str:
        image = cv2.imread(image)

    if crop:
        image = image[crop_y:crop_height, crop_x:crop_width]

    if len(image.shape) > 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    image = cv2.resize(image, (resize, resize)).astype('float')

    dct = scipy.fftpack.dct(scipy.fftpack.dct(image, axis=0, type=dct_type), axis=1, type=dct_type)

    size = resize * resize

    overall_mean = ((dct.mean() * size) - dct[0][0]) / (size - 1)

    n_blocks = resize / top_left
    block_size = top_left * top_left

    hash_array = np.zeros((top_left, top_left), dtype=np.bool)

    for y in xrange(n_blocks):
        for x in xrange(n_blocks):
            block = image[y * top_left:(y + 1) * top_left, x * top_left:(x + 1) * top_left]
            block_dct = scipy.fftpack.dct(scipy.fftpack.dct(block, axis=0, type=3), axis=1, type=3)

            block_mean = ((block_dct.mean() * block_size) - block_dct[0][0]) / (block_size - 1)

            if block_mean > overall_mean:
                hash_array[y, x] = True
            else:
                hash_array[y, x] = False

    return ImageHash(hash_array)


def save_hash(save_path, hash_list, name_list, overwrite=True):
    if overwrite:
        fd = open(save_path, 'w')
    else:
        fd = open(save_path, 'a+')
    for name, hash_value in zip(name_list, hash_list):
        fd.write(name + ':' + str(hash_value) + '\n')
    fd.close()


def hash_dir(dir_path, save_path, crop=True, overwrite=True):
    images = []
    for (dirpath, dirnames, filenames) in os.walk(dir_path):
        images.extend(filenames)
        break

    images = [name for name in images if name.endswith("jpg")]  # Skip non-image files

    # Assumes that the file name is the correct card name
    name_list = [name[:name.index('.')] for name in images]

    hash_list = [0] * len(images)

    index = 0
    for image_path in images:
        image = cv2.imread(os.path.join(dir_path, image_path))
        image_hash = dct_hash(image, crop=crop)
        hash_list[index] = image_hash
        index += 1

    if save_path is not None:
        save_hash(save_path, hash_list, name_list, overwrite)

    return hash_list, name_list


def match(target_hash, hash_list, top=5):
    scores = [target_hash - hash_value for hash_value in hash_list]
    index = [i for i in xrange(len(scores))]

    scores, index = [list(x) for x in zip(*sorted(zip(scores, index), key=lambda pair: pair[0]))]

    return scores[:top], index[:top]


def load_hash(hash_path):
    fd = open(hash_path, 'r')
    lines = fd.readlines()

    hash_list = [line[line.find(':')+1:].strip('\n') for line in lines]
    name_list = [line[0:line.find(':')].strip('\n') for line in lines]

    return hash_list, name_list


def main():
    hash_path = 'ema_ogw_dct.hash'
    img = 'Images/seer_crop.jpg'

    img_hash = dct_hash(img, crop=False)
    str_hash_list, name_list = load_hash(hash_path)
    hash_list = [hex_to_hash(value) for value in str_hash_list]

    scores, index_list = match(img_hash, hash_list)

    for score, index in zip(scores, index_list):
        print name_list[index] + ' : ' + str(score)


def dct_test():

    img = cv2.imread('Images/Eternal Masters/Wasteland.jpg')
    img = img[crop_y:crop_height, crop_x:crop_width]

    test = dct_hash(img)

    print test

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = cv2.resize(img, (32, 32)).astype('float')

    dct = scipy.fftpack.dct(scipy.fftpack.dct(img, axis=0), axis=1)

    dct_img = scipy.fftpack.dct(img, axis=0)

    dct_img = scipy.fftpack.dct(dct_img, axis=1)

    print dct_img


if __name__ == "__main__":
    dct_test()
