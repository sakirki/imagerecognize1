import numpy as np
import cv2
#ボーナスブロック画像切り取り

img = cv2.imread("take_data2/L_block.jpg")
pts = np.array([[340,320],[340,477],[550,477],[550,320]])#座標指定
                #左上、左下、右下、右上
rect = cv2.boundingRect(pts)
x,y,w,h = rect
croped = img[y:y+h, x:x+w].copy()
pts = pts - pts.min(axis=0)
mask = np.zeros(croped.shape[:2], np.uint8)
cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)
dst = cv2.bitwise_and(croped, croped, mask=mask)

cv2.imwrite("take_data2/bns_mask.jpg", dst)