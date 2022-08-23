import os,sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import subprocess
import numpy as np
import shutil


class image_gui():

    # 変数
    filepath = None
    gamma = None
    Brightness = None
    Saturation= None
    Gaussian = None
    input_canvas = None
    output_canvas = None
    chg_out = None

    ##############
    #   初期設定  #
    ##############
    def __init__(self, main):
        # ファイル削除処理
        self.file_del()
        # 参照ボタン配置
        btn3 = Button(root, text=u'参照', command=self.button1_clicked)
        btn3.grid(row=0, column=1)
        btn3.place(x=670, y=320)

        # 閉じるボタン
        close1 = Button(root,text=u'閉じる',command=self.close_clicked)
        close1.grid(row=0,column=3)
        close1.place(x=715,y=320)

        # 参照ファイルパス表示ラベルの作成
        self.file1 = StringVar()
        self.file1_entry = ttk.Entry(root,textvariable=self.file1, width=70)
        self.file1_entry.grid(row=0, column=2)
        self.file1_entry.place(x=12,y=10)

    ##########################
    # ファイルを削除するメソッド #
    ##########################
    def file_del(self):
        if os.path.exists("./output_image_small.png") == True:
            os.remove("./output_image_small.png")        
        if os.path.exists("./output_image.jpeg") == True:
            os.remove("./output_image.jpeg")        
        if os.path.exists("./output_object_image.jpeg") == True:
            os.remove("./output_object_image.jpeg")
        if os.path.exists("./input_image.png") == True:
            os.remove("./input_image.png")
        if os.path.exists("./input_image_file.jpeg") == True:
            os.remove("./input_image_file.jpeg") 

    ########################
    # フォームを閉じるメソッド #
    ########################
    def close_clicked(self):
        # メッセージ出力
        res = messagebox.askokcancel("確認", "フォームを閉じますか？")
        #　フォームを閉じない場合
        if res != True:
            # 処理終了
            return        

        #不要ファイル削除
        self.file_del()
        #処理終了
        sys.exit()

    ####################################
    # 参照ボタンクリック時に起動するメソッド #
    ####################################
    def button1_clicked(self):
        # ファイル種類のフィルタ指定とファイルパス取得と表示（今回はjpeg)
        fTyp = [("画像ファイル","*.jpeg"),("画像ファイル","*.jpg")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        # 選択したファイルのパスを取得
        self.filepath = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
        # ファイル選択指定なし？
        if self.filepath == "":
            return
        # 選択したパス情報を設定    
        self.file1.set(self.filepath)
 
        # 画像を保存を実施するボタンの生成と配置
        self.button6 = Button(root,text=u"画像保存", command=self.save_clicked,width=11)
        self.button6.grid(row=0, column=3)
        self.button6.place(x=670, y=290)

        # 彩度変更用のスケールバーの設定
        self.Saturation = Scale(root, label='彩度倍率', orient='h',
                         from_=0.0, to=1.0,length=300,tickinterval=0.1,command=self.onSlider,resolution=0.01)
        self.Saturation.set(1.0)  
        self.Saturation.place(x=20,y=60)
        # 明度変更用のスケールバーの設定
        self.Brightness = Scale(root, label='明度倍率', orient='h',
                         from_=0.0, to=1.0,length=300,tickinterval=0.1,command=self.onSlider,resolution=0.01)
        self.Brightness.set(1.0)
        self.Brightness.place(x=20,y=150)

        # 画像ファイル読み込みと表示用画像サイズに変更と保存
        img = cv2.imread(self.filepath)
        cv2.imwrite("input_image_file.jpeg",img)
        img2 = cv2.resize(img,dsize=(320,240))
        cv2.imwrite("input_image.png",img2)
    
        # 入力画像を画面に表示
        self.out_image = ImageTk.PhotoImage(file="input_image.png")
        input_canvas.create_image(163, 122, image=self.out_image)

    ##################################
    # 画像保存ボタンクリック時のメソッド #
    ##################################
    def save_clicked(self):
        # ファイル種類
        f_type = [('画像ファイル', '*.jpeg'), ('画像ファイル', '*.jpg')]
        # 実行中のフォルダパス取得
        ini_dir = os.getcwd()
        # ファイル保存のダイアログ出力
        filepath = filedialog.asksaveasfilename(filetypes=f_type , initialdir=ini_dir, title='名前をつけて保存')
        # ファイル名を取得
        filename = os.path.basename(filepath)
        # ファイルを保存
        if filepath:
            # ファイルを書き込みで開く
            with open(filepath, "w", encoding="utf_8") as f:
                len = f.write(filename)
        else:
            return

        # 編集した画像ファイルがあるか確認する
        if os.path.exists("./output_image.jpeg") == True:            
            # 編集した画像ファイルを、ダイアログで指定したファイルへコピーする
            shutil.copyfile("./output_image.jpeg", filepath)
        else:
            # 編集画像が無いので、入力した画像ファイルで保存する。
            shutil.copyfile("./input_image_file.jpeg", filepath)

    ##################################
    # 顔モザイクONのボタンクリック時の処理 #
    ##################################
    def mosaic_clicked(self):
        # 出力ファイルなし
        if os.path.exists("./output_image.jpeg") == False:
            # 入力ファイルの読み出し
            img = cv2.imread(self.filepath)
        else:
            # 作成済みの出力ファイル
            img = cv2.imread("./output_image.jpeg")

        img = self.face_detect_mosaic(img)
        # 表示用に画像サイズを小さくする
        img2 = cv2.resize(img,dsize=(320,240))
        # 出力画像を保存
        cv2.imwrite("output_mosaic_image.png",img2)
        # 画像をセット
        self.out_image2 = ImageTk.PhotoImage(file="output_mosaic_image.png")
        output_canvas.create_image(160, 120, image=self.out_image2)
        # ファイル削除
        os.remove("./output_mosaic_image.png")

    ##############################
    # 顔検出ONボタンクリック時の処理 #
    ##############################
    def face_clicked(self):
        # 出力ファイルなし
        if os.path.exists("./output_image.jpeg") == False:
            # 入力ファイルの読み出し
            img = cv2.imread(self.filepath)
        else:
            # 作成済みの出力ファイル
            img = cv2.imread("./output_image.jpeg")
        # 顔検出と描画する
        img = self.face_detect(img)
        # 表示用に画像サイズを小さくする
        img2 = cv2.resize(img,dsize=(240,240))
        # 出力画像を保存
        cv2.imwrite("output_facerectangle_image.png",img2)
        # 画像をセット
        self.out_image3 = ImageTk.PhotoImage(file="output_facerectangle_image.png")
        output_canvas.create_image(160, 120, image=self.out_image3)
        os.remove("./output_facerectangle_image.png")
        
    ###################
    # γ補正メソッド     #
    ###################
    def gamma_correction(self,image,gamma):
        # 整数型で2次元配列を作成[256,1]
        lookup_table = np.zeros((256, 1), dtype = 'uint8')
        for loop in range(256):
            # γテーブルを作成
            lookup_table[loop][0] = 255 * pow(float(loop)/255, 1.0/gamma)
        # lookup Tableを用いて配列を変換        
        image_gamma = cv2.LUT(image, lookup_table)
        return image_gamma

    #####################
    # 彩度/明度変更メソッド #
    #####################
    def saturation_brightness_chg(self,image,saturation,brightness):
        # 色空間をBGRからHSVに変換
        img_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        # 彩度の計算
        img_hsv[:,:,(1)] = img_hsv[:,:,(1)]*saturation
        # 明度の計算
        img_hsv[:,:,(2)] = img_hsv[:,:,(2)]*brightness
        # 色空間をHSVからBGRに変換
        image_sat_bri = cv2.cvtColor(img_hsv,cv2.COLOR_HSV2BGR)
        return image_sat_bri

    ####################
    # ぼかし変更メソッド  #
    ####################
    def Gaussian_chg(self,image,kernel):
        #Gaussianフィルタ制御
        gaussian_img = cv2.GaussianBlur(image,(kernel,kernel),5)
        return gaussian_img   
    
    def onSlider(self,args): 
        # 入力ファイルの読み出し
        img = cv2.imread(self.filepath)
        # ガンマ補正
        #i_out = self.gamma_correction(img,float(self.gamma.get()))
        # 彩度、明度変更
        i_out = self.saturation_brightness_chg(img,self.Saturation.get(),self.Brightness.get())
        # GUIに表示する用の画像ファイルを作成
        cv2.imwrite("output_image.jpeg",i_out)
        self.chg_out = i_out
        # 表示用に画像サイズを小さくする
        img2 = cv2.resize(i_out,dsize=(320,240))
        #画像の輝度変化を強調する処理
        img2=img2.astype(np.float32)
        #edge_valueは手動で変えてください輝度変化の値です
        edge_value=70
        img_edge=img2-edge_value
        sigmoid=1/(1+np.exp(-0.1*img_edge))*255
        sigmoid=sigmoid.astype(np.uint8)
        # 出力画像を保存
        cv2.imwrite("output_mosaic_image.png",sigmoid)
        # 出力画像を保存
        cv2.imwrite("output_image_small.png",sigmoid)
        # 画像をセット
        self.out_image2 = ImageTk.PhotoImage(file="output_image_small.png")
        output_canvas.create_image(160, 120, image=self.out_image2)


if __name__ == '__main__':
    root = Tk()
    root.title("Image Viewer")
    # GUI全体のフレームサイズ
    root.geometry("800x600")
    # 出力ファイル画像表示の場所指定とサイズ指定
    output_canvas = Canvas(root, width=320, height=240)
    output_canvas.place(x=450, y=350)
    #　入力ファイル画像表示の場所指定とサイズ指定
    input_canvas = Canvas(root, width=320, height=240)
    input_canvas.place(x=50, y=350)
    # GUI表示
    image_gui(root)
    root.mainloop()