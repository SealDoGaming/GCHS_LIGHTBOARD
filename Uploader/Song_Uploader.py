import os
import sys
import json
import math
import ffmpeg
import firebase_admin
from firebase_admin import credentials

from tkinter import *
from tkinter import Tk,Frame,LabelFrame, Label, Button,Listbox,Scrollbar,Canvas,PhotoImage,Entry,ttk,StringVar,IntVar,BooleanVar,Menu,Toplevel,filedialog
from PIL import ImageTk, Image

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, r"Uploader files")
service_dir = os.path.join(data_dir, r"ServiceFolder")

sys.path.append(data_dir)
sys.path.append(service_dir)

from component_classes import *

cred = credentials.Certificate(os.path.join(service_dir,"gchs-lightboard-firebase-adminsdk-h2sjx-36d8c33c48.json"))
firebase_admin.initialize_app(cred)




class MyApplication:
    def __init__(self, master):
        self.master = master
        
        master.title("Song Uploading Program")
        master.geometry("700x400")
        self.menubar = Menu(master)
        
        self.current_menu=None
        
        master.config(menu= self.menubar)
        # display the menu
        self.filemenu = Menu(self.menubar, tearoff=0)
        
        self.filemenu.add_command(label="Upload New Song", command=self.new_song_upload)
        self.filemenu.add_command(label="Upload New Pattern", command=self.new_pattern_upload)
        
        """
        self.filemenu.add_command(label="Open", command=self.open_level)
        self.filemenu.add_command(label="Save", command=self.save_level)
        self.filemenu.add_separator()
        #add a way to clear grid and level
        self.filemenu.add_command(label="Exit", command=root.quit)
        
        """
        
        self.menubar.add_cascade(label="Upload Song", menu=self.filemenu)
        self.editmenu = Menu(self.menubar, tearoff=0)
        
    
        
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        
        self.frame = Frame(master,)
        self.frame.pack(expand=True,fill='both')
        
        topBuffer=Frame(self.frame,height=10)
        topBuffer.pack(side='top',fill='x')
        
        
        #Make this whole section into its own initialization function later so that by pressing Upload New Song, it will be brought to here.
        
        
        
    def new_song_upload(self):
        if(self.current_menu!=None):
            self.current_menu.forget()
            self.current_menu.destroy()
        
        self.current_menu=New_Song_Frame(self.frame,self.file_select(),cred)
    def new_pattern_upload(self):
        if(self.current_menu!=None):
            self.current_menu.forget()
            self.current_menu.destroy()
        
        #self.current_menu=New_Pattern_Frame(self.frame,self.file_select(),cred)
        self.current_menu=New_Pattern_Frame(self.frame)
    
    def file_select(self):
        #filename = filedialog.askopenfilename(initialdir =  level_dir, title = "Select A Song", filetype =(("Text files","*.txt*"), ("all files","*.*")))
        filename = filedialog.askopenfilename(initialdir =  "/Downloads/", title = "Select A Song", filetype =(("MP3 (.mp3)","*.mp3*"),("Waveform files (.wav)","*.wav*"),("Ogg files (.ogg)","*.ogg*"))) 
        return filename
        
        
        
    def on_delete(self):
        pygame.mixer.quit()
        self.master.destroy()
    def test(self):
        pass
        

root = Tk()
app = MyApplication(root)
root.wm_protocol ("WM_DELETE_WINDOW", app.on_delete)
root.mainloop()
