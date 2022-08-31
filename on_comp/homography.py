#透視変換
import cv2
import numpy as np
import math

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
#左上、左下、右下、右上
#if img is not None:
ui_frame = img.copy()
pickup_mode = 'none'
cv2.imshow('UI_image', ui_frame)
cv2.setMouseCallback('UI_image', mouse_event)
cv2.waitKey(0)

#hfakjdhakjdshakflajhfkajdflajdfakjsflaksjdhafdajdhflakjhdfjkahkjfhalkjsdalkjflaskjdaksjdsjhfalksdjhf
#hfakjdhakjdshakflajhfkajdflajdfakjsflaksjdhafdajdhflakjhdfjkahkjfhalkjsdalkjflaskjdaksjdsjhfalksdjhf


# 比率調整"1.0～1.5"の5段階調整
w_ratio = 1.1

# 変換前4点の座標　p1:左上　p2:右上 p3:左下 p4:右下
#"L_block.jpg"の座標
'''
p1 = np.array([79, 93])0
p2 = np.array([373,7])3
p3 = np.array([243,269])1
p4 = np.array([639,101])2
'''
#"sabun_img.jpg"の座標
'''
p1 = np.array([127, 68])
p2 = np.array([383,40])
p3 = np.array([242,203])
p4 = np.array([538,151])
'''

# 入力画像の読み込み
#img = cv2.imread("take_data2/sabun_img.jpg")

#マウスクリックした座標
p1 = pts[0]
p2 = pts[3]
p3 = pts[1]
p4 = pts[2]
 
#　幅取得
o_width = np.linalg.norm(p2 - p1)
o_width = math.floor(o_width * w_ratio)
 
#　高さ取得
o_height = np.linalg.norm(p3 - p1)
o_height = math.floor(o_height)
 
# 変換前の4点
src = np.float32([p1, p2, p3, p4])
 
# 変換後の4点
dst = np.float32([[0, 0],[o_width, 0],[0, o_height],[o_width, o_height]])
 
# 変換行列
M = cv2.getPerspectiveTransform(src, dst)
 
# 射影変換・透視変換する
output = cv2.warpPerspective(img, M,(o_width, o_height))

#画面に表示する
cv2.imshow('homography', output)
cv2.waitKey(0)

# 射影変換・透視変換した画像の保存
#cv2.imwrite("take_data2/ho2.jpg", output)

