'''
usage python3 img_tracker.py

kindly create the save directory on the current path
'''
import cv2 as cv
import os
import math
import argparse
import sys
def face_detection_tracker(path_img):
    try:
        tracking_objects = {}
        
        track_id = 0
        center_points_cur_frame=[]
        face_cascade=cv.CascadeClassifier(cv.data.haarcascades+'haarcascade_frontalface_default.xml')
        name_img=sorted(os.listdir(os.path.join(os.getcwd(),path_img)),key=lambda f:int("".join(filter(str.isdigit,f))))
        for i in (name_img):
            img=cv.imread(os.path.join(os.getcwd(),path_img,i))
            gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            faces=face_cascade.detectMultiScale(gray,1.1,4)  
            tracker =cv.legacy.TrackerMedianFlow_create()
            j=1            
            for (x, y, w, h) in faces:
                # cv.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cx=int((x+x+w)/2)
                cy=int((y+y+h)/2)
                bbox=(x,y,x+w,y+h)                
                center_points_cur_frame.append((x,y,w,h))                  
                ok=tracker.init(img,bbox)
                ok,bbox=tracker.update(img)
                if ok:   #tracking success                
                    p1=(int(bbox[0]),int(bbox[1]))
                    p2=(int(bbox[0])+int(bbox[2]),int(bbox[1]+bbox[3]))
                    cv.rectangle(img,p1,p2,(255,0,0),2,1)
                    j+=1                 
            center_points_cur_frame_copy =center_points_cur_frame.copy()
            tracking_objects_copy = tracking_objects.copy()
            for object_id,pt2 in tracking_objects_copy.items():
                # #print("------>pt2 ",pt2)
                object_exists=False
                for pt in center_points_cur_frame_copy:
                    distance=math.hypot(pt2[0]-pt[0],pt[1]-pt[1])
                    #update Ids position
                    if distance <20:
                        tracking_objects[object_id]=pt
                        object_exists=True
                        if pt in center_points_cur_frame:
                            center_points_cur_frame.remove(pt)                            
                        continue
                #Remove Ids lost
                if not object_exists:
                    tracking_objects.pop(object_id)
            #Add new Ids found
            for pt in center_points_cur_frame:
                tracking_objects[track_id]=pt
                track_id +=1    
            metadata = {"data":[]}        
            for object_id,pt in tracking_objects.items():
                cv.putText(img,str(object_id),(pt[0],pt[1]-7),0,1,(0,0,255),2) 
                data = {}
                data["object_id"] = object_id
                x,y,w,h = list(pt)
                data["x"] = x
                data["y"] = y
                data["w"] = w
                data["h"] = h
                data['img_name']=i
                metadata["data"].append(data)                    
            print(metadata)                     
            cv.imshow("img",img)
            cv.waitKey(0)           

    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        print("Exception type: ", exception_type)
        print("File name: ", filename)
        print("Line number: ", line_number)


def args_parse():
    parser=argparse.ArgumentParser()
    parser.add_argument("-p","--path_src",help="give image path",required=True)
    argument=parser.parse_args()
    src_path=argument.path_src
    face_detection_tracker(src_path)

if __name__=="__main__":
    args_parse()    
    # face_detection_tracker("save")