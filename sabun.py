import cv2

baseImage = cv2.imread("take_data/offmapp.jpg")
new_img = cv2.imread("take_data/onmapp.jpg")

org_frame = cv2.split(baseImage)
new_frame = cv2.split(new_img)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))

fgbg = [ cv2.createBackgroundSubtractorMOG2(detectShadows = False), \
            cv2.createBackgroundSubtractorMOG2(detectShadows = False), \
            cv2.createBackgroundSubtractorMOG2(detectShadows = False) ]
#detectShadowsは影ありだとTrue,なしはFalse,デフォはTrue

fgmask = [0]*3
for i in range(3):
    fgmask[i] = fgbg[i].apply(org_frame[i])
    fgmask[i] = fgbg[i].apply(new_frame[i])
    #fgmask[i] = cv2.morphologyEx(fgmask[i], cv2.MORPH_OPEN, kernel)
    ret,fgmask[i] = cv2.threshold(fgmask[i],4,255,cv2.THRESH_BINARY)
fgmask_all = cv2.bitwise_or(fgmask[0],fgmask[1])
fgmask_all = cv2.bitwise_or(fgmask_all,fgmask[2])

fgmask_all = cv2.dilate(fgmask_all,kernel,iterations = 1)
#cv2.imshow("dilate",fgmask_all)
fgmask_all = cv2.erode(fgmask_all,kernel,iterations = 4)
# cv2.imshow("erode",fgmask_all)

fgmask_all_not = cv2.bitwise_not(fgmask_all)#色反転
fgmask_not_frame = cv2.cvtColor(fgmask_all_not, cv2.COLOR_GRAY2BGR)#色の変換GRAY→BGR


#  fgmask = cv2.morphologyEx(fgmask,cv2.MORPH_CLOSE,kernel)
# cv2.imshow("mask",fgmask)

mask_img = cv2.bitwise_and(new_img,new_img,mask=fgmask_all)
mask_img = cv2.bitwise_or(mask_img,fgmask_not_frame)

cv2.imshow("sabun_img",mask_img)
cv2.waitKey(0)
cv2.imwrite('take_data/sabun_img.jpg',mask_img)