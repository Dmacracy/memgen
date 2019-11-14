import os
import sys
import time
import random
import datetime

import cv2 as cv
import numpy as np


def get_img(imgname):
  '''Reads in an imag filename and returns the 
     corresponding image object which is a uint 
     numpy array.'''
  return cv.imread(imgname)

def write_on_img(img, outname, text="FUCK", loc=(200,200),
                 font=cv.FONT_HERSHEY_PLAIN, size=3,
                 color=(255, 255, 255), thickness=1):
  '''This function writes text onto an image and then writes 
     the resulting image to disk.'''
  img = cv.putText(img, text, loc, font, size, (0,0,0), thickness+8)
  img = cv.putText(img, text, loc, font, size, (255,255,255), thickness+5)
  img = cv.putText(img, text, loc, font, size, color, thickness)
  #cv.imwrite(outname, img)
  return img

def display_img(outdir, window, img):
  cv.imshow(window, img)
  k = cv.waitKey(0)
  if k == 27:         # wait for ESC key to exit
    cv.destroyAllWindows()
  elif k == ord('n'):
    run()
  elif k == ord('s'):
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('MeMe_%Y-%m-%d__%H:%M:%S')
    cv.imwrite(os.path.join(outdir, timestamp + ".jpg"), img)
    run()
    
    

def write_randomly(img, outname, text):
  '''This function writes text onto an image with random colors, 
     a random location and with random size and thickness.'''
  x = random.randint(0, img.shape[1] - img.shape[1] // 4)
  y = random.randint(0, img.shape[0] - img.shape[0] // 4)
  r = random.randint(0, 255)
  g = random.randint(0, 255)
  b = random.randint(0, 255)
  size = random.randint(1, 10)
  thickness = random.randint(3, 10)
  write_on_img(img, outname, text=text, loc=(x, y), size=size, color=(r, g, b))

def write_meme(img, outname, textupp, textlow, maxlinelen=6, imdiv=12):
  line1up = " ".join(textupp[:maxlinelen])
  line2up = " ".join(textupp[maxlinelen:2*maxlinelen])
  line1lo = " ".join(textlow[:maxlinelen])
  line2lo = " ".join(textlow[maxlinelen:2*maxlinelen])
  r = random.randint(0, 255)
  g = random.randint(0, 255)
  b = random.randint(0, 255)
  img = write_on_img(img, outname, text=line1up, loc=(0, img.shape[0] // imdiv), size=4, color=(r, g, b), thickness=5)
  img = write_on_img(img, outname, text=line2up, loc=(0, 2 * img.shape[0] // imdiv), size=4, color=(r, g, b), thickness=5)
  img = write_on_img(img, outname, text=line2lo, loc=(0, img.shape[0] - img.shape[0] // imdiv), size=4, color=(r, g, b), thickness=5)
  img = write_on_img(img, outname, text=line1lo, loc=(0, img.shape[0] - (2 * img.shape[0] // imdiv)), size=4, color=(r, g, b), thickness=5)
  return img
  

def read_txt(txtfilename):
  '''Reads in a text file and returns it as a list of 
     strings that are space separted words.'''
  with open(txtfilename, "r") as txtfile:
    line = " ".join(txtfile.readlines())
    return line.split()

def return_random_text(textList, minstrlen=3, maxstrlen=12):
  '''Given a list of strings, this returns a random sublist 
     of the text.'''
  randomlen = random.randint(minstrlen, maxstrlen)
  r = random.randint(0, len(textList) - randomlen - 1)
  randstringlist = textList[r : r + randomlen]
  return randstringlist

def choose_random_file(direct):
  files = os.listdir(direct)
  return files[random.randint(0, len(files) - 1)]
  
  
def run():
  if getattr(sys, 'frozen', False):
    # frozen
    path = os.path.dirname(sys.executable)
  else:
    # unfrozen
    path = os.path.dirname(os.path.realpath(__file__))
  txtdir = os.path.join(path, "input_texts")
  imgdirin = os.path.join(path, "input_images")
  imgdirout = os.path.join(path, "output_images")
  intxt =  os.path.join(txtdir, choose_random_file(txtdir))
  img = choose_random_file(imgdirin)
  inimg = os.path.join(imgdirin, img)
  outimg = os.path.join(imgdirout, img)
  text = read_txt(intxt)
  meme = write_meme(get_img(inimg), outimg, return_random_text(text), return_random_text(text))
  cv.namedWindow("MeMeGen", cv.WINDOW_NORMAL)
  if meme.shape[0] > meme.shape[1]:
    cv.resizeWindow("MeMeGen", int(float(meme.shape[1]) / float(meme.shape[0]) * 700), 700)
  else:
    cv.resizeWindow("MeMeGen", 700, int(float(meme.shape[0]) / float(meme.shape[1]) * 700))
  display_img(imgdirout, "MeMeGen", meme)
    
if __name__ == "__main__":
  run()



  
  
