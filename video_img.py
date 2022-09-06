'''
python3 video_img.py -v 'video path' -s 'save directory name'

'''

from ast import arg
import cv2 as cv
import os
import shutil
import argparse
def video_img(videsrc):
    try:
        videcap=cv.VideoCapture(videsrc)
        succ,img=videcap.read()
        count=0
        save_path=input("Enter the name of Save directory:- ")
        if not os.path.exists(os.path.join(os.getcwd(),save_path)):

            os.mkdir(os.path.join(os.getcwd(),save_path))
        else:
            shutil.rmtree(os.path.join(os.getcwd(),save_path))
            os.mkdir(os.path.join(os.getcwd(),save_path))

        while succ:
            # cv.imwrite("save/frame%d.jpg"%count,img)
            cv.imwrite(os.path.join(os.getcwd(),save_path,f"frame{count}.jpg"),img)
            succ,img=videcap.read()
            print("Read a new freame",succ)
            count +=1 
    except Exception as e:
        print(e)
def args_parse():
    parser=argparse.ArgumentParser()
    parser.add_argument("-v","--video",help="add Video path",required=True)
    argument=parser.parse_args()
    video_src=argument.video
    video_img(video_src)
if __name__=="__main__":
    args_parse()