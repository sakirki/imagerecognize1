import cv2

'''
# maskの順番 r g b y bk
for i, cur_mask in enumerate(mask): 
    if i!=4 : #黒以外
        contours, hierarchy = cv2.findContours(cur_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:                  
        contours, hierarchy = cv2.findContours(cur_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
'''
im = cv2.imread('take_data/on_map.jpg')
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
contours, hierarchy = cv2.findContours(im_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# 各色の領域ごとに処理
for j,contour in enumerate(contours):#enumerate()リストやタプルの要素とインデックスを取得
    area = cv2.contourArea(contour,False)
    rect = cv2.boundingRect(contour)
    rectarea = rect[2]*rect[3]

    #大きさ不適合
    btm = rect[1]+rect[3]
    if btm<220 and (rectarea<380 or rectarea>4000) : # 画面上方の場合
        continue
    if 220<=btm<430 and (rectarea<1000 or rectarea>9000) : # 画面中段の場合 R 9500 
        continue
    if btm>=430 and (rectarea<2000 or rectarea>24000) : # 画面下方の場合
        continue

print(rectarea)