#ライブラリのインポート
import numpy as np
import cv2
#ベース画像の読み込み
img=cv2.imread("data/temp/notest.jpg")
img=img.astype(np.float32)
#画像の輝度変化を強調する処理
edge_value=70
img_edge=img-edge_value
sigmoid=1/(1+np.exp(-0.1*img_edge))*255
sigmoid=sigmoid.astype(np.uint8)
#画像の出力
cv2.imwrite('edge_value'+str(edge_value)+'.jpg',sigmoid)