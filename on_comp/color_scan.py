import cv2
import numpy as np
#画像スキャン
#物体検出、外接短形、座標
#配列で渡すやつ

src = cv2.imread("take_data2/ho2.jpg")

block=[[0,0]]*8

gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
retval, bw = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
contours, hierarchy = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

# 矩形検出された数（デフォルトで0を指定）
detect_count = 0

block_count = 1

block_idx=0
# 各輪郭に対する処理
for i in range(0, len(contours)):
    '''
    # 輪郭の領域を計算
    area = cv2.contourArea(contours[i])

    # ノイズ（小さすぎる領域）と全体の輪郭（大きすぎる領域）を除外
    if area < 1e2 or 1e4 < area:
        continue
    '''
    # 外接矩形
    if len(contours[i]) > 0:
        rect = contours[i]
        x, y, w, h = cv2.boundingRect(rect)
        #print('面積',i,'番目',w*h)
        #ノイズ除去と大枠除去
        rect_area = w*h
        if rect_area<1e3 or 1e4<rect_area:
            continue

        #ブロックの中心にブロック番号(個数)付与
        M = cv2.moments(contours[i])
        if M['m00']!=0:
            cx,cy= int(M["m10"]/M["m00"]) , int(M["m01"]/M["m00"])
            #print(block_count,'番目',cx,cy)
        
        block[block_idx]=[cx,cy]
        block_idx += 1
        #cv2.putText(src,str(block_count) , (cx, cy), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1, cv2.LINE_AA)

        block_count += 1
        #外接短形の描写
        cv2.rectangle(src, (x, y), (x + w, y + h), (0, 255, 0), 2)

        #外接矩形毎に画像を保存
        #cv2.imwrite('{ファイルパス}' + str(detect_count) + '.jpg', src[y:y + h, x:x + w])

        detect_count = detect_count + 1
''''''
#blockのソート
SORT1=[[0,0]]*3
SORT2=[[0,0]]*2
SORT3=[[0,0]]*3
my_c1 = 0
my_c2 = 0
my_c3 = 0
for g in range(0,8):
    if block[g][1]<50:
        SORT1[my_c1] = block[g]
        my_c1+=1
    if 50<block[g][1] and block[g][1]<130:
        SORT2[my_c2] = block[g]
        my_c2+=1
    if block[g][1]>140:
        SORT3[my_c3] = block[g]
        my_c3+=1
SORT1.sort()
SORT2.sort()
SORT3.sort()
for h in range(0,8):
    if h<3:
        block[h]=SORT1[h]
    if 2<h and h<5:
        block[h]=SORT2[h-3]
    if h>4:
        block[h]=SORT3[h-5]
'''
print(SORT1)
print(SORT2)
print(SORT3)
'''
#print(block)
crimg = cv2.imread('take_data2/ho2.jpg')
#block2=[[40,43],[146,43],[253,47],[41,114],[270,116],[44,198],[166,200],[285,200]]
for idx in range(0,8):
    # 対象範囲を切り出し
    boxFromX = block[idx][0]-1 #対象範囲開始位置 X座標
    boxFromY = block[idx][1]-1 #対象範囲開始位置 Y座標
    boxToX = block[idx][0]+1 #対象範囲終了位置 X座標
    boxToY = block[idx][1]+1 #対象範囲終了位置 Y座標
    # y:y+h, x:x+w　の順で設定
    imgBox = crimg[boxFromY: boxToY, boxFromX: boxToX]

    # RGB平均値を出力
    # flattenで一次元化しmeanで平均を取得
    b = imgBox.T[0].flatten().mean()
    g = imgBox.T[1].flatten().mean()
    r = imgBox.T[2].flatten().mean()
    block[idx].append([b,g,r])
    '''
    print('r',r)
    print('g',g)
    print('b',b)
    

print(block[0],block[1],block[2])
print(block[3],'\t\t\t\t',block[4])
print(block[5],block[6],block[7])
'''
# 外接矩形された画像を表示
cv2.imshow('output', src)
cv2.waitKey(0)

#画像の保存
#cv2.imwrite('take_data/cont_block_rect3.jpg',src)

# 終了処理
cv2.destroyAllWindows()
block_color=[[]]*8
#閾値判定
for i in range(0,8):
    #赤の範囲
    #b
    if 0.0<block[i][2][0] and block[i][2][0]<25.0:
        #g
        if 3.0<block[i][2][1] and block[i][2][1]<39.0:
            #r
            if 89.0<block[i][2][2]: #and block[i][2][2]<
                block_color[i]='r'
    #青の範囲
    #b
    if 50.0<block[i][2][0] and block[i][2][0]<75.0:
        #g
        if 18.0<block[i][2][1] and block[i][2][1]<52.0:
            #r
            if 0.0<block[i][2][2] and block[i][2][2]<35.0:
                block_color[i]='b'
    #緑の範囲
    #b
    if 0.0<block[i][2][0] and block[i][2][0]<35.0:
        #g
        if 20.0<block[i][2][1] and block[i][2][1]<53.0:
            #r
            if 0.0<block[i][2][2] and block[i][2][2]<35.0:
                block_color[i]='g'
    #黄の範囲
    #b
    if 5.0<block[i][2][0] and block[i][2][0]<45.0:
        #g
        if 87.0<block[i][2][1] and block[i][2][1]<236.0:
            #r
            if 105.0<block[i][2][2] and block[i][2][2]<255.1:
                block_color[i]='y'

print(block_color[0],block_color[1],block_color[2])
print(block_color[3],' ',block_color[4])
print(block_color[5],block_color[6],block_color[7])