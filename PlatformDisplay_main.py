# 実行前にpygameをインストールする必要があります

import pygame
import sys
from pygame.locals import *
import datetime

import tkinter

width=900
height=540

fontname="yugothicyugothicuilight"
timefontname="msgothicmsuigothicmspgothic"


data=[["東京地下鉄1000系","Tokyo Metro Series 1000","2012年-    運行区間: 銀座線 浅草-渋谷"],
      ["小田急50000形 VSE","Odakyu 50000 Series (VSE)","新宿-箱根湯本,片瀬江ノ島"],
      ["JR東海 キヤ97系200番台","JR Central Series KiYa 97-200","東海区間はどこでも行けるはず。知らんけど。"],
      ["京王3000系+1000系 7色7重連","Keio 3000 & 1000 Series 7-colors","なんだこれは"]]
infomes="東京大学へようこそ！"
position=[width-140,width-140,width-140,width-140,width-140]
positionreset=[130-width,130-width,130-width,130-width,130-width]

root=[]
txt=[[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
infotxt=[]

def close_edit_window():
    global data,txt,infomes,infotxt,root
    for i in range(4):
        for j in range(3):
            data[i][j]=txt[i][j].get()
    infomes=infotxt.get()
    root.destroy()

def sys_close():
    global data,infomes
    with open("platformdisplaydata.txt","w",encoding="UTF-8") as f:
        for i in range(4):
            for j in range(3):
                f.write(data[i][j]+"\n")
        f.write(infomes+"\n")
    pygame.quit()
    sys.exit()

# define a main function
def main():
    global root,txt,infotxt,infomes,width,height,fontname,timefontname

    try:
        with open("platformdisplaydata.txt","r",encoding="UTF-8") as f:
            dt=f.readlines()
        for i in range(4):
            for j in range(3):
                data[i][j]=dt[i*3+j].replace("\n","")
        infomes=dt[12].replace("\n","")
    except:
        pass


    pygame.init()

    # print(sorted(pygame.font.get_fonts()))

    window = pygame.display.set_mode((width,height), pygame.RESIZABLE)
    pygame.display.set_caption("Window")

    sysfont=pygame.font.SysFont(fontname,48)
    minifont=pygame.font.SysFont(fontname,24)
    timefont=pygame.font.SysFont(timefontname,24)
    
    clock = pygame.time.Clock()
    
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
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    sys_close()
                elif event.key==K_e:
                    root = tkinter.Tk()
                    root.geometry('600x400')
                    root.title('情報を編集')
                    root.resizable(width=False,height=False)
                    lbl=[[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
                    for i in range(4):
                        lbl[i][0] = tkinter.Label(text=str(i+1)+'番線')
                        lbl[i][0].place(x=10, y=10+i*90)
                        txt[i][0] = tkinter.Entry(width=40)
                        txt[i][0].place(x=80, y=10+i*90)
                        txt[i][0].delete(0, tkinter.END)
                        txt[i][0].insert(0,data[i][0])
                        lbl[i][1] = tkinter.Label(text=str(i+1)+'番線 英語')
                        lbl[i][1].place(x=10, y=40+i*90)
                        txt[i][1] = tkinter.Entry(width=40)
                        txt[i][1].place(x=80, y=40+i*90)
                        txt[i][1].delete(0, tkinter.END)
                        txt[i][1].insert(0,data[i][1])
                        lbl[i][2] = tkinter.Label(text=str(i+1)+'番線 詳細')
                        lbl[i][2].place(x=10, y=70+i*90)
                        txt[i][2] = tkinter.Entry(width=80)
                        txt[i][2].place(x=80, y=70+i*90)
                        txt[i][2].delete(0, tkinter.END)
                        txt[i][2].insert(0,data[i][2])
                    infolbl = tkinter.Label(text='ご案内')
                    infolbl.place(x=10,y=370)
                    infotxt = tkinter.Entry(width=80)
                    infotxt.place(x=80,y=370)
                    infotxt.delete(0, tkinter.END)
                    infotxt.insert(0,infomes)
                    root.protocol("WM_DELETE_WINDOW", close_edit_window)
                    root.mainloop()
                    
        
       
        # 1番線
        sur=sysfont.render(data[0][0 if (sec%20<15) else 1], False, (255,128,0))
        window.blit(sur,(140,70))
        sur=minifont.render(data[0][2], False, (0,192,0))
        window.blit(sur,(140+position[0],130))
        positionreset[0]=-sur.get_width()-50

        # 1番線
        sur=sysfont.render(data[1][0 if (sec%20<15) else 1], False, (255,128,0))
        window.blit(sur,(140,170))
        sur=minifont.render(data[1][2], False, (0,192,0))
        window.blit(sur,(140+position[1],230))
        positionreset[1]=-sur.get_width()-50

        # 3番線
        sur=sysfont.render(data[2][0 if (sec%20<15) else 1], False, (255,128,0))
        window.blit(sur,(140,270))
        sur=minifont.render(data[2][2], False, (0,192,0))
        window.blit(sur,(140+position[2],330))
        positionreset[2]=-sur.get_width()-50

        # 4番線
        sur=sysfont.render(data[3][0 if (sec%20<15) else 1], False, (255,128,0))
        window.blit(sur,(140,370))
        sur=minifont.render(data[3][2], False, (0,192,0))
        window.blit(sur,(140+position[3],430))
        positionreset[3]=-sur.get_width()-50

        # ご案内
        sur=minifont.render(infomes, False, (0,192,0))
        window.blit(sur,(140+position[4],480))
        positionreset[4]=-sur.get_width()-50

        for i in range(5):
            position[i]-=1
            if position[i]<positionreset[i]:
                position[i]=width-140

        window.fill((120,120,120),(0,0,width,65))
        window.fill((120,120,120),(0,0,130,height))
        window.fill((120,120,120),(width-20,0,20,height))
        window.fill((120,120,120),(0,520,width,height-520))
        window.fill((120,120,120),(0,160,width,5))
        window.fill((120,120,120),(0,260,width,5))
        window.fill((120,120,120),(0,360,width,5))
        window.fill((120,120,120),(0,460,width,5))
        
        window.fill((0,0,0),(width-100,10,80,35)) # 時刻の背景
        sur=timefont.render(now.strftime("%H"+(":" if usec%1000000<500000 else " ")+"%M"), False, (255,128,0))
        window.blit(sur,(width-90,15))

        # 東大の青と東大の黄色
        window.fill((36,145,255),(10,30,30,30))
        window.fill((242,169,0),(10,00,30,30))

        sur=sysfont.render("走行中の車両", True, (255,255,255))
        window.blit(sur,(50,5))
        sur=minifont.render("内側が1番線で、外側が4番線です", True, (255,255,255))
        window.blit(sur,(350,25))

        sur=sysfont.render("1番線", True, (255,255,255))
        window.blit(sur,(5,70))
        sur=minifont.render("Track 1", True, (255,255,255))
        window.blit(sur,(5,130))
        sur=sysfont.render("2番線", True, (255,255,255))
        window.blit(sur,(5,170))
        sur=minifont.render("Track 2", True, (255,255,255))
        window.blit(sur,(5,230))
        sur=sysfont.render("3番線", True, (255,255,255))
        window.blit(sur,(5,270))
        sur=minifont.render("Track 3", True, (255,255,255))
        window.blit(sur,(5,330))
        sur=sysfont.render("4番線", True, (255,255,255))
        window.blit(sur,(5,370))
        sur=minifont.render("Track 4", True, (255,255,255))
        window.blit(sur,(5,430))
        sur=minifont.render("ご案内", True, (255,255,255))
        window.blit(sur,(5,480))

        # pygame.transform.smoothscale

        pygame.display.update()
        clock.tick(50)
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()