from tkinter import *
from turtle import Turtle
from click import command
from pygame import mixer
import os
import HandTrackingModule as HTM
import cv2
from PIL import Image,ImageTk,ImageFilter
root=Tk()
root.title("Music Player")
root.geometry("1280x680")
root.config(bg="#0f9876")
mixer.init()
bg=Image.open("music_bg.png")
bg=bg.resize((1280,650))
#bg=bg.filter(ImageFilter.BoxBlur(3))
bg=ImageTk.PhotoImage(bg)
Label(root,image=bg).place(x=0,y=0)

def add_music():
    path=r"C:\Users\asus\Music"
    songs=os.listdir(path)
    for j,i in enumerate(songs):
        if i.endswith(".mp3"):
            playlist.insert(END,i)
def play_music():
   global music_number
   global Music_Name
   global x
   Music_Name= playlist.get(ACTIVE)
   try:
    music_number=playlist.curselection()[0]
   except:
        pass
   mixer.music.load(Music_Name)
   mixer.music.play()
   l1.config(text="Now Playing...\n"+Music_Name)
def next_song():
    global music_number
    global Music_Name
    mixer.music.stop()
    if music_number==playlist.index("end")-1:
        music_number=0
    else:
        music_number+=1
    Music_Name=playlist.get(music_number)
    mixer.music.load(Music_Name)
    mixer.music.play()
    l1.config(text=Music_Name)

def previous_song():
    global Music_Name
    global music_number
    mixer.music.stop()
    if music_number==0 :
        music_number = playlist.index("end")-1
    else:
        music_number-=1
    Music_Name=playlist.get(music_number)
    mixer.music.load(Music_Name)
    mixer.music.play()
    l1.config(text="Now Playing...\n"+Music_Name)

#hand detection
def manually():
    global x
    x=True
def gesture():
    global Music_Name ,vframe
    vframe=Label(Frame_Video)
    vframe.place(x=0,y=0)
    cap = cv2.VideoCapture(0)
    global x,tr1,tr2,detector,u,u2,hand_pos_starting_v,hand_pos_starting,hand_pos_starting2,hand_pos_starting2_v,uv,u2_v,temp
    detector = HTM.handDetector()
    u=False
    u2=False
    hand_pos_starting=500
    hand_pos_starting2=0
    uv=False
    u2_v=False
    hand_pos_starting_v=0
    hand_pos_starting2_v=0
    temp=0
    x=False
    tr1=True
    tr2=True
    def show_frames():
        global x,vol_var,tr1,tr2,vframe,detector,u,u2,hand_pos_starting_v,hand_pos_starting,hand_pos_starting2,hand_pos_starting2_v,uv,u2_v,temp
        success, img = cap.read()
        img=cv2.flip(img,1)
        img = detector.findHands(img)
        lmlist = detector.findPosition(img)
        ax=True
        if len(lmlist) != 0:
            if tr1:
                if lmlist[4][0]<=300:
                    hand_pos_starting=lmlist[4][0]
                else:
                    hand_pos_starting2=lmlist[4][0]
                print("1",lmlist[4][0])
                tr1=False
                
            if hand_pos_starting<=300 and lmlist[4][0]>150:
                next_song()
                print("2",lmlist[4][0])
                cv2.waitKey(1000)
                hand_pos_starting=500
                tr1=True
                ax=False
            if hand_pos_starting2>300 and lmlist[4][0]<300:
                previous_song()
                print("3",lmlist[4][0])
                cv2.waitKey(1000)
                hand_pos_starting2=0
                tr1=True
                ax=False

            # Volume
            if ax:
                if tr2:
                    if lmlist[4][1]<=250:
                        hand_pos_starting_v=lmlist[4][1]
                    else:
                        hand_pos_starting2_v=lmlist[4][1]
                    tr2=False
                if hand_pos_starting_v<=250 and lmlist[4][1]>250:
                    vol_var=mixer.music.get_volume()-0.1
                    mixer.music.set_volume(vol_var)
                    cv2.waitKey(1000)
                    hand_pos_starting_v=500
                    tr2=True
                if hand_pos_starting2_v>250 and lmlist[4][1]<250:
                    vol_var=mixer.music.get_volume()+0.1
                    mixer.music.set_volume(vol_var)
                    cv2.waitKey(1000)
                    hand_pos_starting2_v=0
                    tr2=True         
                #vol.set( mixer.music.get_volume())
                vol.configure(vol.set(vol_var))

        img=Image.fromarray(img)
        img=ImageTk.PhotoImage(image=img)
        vframe.img=img
        vframe.configure(image=img)
        if x:
            cap.release()
            vframe.configure(image=hgbtn)
            return
        vframe.after(10,show_frames)
    show_frames()
    
def set_vl(z):
    mixer.music.set_volume(float(z))
    vol_var = float(z) 
music_number=0

Frame_Music = Frame(root, bd=2, relief = RIDGE)
Frame_Music.place(x=750, y=0, width=520, height=340)

Frame_Video = Frame(root, bd=2, relief = RIDGE)
Frame_Video.place(x=10, y=0, width=700, height=340)

x=False
Scroll = Scrollbar(Frame_Music)
playlist = Listbox(Frame_Music, width=100, font=("Times new roman",15), bg="PaleGreen", fg="Maroon", selectbackground="lightblue", cursor="hand2", bd=0, yscrollcommand=Scroll.set)
Scroll.config(command=playlist.yview)
add_music()
Scroll.pack(side=RIGHT,fill=Y)
playlist.pack(side=LEFT,fill=BOTH)
Music_Name=playlist.get(0)

hgbtn=Image.open("hg.jpeg")
hgbtn=hgbtn.resize((700,340))
hgbtn=ImageTk.PhotoImage(hgbtn)
vol_var=1
l2=Label(Frame_Video,image=hgbtn)
l2.place(x=0,y=0)
l1=Label(root,text="Now Playing...\n",width="20",font=("Algerian",20),wraplength=400,bg="LightSeaGreen")
vol=Scale(root,variable=vol_var,from_=0,to=1,orient=HORIZONTAL,resolution=.1,command=set_vl)
vol.set(1)
Button(root,text="Play",command=play_music,font=("Algerian",15),bg="YellowGreen").place(x=10,y=380,width="150",height="50")
Button(root,text="Pause",command=mixer.music.pause,font=("Algerian",15),bg="YellowGreen").place(x=180,y=380,width="150",height="50")
Button(root,text="Resume",command=mixer.music.unpause,font=("Algerian",15),bg="YellowGreen").place(x=10,y=450,width="150",height="50")
Button(root,text="Stop",command=mixer.music.stop,font=("Algerian",15),bg="YellowGreen").place(x=180,y=450,width="150",height="50")
Button(root,text="Gesture Control",command=gesture,font=("Algerian",15),bg="IndianRed").place(x=85,y=520,width="200",height="50")
Button(root,text="Control Manually",command=manually,font=("Algerian",15),bg="IndianRed").place(x=85,y=580,width="200",height="50")
l1.place(x=950,y=400)
vol.place(x=1030,y=580,width="150")
root.mainloop()
mixer.music.stop()
