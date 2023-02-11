################################################
"""
Part of Tarl Project.

Handles small stuff.. Just keeping stuff
organised :)
"""
################################################


import numpy as np
import pyautogui
import math
import cv2


def add_transparent_image(bg,fg,x,y,c=False):
    
    bg = cv2.cvtColor(bg, cv2.COLOR_BGR2BGRA)

    if x < bg.shape[1] - fg.shape[1] and y < bg.shape[0] - fg.shape[0]:

        bg_copy = bg.copy()
    
  

        bg[y:y+fg.shape[0], x:x+fg.shape[1]] = fg


        y_c = 0
        for y in bg:
        
            x_c = 0
            for x in y:
                if int(math.ceil(x[3])) == 0:
                
                    bg[y_c,x_c] = bg_copy[y_c,x_c]
                x_c+=1
            y_c+=1
    if not c:
        bg = cv2.cvtColor(bg,  cv2.COLOR_BGRA2RGB)
    else:
        bg = cv2.cvtColor(bg,  cv2.COLOR_BGRA2BGR)

    #cv2.imshow(".",bg)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows() 
    return bg

def add_transparent_image_center(bg,fg):
    return add_transparent_image(bg,fg,round(bg.shape[1]/2-fg.shape[1]/2),round(bg.shape[0]/2-fg.shape[0]/2),c=True)

