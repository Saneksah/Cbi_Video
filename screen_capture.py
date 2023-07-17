import cv2 
import numpy as np
import os
import pyautogui
from PIL import Image, ImageChops
from fpdf import FPDF

path_image1 = os.path.dirname(os.path.abspath(__file__)) + "\\" + "photo_main"
path_image2 = os.path.dirname(os.path.abspath(__file__)) + "\\" + "photo"


if not os.path.exists(path_image1):
    os.makedirs(path_image1)
if not os.path.exists(path_image2):
    os.makedirs(path_image2)

pdf = FPDF()
pdf.add_page()
pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
pdf.set_font('DejaVu', '', 14)
pdf.cell(200, 10, txt="Отчет", ln=1, align="C")

def screenshoter(output_folder, window):
    screen_width, screen_height = pyautogui.size()
    captured_frame = None

    cap = cv2.VideoCapture('main.mp4')

    screen_number = 1
    cv2.namedWindow('video', cv2.WINDOW_NORMAL)
    cv2.moveWindow('video', window, 0)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('video', frame)
        cv2.imwrite(f'{output_folder}/frame_{cap.get(cv2.CAP_PROP_POS_FRAMES)}.png', frame)
        
        if cv2.waitKey(20) & 0XFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def difference_images(img1, img2):
    image_1 = Image.open(img1)
    image_2 = Image.open(img2)

    result=ImageChops.difference(image_1, image_2).getbbox() 
    if result==None:
        pdf.cell(200, 10, txt=f"{img1},{img2}, ok", ln=1, align="С")
    else:
        pdf.cell(200, 10, txt=f"{img1},{img2}, ne ok", ln=1, align="С")
    return

def obrobotka():
    path1='./photo_main/'
    path2='./photo/'
    img_main = os.listdir(path1)
    img_proverka = os.listdir(path2)
    check_file = 0
    current_file = 0
    while True:
        try:
            difference_images(path1+img_main[current_file], path2+img_proverka[check_file])
            
            if current_file == len(img_main):
                break
            if check_file == len(img_proverka):
                break
            
            check_file += 1
            current_file += 1
        except:
            print('End')
            break


screenshoter(path_image1, 1920)
screenshoter(path_image2, 7000)
obrobotka()



pdf.output(os.path.dirname(os.path.abspath(__file__)) + '\\' + "report.pdf")