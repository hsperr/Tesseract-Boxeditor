# Tesseract-Boxeditor v 0.1

I found there is actually no good box editors for [Tesseract OCR](https://github.com/tesseract-ocr) around so I decided to start my own.
[Felix Von Drigalski](https://github.com/felixvd) showed me the opencv for python2.7 library which this is built on top of.

## Requirements

```
  - Python 2.7
  - OpenCV
```

## Install

If you already have Python 2.7 (Mini/Anaconda Recommended) installed, you can get openCV with

```
conda install opencv
```

or if you don't have anaconda using pip

```
pip install opencv
```

After that the script should run.

## How to use

The script needs a folder as parameter, in that folder it will search all `*.png` and `*.jpg` files. for each of those it will look if a corresponding `*.box` and `*.txt` exists in the same folder. The `txt` will be used to display the character that needs to be boxed next and the `box` file is to load previously done work.

e.g. (image1 etc are just example names):

```
python ~/ocr/receipts/

  - Expects:
     -> image1.jpg
     -> image1.box (optional)
     -> image1.txt (not optional but will be later)
     -> image2.jpg
     -> image2.box 
     ....
```

### Keyboard Shortcuts

For now they are not seperately documented but keyboard shortcuts are:

```
  n - load next image
  b - load previous image
  s - save boxes
  r - reset all boxes
  u - undo last box
```

