from __future__ import print_function

import numpy as np
import cv2
import sys
import os
import glob

BLUE = [255,0,0]        # rectangle color
ix, iy = -1, -1
rectangles = []
letters = []

def drawRectangles():
    for cnt, (x1, y1, x2, y2) in enumerate(rectangles):
        cv2.rectangle(img, (x1, y1), (x2, y2), BLUE, 1)
        cv2.putText(img, str(cnt), (x2, y2+2), cv2.FONT_HERSHEY_SIMPLEX, 1, 1)
        #:TODO : Write number under each rectangle (for easier typing later)

def onmouse(event, x, y, flags, param):
    global rectangle, ix, iy, img, img2, buffer_img
    # Draw Rectangle
    y=y+3
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Set {} {}".format(x, y))
        rectangle = True
        if ix<0 and iy<0:
            ix,iy = x,y
        else:
            rectangles.append((min(ix, x), min(iy, y), max(ix, x), max(iy,y)))
            img = img2.copy()
            drawRectangles()
            #buffer_img = img.copy()
            print(rectangles)
            ix, iy = -1, -1
            cv2.imshow('input',img)
    elif event == cv2.EVENT_MOUSEMOVE:
        pass
    elif event == cv2.EVENT_LBUTTONUP:
        pass


def load_box(filename):
    box_filename = filename[:-4] + '.box'
    print(box_filename)
    rectangles = []
    if os.path.exists(box_filename):
        try:
            with open(box_filename) as f:
                split = f.read().split('\n')
                print(split)
                rectangles = [map(int, x.split(' ')[1:-1]) for x in split[:-1]]
        except Exception as e:
            print("Couldn't load boxfile: {}".format(e))
    return rectangles

def load_letters(filename):
    letter_filename = filename[:-4] + '.txt'
    print(letter_filename)
    rectangles = []
    if os.path.exists(letter_filename):
        try:
            with open(letter_filename) as f:
                split = f.read().decode('utf-8').replace('\n', '').replace(' ', '').replace(u'\u3000', '')
                print(split)
                letters = [x for x in split if not x == u'\u3000']
                print(letters)
        except Exception as e:
            print("Couldn't load letters: {}".format(e))
    return letters

def save_box():
    with open(box_filename, 'w') as f:
      for vector in rectangles:
          f.write(','.join([str(x) for x in vector])+'\n')

def undo_rectangle():
    global img, img2, rectangles
    rectangles = rectangles[:-1]
    img = img2.copy()
    drawRectangles()

def reset():
    global img, img2, rectangles
    print("resetting \n")
    img = img2.copy()
    rectangles = []
    drawRectangles()

def load_image(filename):
    rectangles = load_box(filename)
    letters = load_letters(filename)
    img = cv2.imread(filename)
    original_img = img.copy()                               # a copy of original image
    drawRectangles()
    return img, original_img, rectangles, letters


if __name__ == '__main__':
    global img, img2, rectangles, letters
    # Loading images
    if len(sys.argv) == 2:
        folder = sys.argv[1] # for drawing purposes
    else:
        folder = './'

    images = list(glob.glob(folder+"*.jpg"))
    images.extend(list(glob.glob(folder+"*.png")))

    current_image = 0
    filename = images[current_image]
    img, img2, rectangles, letters = load_image(filename)
    print(letters)

    cv2.namedWindow('input')
    cv2.setMouseCallback('input',onmouse)

    while(1):
        print("Pls Input")
        cv2.imshow('input',img)
        print("Next letter:",letters[len(rectangles)], [letters[len(rectangles)]])
        k = 0xFF & cv2.waitKey(0)

        # key bindings
        if k == 27:         # esc to exit
            break
        elif k == ord('s'): # save rectangles
            save_box()
        elif k == ord('u'):
            undo_rectangle()
        elif k == ord('r'): # reset everything
            reset()
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
