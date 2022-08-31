import cv2
import numpy as np

#座標クリックして画像切り取りGUI

def mouse_event(event, x, y, flags,param):
    drag = -1
    if pickup_mode=="none":
        if event==cv2.EVENT_LBUTTONUP:
            drag = -1

        if event==cv2.EVENT_LBUTTONDOWN:
            for i,pt in enumerate(pts):
                if np.linalg.norm(np.array(pt)-np.array([x,y]))<60:
                    drag = i
                    pts[drag]= [x,y]
                    break

    cv2.polylines(ui_frame,[pts],True, (255,0,0) , 1 )
    prev_pt = None
    for pt in pts:
        cv2.circle(ui_frame, center =(int(pt[0]),int(pt[1])), radius = 6 , color = (0,0,255), thickness=2)
        if prev_pt is not None:
            cv2.line(ui_frame,((int(prev_pt[0]),int(prev_pt[1]))),((int(pt[0]),int(pt[1]))), (0,0,255), 2)
        else :
            first_pt=pt
        prev_pt=pt

    cv2.line(ui_frame,((int(prev_pt[0]),int(prev_pt[1]))),((int(first_pt[0]),int(first_pt[1]))), (0,0,255), 2)
    cv2.imshow('UI_image', ui_frame)

img = cv2.imread("take_data2/sabun_img.jpg")
pts = np.array(((127,68),(242,203),(538,151),(383,40)))
#if img is not None:
ui_frame = img.copy()
pickup_mode = 'none'
cv2.imshow('UI_image', ui_frame)
cv2.setMouseCallback('UI_image', mouse_event)
cv2.waitKey(0)
rect = cv2.boundingRect(pts)
x,y,w,h = rect
croped = img[y:y+h, x:x+w].copy()
pts = pts - pts.min(axis=0)
mask = np.zeros(croped.shape[:2], np.uint8)
cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)
dst = cv2.bitwise_and(croped, croped, mask=mask)

cv2.imwrite('take_data2/hmgra_img.jpg',dst)
cv2.destroyAllWindows()