import cv2
import numpy as np

# 画像の読み込み
img = cv2.imread('data/temp/blueimage.jpg')

# グレースケール変換
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# HSV変換
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)

# 色範囲によるマスク生成
img_mask = cv2.inRange(img_hsv, np.array([159, 127,0]), np.array([177, 255, 255]))

# 輪郭抽出
contours, hierarchy = cv2.findContours(
    img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 小さい輪郭は誤検出として削除
contours = list(filter(lambda x: cv2.contourArea(x) > 100, contours))

# 輪郭の描画
cv2.drawContours(img, contours, -1, color=(0, 0, 255), thickness=2)

# イメージの表示
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()