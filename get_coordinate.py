import cv2

#クリックした座標を表示する

def onMouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)

img = cv2.imread('data/temp/blue_test.jpg')
cv2.imshow('sample', img)
cv2.setMouseCallback('sample', onMouse)
cv2.waitKey(0)