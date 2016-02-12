from __future__ import print_function

import numpy as np
import cv2
import sys
import os
import glob

def print_next_letter(letters, rectangles):
    if len(rectangles)<len(letters):
        print("Draw a box around:",letters[len(rectangles)], [letters[len(rectangles)]])
    else:
        print("Seems we are finished, press 's' to save and 'n' for next image")

def drawRectangles(img, rectangles):
    for cnt, (x1, y1, x2, y2) in enumerate(rectangles):
        cv2.rectangle(img, (x1, y1-offset), (x2, y2-offset), BLUE, 1)
        #cv2.putText(img, str(cnt), (x2, y2+2), cv2.FONT_HERSHEY_SIMPLEX, 1, 1)

BLUE = [255,0,0]        # rectangle color
ix, iy = -1, -1
rectangles = []
letters = []
offset = 0 

def onmouse(event, x, y, flags, param):
    global rectangles, ix, iy, img, letters, offset
    # Draw Rectangle
    y=y+3+offset
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Set {} {}".format(x, y))
        rectangle = True
        if ix<0 and iy<0:
            ix,iy = x,y
        else:
            rectangles.append((min(ix, x), min(iy, y), max(ix, x), max(iy,y)))
            drawRectangles(img, rectangles)
            cv2.imshow('input',img)
            print_next_letter(letters, rectangles)
            ix, iy = -1, -1

def load_box(box_filename):
    print(box_filename)
    rectangles = []
    if os.path.exists(box_filename):
        try:
            with open(box_filename) as f:
                split = f.read().split('\n')
                print(split)
                rectangles = [map(int, x.split(' ')) for x in split[:-1]]
        except Exception as e:
            print("Couldn't load boxfile: {}".format(e))
    return rectangles

def load_letters(letter_filename):
    print(letter_filename)
    rectangles = []
    if os.path.exists(letter_filename):
        try:
            with open(letter_filename) as f:
                split = f.read().decode('utf-8').replace('\n', '').replace(' ', '').replace(u'\u3000', '').replace('\t', '')
                print(split)
                letters = [x for x in split if not x == u'\u3000']
                print(letters)
        except Exception as e:
            print("Couldn't load letters: {}".format(e))
    return letters

def save_boxes(filename, rectangles):
    with open(filename, 'w') as f:
      for vector in rectangles:
          f.write(' '.join([str(x) for x in vector])+'\n')

def load_image(filename):
    img = cv2.imread(filename)
    return img

def read_filenames_from_folder(folder):
    images = list(glob.glob(folder+"*.jpg"))
    images.extend(list(glob.glob(folder+"*.png")))
    return images

def create_window_and_register_callback():
    cv2.namedWindow('input')
    cv2.setMouseCallback('input',onmouse)
    cv2.moveWindow('input', 300, 0)

if __name__ == '__main__':
    global img, img2, rectangles, letters

    # Loading images
    if len(sys.argv) == 2:
        folder = sys.argv[1] # for drawing purposes
    else:
        folder = './'

    if not os.path.isdir(folder):
        print("Please secify a folder as first argument, see README.md for details.")

    image_names = read_filenames_from_folder(folder)

    current_image = 0
    filename = image_names[current_image]
    box_filename = filename[:-4]+'.box'
    letter_filename = filename[:-4]+'.txt'

    original = load_image(filename)
    print(original.shape)
    img = load_image(filename)[:800]
    empty_image = np.matrix(img.shape)

    rectangles = load_box(box_filename)
    letters = load_letters(letter_filename)

    create_window_and_register_callback()
    offset = 0

    while(1):
        print("Pls Input")
        drawRectangles(img, rectangles)
        cv2.imshow('input', img)
        print_next_letter(letters, rectangles)
        k = 0xFF & cv2.waitKey(0)
        # key bindings
        if k == 27:         # esc to exit
            break
        elif k == ord('j'): # save rectangles
            if offset<original.shape[1]:
                offset += 50
            img = original.copy()[offset:800+offset, :]
            print(offset)
        elif k == ord('k'): # save rectangles
            if offset>0:
                offset -= 50
            img = original.copy()[offset:800+offset, :]
            print(offset)
        elif k == ord('s'): # save rectangles
            save_boxes(box_filename, rectangles)
        elif k == ord('u'):
            rectangles = rectangles[:-1]
            img = original.copy()[offset:800+offset, :]
        elif k == ord('r'): # reset everything
            rectangles = []
            img = original.copy()[offset:800+offset, :]
        elif k == ord('n'):
            current_image+=1
            if current_image>=len(images):
                current_image = 0
            filename = images[current_image]
            img, img2, rectangles = load_image(filename)
        elif k == ord('b'):
            current_image-=1
            if current_image<0:
                current_image = len(images)-1
            filename = images[current_image]
            img, img2, rectangles = load_image(filename)
    cv2.destroyAllWindows()
