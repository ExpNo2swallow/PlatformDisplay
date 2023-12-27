# 実行前にpygameをインストールする必要があります

import pygame
import sys
from pygame.locals import *
import datetime
import csv

import tkinter
from functools import partial

width=900
height=540

fontname="yugothic"
timefontname="msgothic"


data=[["test","",""],
      ["てすと","",""],
      ["テスト","",""],
      ["確認","",""]]
infomes="これは確認テストです。"
position=[width-140,width-140,width-140,width-140,width-140]
positionreset=[130-width,130-width,130-width,130-width,130-width]

root=[]
txt=[[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
infotxt=[]
accident=[0,0,0,0]
traindatalist=[["テスト1","Test1","これはテストです"]]
traindatalist_st=[]
traindatalist_sv=[]
traindatalist_lb=[]
traindatalist_sc=[]
linename=[["1番線","2番線","3番線","4番線"],["Track 1","Track 2","Track 3", "Track 4"]]
numberoflines=4

def writing_window():
    global root,txt,infotxt,infomes,width,height,fontname,timefontname
    
#メイン画面に反映
def refrection(i):
    global infomes,infotxt,data,txt
    if(i<numberoflines):
        for j in range(3):
            data[i][j]=txt[i][j].get()
        infomes=infotxt.get()
    else:
        print(i)

#ワンタッチ線路封鎖
def accidenting(i):
    global infomes,infotxt,data,txt,accident
    if(accident[i]==0):
        data[i][0]="車両・線路確認"
        data[i][1]="Something wrong is occuring!"
        data[i][2]="しばらくお待ちください"
    else:
        refrection(i)

def sys_close():
    global data,txt,infomes,infotxt,root
    root.destroy()
    with open("platformdisplaydata.txt","w",encoding="UTF-8") as f:
        for i in range(numberoflines):
            for j in range(3):
                f.write(data[i][j]+"\n")
        f.write(infomes+"\n")
    pygame.quit()
    sys.exit()

#ワンタッチ回送列車
def outofservicebutton(i):
    global infomes,data,txt
    if(i<4):
        txt[i][0].delete(0,"end")
        txt[i][1].delete(0,"end")
        txt[i][2].delete(0,"end")
        txt[i][0].insert(0,"回送")
        txt[i][1].insert(0,"Out of service")
        txt[i][2].insert(0,"この列車は回送列車です。ご利用になれませんのでご注意ください。")
    else:
        print(i)
    refrection(i)

#CSV読み込み
def csvreader():
    global traindatalist
    with open("train_list.csv",encoding="utf-8") as traindatalist_csv:
        traindatalist_csvr=csv.reader(traindatalist_csv)
        traindatalist=[row for row in traindatalist_csvr]
    print(traindatalist)
    numcount=0
    for train_d in traindatalist:
        traintext = train_d[0]+' '+train_d[2]
        print(traintext)
        if(numcount>=len(traindatalist_st)):
            traindatalist_st.append(traintext)
        else:
            traindatalist_st[numcount]=traintext
        numcount+=1
#CSV書き出し
def csvwriter(txtnum):
    global txt,data,traindatalist_sv,traindatalist_sc,traindatalist_lb,traindatalist_st
    with open("train_list.csv",'a',encoding="utf-8",newline='') as traindatalist_csv:
        write_csv=csv.writer(traindatalist_csv)
        write_csv.writerow([txt[txtnum][0].get(),txt[txtnum][1].get(),txt[txtnum][2].get()])
    csvreader()
    traindatalist_sv = tkinter.StringVar(value=traindatalist_st)
    traindatalist_lb = tkinter.Listbox(listvariable=traindatalist_sv,width=90,height=8)
    traindatalist_sc = tkinter.Scrollbar(orient=tkinter.VERTICAL, command=traindatalist_lb.yview)
    traindatalist_lb["yscrollcommand"] = traindatalist_sc.set
    traindatalist_lb.grid(row=0, column=0)
    traindatalist_sc.grid(row=0, column=1, sticky=(tkinter.N, tkinter.S))
    traindatalist_lb.place(x=10,y=460)
    traindatalist_sc.place(x=550,y=460,height=135)
    
#選択されたデータ読み込み
def dataroader(txtnum):
    global traindatalist,txt,traindatalist_lb
    txt[txtnum][0].delete(0,"end")
    txt[txtnum][1].delete(0,"end")
    txt[txtnum][2].delete(0,"end")
    listnum=traindatalist_lb.curselection()
    print(listnum)
    txt[txtnum][0].insert(0,traindatalist[listnum[0]][0])
    txt[txtnum][1].insert(0,traindatalist[listnum[0]][1])
    txt[txtnum][2].insert(0,traindatalist[listnum[0]][2])

# define a main function
def main():
    global root,txt,infotxt,infomes,width,height,fontname,timefontname,traindatalist,traindatalist_lb,traindatalist_sc,traindatalist_st,traindatalist_sv,linename,numberoflines
    pygame.init()

    # print(sorted(pygame.font.get_fonts()))
    
    numberoflines=input('線路数を入力してください')
    if numberoflines.isdecimal():
        numberoflines=int(numberoflines)
    else:
        numberoflines=4
    try:
        with open("platformdisplaydata.txt","r",encoding="UTF-8") as f:
            dt=f.readlines()
        for i in range(numberoflines):
            if i>= len(data):
                data.append([0,0,0])
            for j in range(3):
                data[i][j]=dt[i*3+j].replace("\n","")
        infomes=dt[3*numberoflines].replace("\n","")
    except:
        pass
    for i in range(numberoflines):
        if i>=len(linename[0]):
            linename[0].append(0)
            linename[1].append(0)
        linename[0][i]=str(i+1)+'番線'
        linename[1][i]='Track '+str(i+1)
    window = pygame.display.set_mode((width,height), pygame.RESIZABLE)
    pygame.display.set_caption("Window")

    sysfont=pygame.font.SysFont(fontname,48)
    minifont=pygame.font.SysFont(fontname,24)
    timefont=pygame.font.SysFont(timefontname,24)
    clock = pygame.time.Clock()

    #ここからサブウィンドウ処理
    root = tkinter.Tk()
    root.geometry("200x200")
    root.title('情報を編集')
    root.resizable(width=True,height=True)
    lbl=[[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
    btn=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    for i in range(numberoflines):
        print(i)
        if i>=len(lbl):
            lbl.append([0,0,0])
        if i>=len(txt):
            txt.append([0,0,0])
        if i>=len(btn):
            btn.append([0,0,0,0,0])
        if i>=len(data):
            data.append(["test","",""])
        lbl[i][0] = tkinter.Label(text=linename[0][i])
        lbl[i][0].place(x=10, y=10+i*90)
        txt[i][0] = tkinter.Entry(width=40)
        txt[i][0].place(x=80, y=10+i*90)
        txt[i][0].delete(0, tkinter.END)
        txt[i][0].insert(0,data[i][0])
        btn[i][0] = tkinter.Button(width=5,text='反映',command=partial(refrection,i))
        btn[i][0].place(x=330,y=10+i*90)
        btn[i][1] = tkinter.Button(width=5,text='回送',command=partial(outofservicebutton,i))
        btn[i][1].place(x=380,y=10+i*90)
        btn[i][2] = tkinter.Button(width=5,text='非常',command=partial(accidenting,i))
        btn[i][2].place(x=430,y=10+i*90)
        btn[i][3] = tkinter.Button(width=5,text='読込',command=partial(dataroader,i))
        btn[i][3].place(x=480,y=10+i*90)
        btn[i][4] = tkinter.Button(width=5,text='書出',command=partial(csvwriter,i))
        btn[i][4].place(x=530,y=10+i*90)
        lbl[i][1] = tkinter.Label(text=linename[0][i]+' 英語')
        lbl[i][1].place(x=10, y=40+i*90)
        txt[i][1] = tkinter.Entry(width=40)
        txt[i][1].place(x=80, y=40+i*90)
        txt[i][1].delete(0, tkinter.END)
        txt[i][1].insert(0,data[i][1])
        lbl[i][2] = tkinter.Label(text=linename[0][i]+' 詳細')
        lbl[i][2].place(x=10, y=70+i*90)
        txt[i][2] = tkinter.Entry(width=80)
        txt[i][2].place(x=80, y=70+i*90)
        txt[i][2].delete(0, tkinter.END)
        txt[i][2].insert(0,data[i][2])
    infolbl = tkinter.Label(text='ご案内')
    infolbl.place(x=10,y=10+numberoflines*90)
    infotxt = tkinter.Entry(width=80)
    infotxt.place(x=80,y=10+numberoflines*90)
    infotxt.delete(0, tkinter.END)
    infotxt.insert(0,infomes)
    #ここから読み込みデータの処理
    csvreader()
    traindatalist_sv = tkinter.StringVar(value=traindatalist_st)
    traindatalist_lb = tkinter.Listbox(listvariable=traindatalist_sv,width=90,height=8)
    traindatalist_sc = tkinter.Scrollbar(orient=tkinter.VERTICAL, command=traindatalist_lb.yview)
    traindatalist_lb["yscrollcommand"] = traindatalist_sc.set
    traindatalist_lb.grid(row=0, column=0)
    traindatalist_sc.grid(row=0, column=1, sticky=(tkinter.N, tkinter.S))
    traindatalist_lb.place(x=10,y=40+numberoflines*90)
    traindatalist_sc.place(x=550,y=40+numberoflines*90,height=135)


    root.protocol("WM_DELETE_WINDOW", sys_close)
    #ここまでサブウィンドウ処理

    while True:        
        now=datetime.datetime.now()
        sec=now.second
        usec=now.microsecond
        window.fill((0,0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys_close()
            elif event.type == pygame.VIDEORESIZE:
                width=event.w
                height=event.h
                window = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
        
        for i in range(numberoflines):
            if i >= len(position):
                position.append(width-140)
            if i >= len(positionreset):
                positionreset.append(0)
            sur=sysfont.render(data[i][0 if (sec%20<15)else 1], False, (255,128,0))
            window.blit(sur,(140,70+i*100))
            sur=minifont.render(data[i][2],False,(0,192,0))
            window.blit(sur,(140+position[i],130+100*i))
            positionreset[i]=-sur.get_width()-50
        # ご案内
        if len(position)<= numberoflines:
            position.append(width-140)
        if len(positionreset)<=numberoflines:
            positionreset.append(0)
        positionreset[numberoflines]=-sur.get_width()-50
        sur=minifont.render(infomes, False, (0,192,0))
        window.blit(sur,(140+position[numberoflines],80+100*numberoflines))

        for i in range(numberoflines+1):
            position[i]-=1
            if position[i]<positionreset[i]:
                position[i]=width-140

        window.fill((120,120,120),(0,0,width,65))
        window.fill((120,120,120),(0,0,130,height))
        window.fill((120,120,120),(width-20,0,20,height))
        for i in range(numberoflines):
            window.fill((120,120,120),(0,160+100*i,width,5))
        
        window.fill((120,120,120),(0,120+100*numberoflines,width,height-120-100*numberoflines))
        window.fill((0,0,0),(width-100,10,80,35)) # 時刻の背景
        sur=timefont.render(now.strftime("%H"+(":" if usec%1000000<500000 else " ")+"%M"), False, (255,128,0))
        window.blit(sur,(width-90,15))

        # 東大の青と東大の黄色
        window.fill((36,145,255),(10,30,30,30))
        window.fill((242,169,0),(10,00,30,30))

        sur=sysfont.render("走行中の車両", True, (255,255,255))
        window.blit(sur,(50,5))
        for i in range(numberoflines):
            sur=sysfont.render(linename[0][i],True,(255,255,255))
            window.blit(sur,(5,70+100*i))
            sur=minifont.render(linename[1][i],True,(255,255,255))
            window.blit(sur,(5,130+100*i))
        sur=minifont.render("ご案内", True, (255,255,255))
        window.blit(sur,(5,80+100*numberoflines))

        # pygame.transform.smoothscale

        pygame.display.update()
        clock.tick(50)
        root.update()
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()