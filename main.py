import glob
import os
import time
from emailing import send_email
import cv2
import glob,os
from threading import Thread

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1

def clean_folder():
    images = glob.glob("images/*.png")
    for img in images:
        os.remove(img)

while True:
    check, frame = video.read()


    '''Conver frame into grayscale frames, this will reduce the amount of data in matrices'''
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame,(21,21),0)  # Blurring the gray frame so that it doesn't have so much noise.

    '''Comparaing the 1st frame with the new frames'''
    if first_frame is None:
        first_frame = gray_frame_gau
    delta_frame = cv2.absdiff(first_frame,gray_frame_gau)

    '''Close to 0 means black pixed & 255 means white pixels, so we are specifying if pixel are more than 60 then change it to 255'''
    thresh_frame = cv2.threshold(delta_frame,60,255,cv2.THRESH_BINARY)[1]

    '''To remove the noise from threshframe we'll have to dilate it.'''
    dil_frame = cv2.dilate(thresh_frame,None, iterations=2)

    '''Now put a frame around the object'''
    contours, check = cv2.findContours(dil_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    status = 0
    for contour in contours:
        if cv2.contourArea(contour) < 20000:
            continue
        x,y,w,h  = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
        if rectangle.any():
            status = 1
            '''Save images if object is present'''
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            all_images  = glob.glob("images/*.png")
            index = int(len(all_images)/2)
            images_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    '''Object has left the frame'''
    if status_list[0]==1 and status_list[1]==0:
        email_thread = Thread(target=send_email,args=(images_with_object,))
        email_thread.daemon = True
        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True

        email_thread.start()


    status_list.append(status)
    cv2.imshow("My Video", frame)

    key = cv2.waitKey(1)    # This creates keyboard key object
    if key == ord("q"):     # we are checking if the user's pressed key == 'r', then break
        break

video.release()
clean_thread.start()

