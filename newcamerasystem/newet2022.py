# -*- coding: utf-8 -*-
import cv2
import numpy as np
import tkinter as tk
import sys

from setuptools import Command
from datetime import datetime
from sympy import false
from svpanel import SV_panel


class main:
    def __init__(self):
        self.debug=false
        self.root = tk.Tk()
        self.root.title(u"カメラ撮影")
        self.root.geometry("600x400")
        '''
        output_canvas = tk.Canvas(self.root, width=320, height=240)
        output_canvas.place(x=400, y=90)
        '''
        btn1=tk.Button(text="撮影開始",command=self.take_picture)
        btn1.pack()
        
        try:
            setfile = sys.argv[1]
        except IndexError:
            setfile = "newcamerasystem/testpic/test.txt"
            
        self.svpanel = SV_panel(self,setfile)
        #self.svpanel.
        self.svpanel.makePanel()
    '''    
    def mouse_event(self,event, x, y, flags, param):
        if self.pickup_mode=="none":
            if event==cv2.EVENT_LBUTTONUP:
                self.drag = -1

            if event==cv2.EVENT_LBUTTONDOWN:
                for i,pt in enumerate(self.svpanel.setting.maskpt):
                    if np.linalg.norm(np.array(pt)-np.array([x*2,y*2]))<16:
                        self.drag = i
                        break
                for i,pt in enumerate(self.svpanel.setting.nummaskpt):
                    if np.linalg.norm(np.array(pt)-np.array([x*2,y*2]))<16:
                        self.drag = i+4
                        break
                

            if 0<=self.drag<=3 and event==cv2.EVENT_MOUSEMOVE:
                self.svpanel.setting.maskpt[self.drag]= [x*2,y*2]
            if 4<=self.drag<=5 and event==cv2.EVENT_MOUSEMOVE:
                self.svpanel.setting.nummaskpt[self.drag-4]= [x*2,y*2]
            
                
        elif self.pickup_mode=="red":
            if event==cv2.EVENT_LBUTTONUP:
                print ("red pickup")
                print(self.hsvchannel[0][y*2][x*2]*2)
                self.svpanel.set_red_h(self.hsvchannel[0][y*2][x*2]*2)
                self.pickup_mode="none"
        elif self.pickup_mode=="green":
            if event==cv2.EVENT_LBUTTONUP:
                print ("green pickup")
                self.svpanel.set_green_h(self.hsvchannel[0][y*2][x*2]*2)
                self.pickup_mode="none"
        elif self.pickup_mode=="blue":
            if event==cv2.EVENT_LBUTTONUP:
                print ("blue pickup")
                self.svpanel.set_blue_h(self.hsvchannel[0][y*2][x*2]*2)
                self.pickup_mode="none"
        elif self.pickup_mode=="yellow":
            if event==cv2.EVENT_LBUTTONUP:
                print ("yellow pickup")
                self.svpanel.set_yellow_h(self.hsvchannel[0][y*2][x*2]*2)
                self.pickup_mode="none"
    '''                
    def take_picture(self):
        self.pcap = cv2.VideoCapture(1)
        while (True):
            ret, self.frame =self.pcap.read()
            cv2.imshow("pキーで画像を保存 qキーで終了", self.frame)
            if cv2.waitKey(1)&0xff == ord('p'): # 「p」キーで画像を保存
                date = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.path = "newcamerasystem/testpic/pic" + date + ".jpg"
                cv2.imwrite(self.path, self.frame) # ファイル保存
            elif cv2.waitKey(1)& 0xff== ord('q'):
                    break # 「q」キーが押されたら終了する
                
        self.pcap.release()
        cv2.destroyAllWindows()               
        
etmain=main()
#etmain.out_image=cv2.imread("testpic/L_block.jpg")
etmain.root.mainloop()


#追加コード
#画像表示の場所指定とサイズ指定
#output_canvas = Canvas(root, width=320, height=240)
#output_canvas.place(x=440, y=90)
#画像をセットする
#output_canvas.create_image(160, 120, image=self.out_image)