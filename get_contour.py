#輪郭を認識するコード

import cv2

im = cv2.imread('data/temp/map2.jpg')
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
retval, im_bw = cv2.threshold(im_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 輪郭の検出
contours, hierarchy = cv2.findContours(im_bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# 輪郭を１つずつ書き込んで出力
for i in range(len(contours)):
    im_con = im.copy()
    print('ID', i, 'Area', cv2.contourArea(contours[i]))
    im_con = cv2.drawContours(im_con, contours, i, (0,255,0), 2)
    cv2.imwrite('result' + str(i) + '.png', im_con)
