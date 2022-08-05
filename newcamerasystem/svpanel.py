import tkinter as tk   
from tkinter import *
import numpy as np
import colorsys as csys

from setting import Setting

class SV_panel:
    def __init__(self,parent,setfile) :
        self.root = tk.Toplevel()
        self.root.title(u"カラー調整")
        self.root.geometry("800x400")
        
        self.main = parent
        
        self.cusf=tk.Frame(self.root)
        self.cusf.pack(fill=tk.BOTH, padx=10, pady=10)
        
        self.SLUT = np.zeros((256, 1), dtype = 'uint8')
        self.VLUT = np.zeros((256, 1), dtype = 'uint8')
        
        self.setting = Setting(setfile)
        self.setting.read_settings()
        
    
    def makeContrastLUT(self,cont, center, LUT):
        tmp = np.zeros((256, 1), dtype = 'float')
        if cont==0: cont=0.0001

        for i in range(256):
            #シグモイド関数
            tmp[i][0] = 100 /(1+ np.exp(-cont*(float(i) -center)/100))

        for i in range(256):
            #正規化
            if tmp[255][0]-tmp[0][0]!=0:
                LUT[i][0] = 255*(tmp[i][0]-tmp[0][0])/(tmp[255][0]-tmp[0][0])
                
    def cont_s(self,n):
           # self.s[0] = float(n)
        self.setting.s_con = float(n)
        self.makeContrastLUT(self.setting.s_con, self.setting.s_center, self.SLUT )
        
    def cont_s_c(self,n):
           # self.s[1] = float(n)
        self.setting.s_center = float(n)
        self.makeContrastLUT(self.setting.s_con, self.setting.s_center, self.SLUT )
        
    def cont_v(self,n):
        #self.v[0] = float(n)
        self.setting.v_con = float(n)
        self.makeContrastLUT(self.setting.v_con, self.setting.v_center, self.VLUT )
       
    def cont_v_c(self,n):
        #self.v[1] = float(n)
        self.setting.v_center = float(n)
        self.makeContrastLUT(self.setting.v_con, self.setting.v_center, self.VLUT )
        
    def range_red(self,n):
        self.setting.red_range = int(n)
        self.drawColorBar()
    def range_green(self,n):
        self.setting.green_range = int(n)
        self.drawColorBar()
    def range_blue(self,n):
        self.setting.blue_range = int(n)
        self.drawColorBar()
    def range_yellow(self,n):
        self.setting.yellow_range = int(n)
        self.drawColorBar()    
                 
              
        
    def set_red_h(self,val):
        self.setting.red_range_center = val
        self.red_e1.delete(0,tk.END)
        self.red_e1.insert(tk.END,self.setting.red_range_center)
        self.drawColorBar()
    def set_green_h(self,val):
        self.setting.green_range_center = val
        self.green_e1.delete(0,tk.END)
        self.green_e1.insert(tk.END,self.setting.green_range_center)
        self.drawColorBar()
    def set_blue_h(self,val):
        self.setting.blue_range_center = val
        self.blue_e1.delete(0,tk.END)
        self.blue_e1.insert(tk.END,self.setting.blue_range_center)
        self.drawColorBar()
    def set_yellow_h(self,val):
        self.setting.yellow_range_center = val
        self.yellow_e1.delete(0,tk.END)
        self.yellow_e1.insert(tk.END,self.setting.yellow_range_center)
        self.drawColorBar()    
        
    def red_pickup(self):
        self.main.pickup_mode = "red"
    def green_pickup(self):
        self.main.pickup_mode = "green"
    def blue_pickup(self):
        self.main.pickup_mode = "blue"
    def yellow_pickup(self):
        self.main.pickup_mode = "yellow" 
        
    def save_setting(self):
        print("設定を保存します")
        self.setting.save_settings()                           
        
    def makePanel(self):
        #彩度,彩度センター
        s_l1=tk.Label(self.cusf, text='彩度:', anchor=tk.W, fg='red')
        s_l1.grid(row=0,column=0,sticky=tk.W)
        s_scale1 = tk.Scale(self.cusf, length=300,orient='h',from_=0.0, to=10, resolution=0.1, tickinterval=2, command=self.cont_s)
        s_scale1.grid(row=0,column=1)
        s_c_l1=tk.Label(self.cusf, text='彩度センター:', anchor=tk.W, fg='red')
        s_c_l1.grid(row=1,column=0,sticky=tk.W)
        s_c_scale1 = tk.Scale(self.cusf, length=300,orient='h',from_=0, to=255, resolution=1, tickinterval=32, command=self.cont_s_c)
        s_c_scale1.grid(row=1,column=1)
        
        s_c_scale1.set(self.setting.s_center)
        s_scale1.set(self.setting.s_con)
        
        #明度,明度センター
        v_l1=tk.Label(self.cusf, text='明度:', anchor=tk.W, fg='blue')
        v_l1.grid(row=2,column=0,sticky=tk.W)
        v_scale1 = tk.Scale(self.cusf, length=300,orient='h',from_=0.0, to=10, resolution=0.1, tickinterval=2, command=self.cont_v)
        v_scale1.grid(row=2,column=1)
        v_c_l1=tk.Label(self.cusf, text='明度センター:', anchor=tk.W, fg='blue')
        v_c_l1.grid(row=3,column=0,sticky=tk.W)
        v_c_scale1 = tk.Scale(self.cusf, length=300,orient='h',from_=0, to=255, resolution=1, tickinterval=32, command=self.cont_v_c)
        v_c_scale1.grid(row=3,column=1)

        v_c_scale1.set(self.setting.v_center)
        v_scale1.set(self.setting.v_con)
        
        # 赤の範囲
        row_start = 0
        red_l1=tk.Label(self.cusf, text='赤:', anchor=tk.W, fg='red')
        red_l1.grid(row=row_start,column=2,sticky=tk.W)
        #self.sv_red = StringVar()
        #self.sv_red.trace("w",self.red_change)
        self.red_e1=tk.Spinbox(self.cusf,width=4,from_=0,to=359,command=self.red_change,wrap=True)
        self.red_e1.delete(first=0)
        self.red_e1.insert(tk.END,self.setting.red_range_center)
        self.red_e1.grid(row=row_start,column=3,sticky=tk.W)
        red_b1=tk.Button(self.cusf,text="pickup",command=self.red_pickup)
        red_b1.grid(row=row_start,column=4,sticky=tk.W)
        red_scale1 = tk.Scale(self.cusf, length=200,orient='h',from_=0, to=60, resolution=2, tickinterval=10, command=self.range_red)
        red_scale1.set(self.setting.red_range)
        red_scale1.grid(row=row_start,column=5)
        
        #緑の範囲
        row_start = 1
        green_l1=tk.Label(self.cusf, text='緑:', anchor=tk.W, fg='green')
        green_l1.grid(row=row_start,column=2,sticky=tk.W)
        self.green_e1=tk.Spinbox(self.cusf,width=4,from_=0,to=359,command=self.green_change,wrap=True)
        self.green_e1.delete(first=0)
        self.green_e1.insert(tk.END,self.setting.green_range_center)
        self.green_e1.grid(row=row_start,column=3,sticky=tk.W)
        green_b1=tk.Button(self.cusf,text="pickup",command=self.green_pickup)
        green_b1.grid(row=row_start,column=4,sticky=tk.W)
        green_scale1 = tk.Scale(self.cusf, length=200,orient='h',from_=0, to=60, resolution=2, tickinterval=10, command=self.range_green)
        green_scale1.set(self.setting.green_range)
        green_scale1.grid(row=row_start,column=5)
        
        #青の範囲
        row_start = 2
        blue_l1=tk.Label(self.cusf, text='青:', anchor=tk.W, fg='blue')
        blue_l1.grid(row=row_start,column=2,sticky=tk.W)
        self.blue_e1=tk.Spinbox(self.cusf,width=4,from_=0,to=359,command=self.blue_change,wrap=True)
        self.blue_e1.delete(first=0)
        self.blue_e1.insert(tk.END,self.setting.blue_range_center)
        self.blue_e1.grid(row=row_start,column=3,sticky=tk.W)
        blue_b1=tk.Button(self.cusf,text="pickup",command=self.blue_pickup)
        blue_b1.grid(row=row_start,column=4,sticky=tk.W)
        blue_scale1 = tk.Scale(self.cusf, length=200,orient='h',from_=0, to=60, resolution=2, tickinterval=10, command=self.range_blue)
        blue_scale1.set(self.setting.blue_range)
        blue_scale1.grid(row=row_start,column=5)
        
        #黄の範囲
        row_start = 3
        yellow_l1=tk.Label(self.cusf, text='黄:', anchor=tk.W, fg='yellow')
        yellow_l1.grid(row=row_start,column=2,sticky=tk.W)
        self.yellow_e1=tk.Spinbox(self.cusf,width=4,from_=0,to=359,command=self.yellow_change,wrap=True)
        self.yellow_e1.delete(first=0)
        self.yellow_e1.insert(tk.END,self.setting.yellow_range_center)
        self.yellow_e1.grid(row=row_start,column=3,sticky=tk.W)
        yellow_b1=tk.Button(self.cusf,text="pickup",command=self.yellow_pickup)
        yellow_b1.grid(row=row_start,column=4,sticky=tk.W)
        yellow_scale1 = tk.Scale(self.cusf, length=200,orient='h',from_=0, to=60, resolution=2, tickinterval=10, command=self.range_yellow)
        yellow_scale1.set(self.setting.yellow_range)
        yellow_scale1.grid(row=row_start,column=5)
        
        #カラーバー
        self.h_range_cv = tk.Canvas(self.cusf,width=400,height=32)
        #h_range_cv.create_rectangle(2,2,400,16)
        for h_val in range(360):
            color = csys.hsv_to_rgb(h_val/360,1,1)
            color_list = [int(x*255) for x in color]
            self.h_range_cv.create_line(h_val,2, h_val,16, fill="#{0[0]:02x}{0[1]:02x}{0[2]:02x}".format(color_list))
            self.h_range_cv.grid(row=4,column=2,columnspan=5)
        self.drawColorBar()
        
        #保存
        save_btn = tk.Button(self.cusf,text=u"設定保存",command=self.save_setting)
        save_btn.grid(row=6,column=0)
       
    #赤の範囲を取得    
    def getRedRange(self):
        try:
            if self.red_e1.get().isdecimal():
                self.setting.red_range_center = int(self.red_e1.get())
            start = self.setting.red_range_center - self.setting.red_range
            if start<0: start = start+360
            end = self.setting.red_range_center + self.setting.red_range
            if end>360: end = end - 360
            return start,end
        except:
            return 0,0
        
    #緑の範囲取得    
    def getGreenRange(self):
        try:
            if self.green_e1.get().isdecimal():
                self.setting.green_range_center = int(self.green_e1.get())
            start = self.setting.green_range_center - self.setting.green_range
            if start<0: start = start+360
            end = self.setting.green_range_center + self.setting.green_range
            if end>360: end = end - 360
            return start,end
        except:
            return 0,0
    
    #青の範囲取得
    def getBlueRange(self):
        try:
            if self.blue_e1.get().isdecimal():
                self.setting.blue_range_center = int(self.blue_e1.get())
            start = self.setting.blue_range_center - self.setting.blue_range
            if start<0: start = start+360
            end = self.setting.blue_range_center + self.setting.blue_range
            if end>360: end = end - 360
            return start,end
        except:
            return 0,0
    
    #黄の範囲取得    
    def getYellowRange(self):
        try:
            if self.yellow_e1.get().isdecimal():
                self.setting.yellow_range_center = int(self.yellow_e1.get())
            start = self.setting.yellow_range_center - self.setting.yellow_range
            if start<0: start = start+360
            end = self.setting.yellow_range_center + self.setting.yellow_range
            if end>360: end = end - 360
            return start,end
        except:
            return 0,0            
        
    def red_change(self,*args):
        val= int(self.red_e1.get())
        self.setting.red_range_center = val 
        self.drawColorBar()
    def green_change(self,*args):
        val= int(self.green_e1.get())
        self.setting.green_range_center = val 
        self.drawColorBar()
    def blue_change(self,*args):
        val= int(self.blue_e1.get())
        self.setting.blue_range_center = val 
        self.drawColorBar()
    def yellow_change(self,*args):
        val= int(self.yellow_e1.get())
        self.setting.yellow_range_center = val 
        self.drawColorBar()
        
                 
    
               
       
    #カラーバー    
    def drawColorBar(self):
        self.h_range_cv.delete("red1")
        self.h_range_cv.delete("red2")
        self.h_range_cv.delete("green")
        self.h_range_cv.delete("yellow")
        self.h_range_cv.delete("blue")

        st, ed = self.getRedRange()
        if st<=ed:
            self.h_range_cv.create_rectangle(st,20, ed,24, fill="red",tag="red1")
        else:
            self.h_range_cv.create_rectangle(0,20, ed,24, fill="red",tag="red1")
            self.h_range_cv.create_rectangle(st,20, 360,24, fill="red",tag="red2")

        st, ed = self.getGreenRange()
        self.h_range_cv.create_rectangle(st,20, ed,24, fill="green",tag="green")
        
        st, ed = self.getBlueRange()
        self.h_range_cv.create_rectangle(st,20, ed,24, fill="blue",tag="blue")
        
        st, ed = self.getYellowRange()
        self.h_range_cv.create_rectangle(st,20, ed,24, fill="yellow",tag="yellow")    