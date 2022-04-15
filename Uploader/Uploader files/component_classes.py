import os
import sys
import json
import math
import wave
import contextlib
from mutagen.mp3 import MP3
import pygame
import pygame.mixer
from database_functions import *
from tkinter import *
from tkinter import Tk,Frame,LabelFrame, Label, Button,Listbox,Scrollbar,Canvas,PhotoImage,Entry,ttk,StringVar,IntVar,BooleanVar,Menu,Toplevel,filedialog
#from tkScroll
from firebase_admin import storage
from firebase_admin import firestore

#import firebase_admin
#from firebase_admin import credentials
#from firebase_admin import firestore


class New_Pattern_Frame(Frame):
    def __init__(self,master,):
        
        self.master = master
        super().__init__(master)
        self.db = firestore.client()
        
        self.storage= storage.bucket("gchs-lightboard.appspot.com")
        self.type= None
        
        
        self.title_var = StringVar()
        #self.song_id_var = StringVar()
        #self.artist_var=StringVar()
        #self.length = self.song_length()
        #self.min_var = IntVar(value=int(self.length/60))
        
        #TODO rewrite to allow change based on whether uploading new song or reuploading a song
        self.title=Text_Frame(self,"Pattern Title",self.title_var)
        self.pattern_list = Pattern_Frame(self)
        
        button_frame = Frame(self)
        
        frameBuffer=Frame(self,height=10)
        frameBuffer.pack()
        

        
        buttonBuffer=Frame(button_frame,height=20)
        
        self.upload = lambda: add_pattern(self.db,self.storage,self.pattern_list.generate_pattern(),self.title.entry.get())
        
        #15 width
        self.add_button = Button(button_frame, text ="Add Frame", command = self.pattern_list.new_frame)
        self.remove_button = Button(button_frame, text ="Remove Frame", command = self.pattern_list.remove_frame)
        self.upload_button = Button(button_frame, text ="Upload Pattern", command = self.upload)
        
        
        
        buttonBuffer.pack()
        self.add_button.pack()
        self.remove_button.pack()
        self.upload_button.pack()
        
        button_frame.pack(fill='y')
        self.pattern_list.pack(side='top',pady=20)
        
        
        
        
        
        self.pack(expand=True,side='top',fill='both')
        
        
        
        
    def test(self):
        pass


class New_Song_Frame(Frame):
    def __init__(self,master,filename,cred):
        
        self.master = master
        super().__init__(master)
        self.db = firestore.client()
        self.cred=cred

        self.filename=filename
        self.storage= storage.bucket("gchs-lightboard.appspot.com")
        self.type= None
        
        pygame.mixer.init()
        #Must be in seconds
        pygame.mixer.music.load(self.filename)
        pygame.mixer.music.play()
        print(pygame.mixer.music.get_busy())
        
        pygame.mixer.music.stop()
        self.title_var = StringVar()
        self.song_id_var = StringVar(value=os.path.split(os.path.abspath(filename))[1])
        self.artist_var=StringVar()
        self.length = self.song_length()
        self.min_var = IntVar(value=int(self.length/60))
        self.sec_var = IntVar(value=int(self.length%60))
        
        #TODO rewrite to allow change based on whether uploading new song or reuploading a song
        self.title=Text_Frame(self,"Song Title",self.title_var)
        
        #TODO rewrite to allow for program to just use current filename
        
        
        #self.textInput(self.frame,"Song Length (seconds)",self.length_var)
        self.id=Text_Frame(self,"Song Filename",self.song_id_var)
        
        self.artist=Text_Frame(self,"Song Artist",self.artist_var)
        
        #TODO rewrite to allow for program to find length using ffmpeg
        self.length=Time_Frame(self,"Song Length (seconds)",self.min_var,self.sec_var)
        
        button_frame = Frame(self)
        frameBuffer=Frame(self,height=10)
        frameBuffer.pack()
        play_song =lambda: pygame.mixer.music.play()
        stop_song =lambda: pygame.mixer.music.stop()
        buttonBuffer=Frame(button_frame,height=20)
        self.sample_button = Button(button_frame, text ="Sample Audio", command = play_song)
        self.stop_button = Button(button_frame, text ="Stop Audio", command = stop_song)
        
        
        self.upload = lambda:add_music(self.db,self.storage,self.filename,self.title.entry.get(),self.id.entry.get(),
                                       self.artist.entry.get(),self.min_var.get(),self.sec_var.get())
        
        
        
        self.upload_button = Button(button_frame, text ="Upload Audio", command = self.upload)
        
        self.sample_button.pack(side='top')
        
        self.stop_button.pack(side='top')
        buttonBuffer.pack()
        self.upload_button.pack()
        
        button_frame.pack(expand=True,fill='y')
        self.pack(expand=True,side='top',fill='both')
        
    def test(self):
        pass
    def song_length(self):
        """
        if(self.filename.find("mp3")>0):
            audio = MP3(self.filename)
            length= int(audio.info.length)
        """
        if(self.filename.find(".wav")>0):
            with contextlib.closing(wave.open(self.filename,'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = frames / float(rate)
                length = int(duration)
        elif(self.filename.find(".mp3")>0):
            length=MP3(self.filename).info.length
        else:
            length=-1
        return length

class Text_Frame(Frame):
    def __init__(self,master,label_text,var):
        self.master = master
        super().__init__(master)
        
        label = Label(self,text=label_text,anchor='n')
        label.pack(fill='x')
        
        self.entry = Entry(self, bd =5,textvariable=var)
        self.entry.pack()
        self.pack()
        
class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=LEFT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill='both', expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)
        
        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

class Pattern_Frame(Frame):
    def __init__(self,master):
        self.master = master
        super().__init__(master)
        
        
        label = Label(self,text="Pattern",anchor='n')
        label.pack()
        # create a canvas object and a vertical scrollbar for scrolling it
        self.scrolling_frame=VerticalScrolledFrame(self,)
        #self.buffer_frame = Frame(self,height=10)
        self.frame_list=[]
        self.count=1
        
        self.new_frame()
            
        self.scrolling_frame.pack(side='top')
        #self.buffer_frame.pack(side='top',fill='y')
        
    def new_frame(self,length=1):
        for i in range(length):
            frame_frame=Pattern_Info_Frame(self.scrolling_frame.interior,self.count)
                
                
            frame_frame.pack(side='top')
            self.frame_list.append(frame_frame)
            self.count+=1
    def remove_frame(self):
        self.frame_list[-1].destroy()
        self.frame_list.pop(-1)
        self.count-=1
    def generate_pattern(self):
        pattern_array=[]
        for i in range(len(self.frame_list)):
            current_frame=self.frame_list[i]
            frame_array=[]
            
            frame_array.append(current_frame.sec_var.get())
            light_array=[]
            for j in range(len(current_frame.light_list)):
                light_array.append(current_frame.light_list[j].get())
            
            frame_array.append(light_array)
            pattern_array.append(frame_array)
        
        return pattern_array
    
class Pattern_Info_Frame(Frame):
    def __init__(self,master,count):
        self.master = master
        super().__init__(master)
        
        self.sec_var =DoubleVar()
        self.sec_var.set(1)
        count_label = Label(self,text=str(count)+": ",anchor='center',)
        count_label.pack(side='left')
        self.sec = Entry(self,text="0",textvariable=self.sec_var, bd =5,width=5)
        self.sec.pack(side='left')
        
        self.light_list=[]
        
        for i in range(5):
            light_var=IntVar()
            light= Checkbutton(self,variable=light_var,onvalue = 1, offvalue = 0,)
            light.pack(side='left')
            self.light_list.append(light_var)
        
        
class Time_Frame(Frame):
    def __init__(self,master,label_text,min_var,second_var):
        
        self.master = master
        super().__init__(master)
        label = Label(self,text=label_text,anchor='n')
        label.pack(fill='x')
        
        entry_frame = Frame(self)
        
        entry_min = Entry(entry_frame, bd =5,textvariable=min_var,width=5)
        mid_label = Label(entry_frame,text=":",anchor='center',)
        entry_second = Entry(entry_frame, bd =5,textvariable=second_var,width=5)
        
        entry_min.pack(side='left')
        mid_label.pack(side='left')
        entry_second.pack(side='left')
        entry_frame.pack()
        
        self.pack()