import cv2


org_frame = cv2.split(self.baseImage)
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
    fgmask[i] = cv2.morphologyEx(fgmask[i], cv2.MORPH_OPEN, kernel)
    ret,fgmask[i] = cv2.threshold(fgmask[i],4,255,cv2.THRESH_BINARY)
fgmask_all = cv2.bitwise_or(fgmask[0],fgmask[1])
fgmask_all = cv2.bitwise_or(fgmask_all,fgmask[2])
