#!/usr/bin/env python
import tkinter as tk
from tkinter import IntVar
from tkinter.colorchooser import askcolor   
from tkinter.filedialog import askopenfilename,asksaveasfilename
from tkinter import messagebox
from PIL import ImageTk, Image
import speech_recognition as sr
import asyncio
from tkinter.ttk import *
from tkfontchooser import askfont
import tkinter.font as tkFont
import gtts
import threading, time
from myimages import *
import pyttsx3

#for speaker
engine=pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id) #you can choose the voice by changing the array index

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

class Task(threading.Thread):
    def __init__(self, master, task):
        threading.Thread.__init__(self, target=task, args=(master,))

        if not hasattr(master, 'thread_enviar') or not master.thread_enviar.is_alive():
            master.thread_enviar = self
            self.start()
def enviar(master):
    if 0:
        pass
    else:
        #master.pg_bar.start(500) 
        pg.start(100)
        open_audio()
        pg.stop()

def enviar1(master):
    if 0:
        pass
    else:
        #master.pg_bar.start(500)
        pg.start(100)
        text_to_speech()
        pg.stop()

def enviar2(master):
    if 0:
        pass
    else:
        #master.pg_bar.start(500)
        pg.start(100)
        read_text()
        pg.stop()

# a function for handling the saving of file part
def save_file():
    filepath=asksaveasfilename(defaultextension="txt",filetypes=[("Text Files","*.txt"),("All Files","*.*")],)
    if not filepath:
         return
    with open(filepath,"w") as output_file:
         text=txt_edit.get(1.0,tk.END)
         output_file.write(text)
    window.title(f"speakNotes - {filepath}")

def open_file():
    filepath = askopenfilename(
       filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if not filepath:
       return
    txt_edit.delete("1.0", tk.END)
    with open(filepath, "r") as input_file:
         text = input_file.read()
         txt_edit.insert(tk.END, text)
    window.title(f"speakNotes - {filepath}")

def open_audio():
    filepath = askopenfilename(
       filetypes=[("Audio Files", ".wav .ogg"), ("All Files", "*.*")])
    if not filepath:
       return
    txt_edit.delete("1.0", tk.END)
    with open(filepath, "rb") as input_file:
         harvard = sr.AudioFile(input_file)
         with harvard as source:
              audio=recognizer.record(source)
              text=recognizer.recognize_wit(audio,key=YOUR_WIT_ID)
              txt_edit.insert(tk.END, text)
    window.title(f"Transcibe Audio to Text - {filepath}")

# a function for handling speech to text part
async def speech_to_text():
    if not isinstance(recognizer,sr.Recognizer):
       raise TypeError("something's not right!")
    if not isinstance(microphone,sr.Microphone):
       raise TypeError("something's not right!")
    text=""
    with microphone as source:
         recognizer.adjust_for_ambient_noise(source)
         audio = recognizer.listen(source)
         text = recognizer.recognize_wit(audio,key=YOUR_WIT_ID)
         #txt_edit.insert(tk.END,text)
    return text

# function for handling the above mentioned function asynchronously(means making it fast)
def speech_to_text_helper():
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
      text = loop.run_until_complete(speech_to_text())
      text = text+" "
      txt_edit.insert(tk.END,text)
# function for changing color of text written in notepad
def change_color():
    val=var.get()
    result = askcolor(color="#6A9662",title = "Color Chooser")
    req = result[1]
    if val==1:
       txt_edit.configure(fg=req)
    elif val==2:
       txt_edit.configure(bg=req)

def font_chooser():
    font = askfont(window)
    if font:
        textFont = tkFont.Font(family=font['family'],size=font['size'],weight=font['weight'],slant=font['slant'])
        txt_edit.configure(font=textFont)

def choose_option():
    win=tk.Toplevel()
    win.wm_title("Choose an option..")
    win.geometry("175x175")
    r1 = Radiobutton(win,text="Text Colour",variable=var,value=1,command=change_color)
    r2 = Radiobutton(win,text="Background Color",variable=var,value=2,command=change_color)
    r3 = Radiobutton(win,text="Font style",variable=var,value=3,command=font_chooser)
    r1.pack(side=tk.TOP,ipady=5) 
    r2.pack(side=tk.TOP,ipady=5) 
    r3.pack(side=tk.TOP)


#function to instruct what to do when a user clicks close button
def on_closing():
    MsgBox = tk.messagebox.askquestion("You wanna leave already?","Are you sure about exiting?",icon="warning")
    if MsgBox == "yes":
       window.destroy()

def notepad():
     # frame and text area placement on the app window
    home_page.grid_remove()
    fr_buttons.grid(row=0,column=0,sticky="ns")
    txt_edit.grid(row=0,column=1,sticky="nsew")
    fr_pg.grid(row=1,column=1,sticky="nsew")

def back():
    fr_buttons.grid_remove()
    txt_edit.grid_remove()
    fr_pg.grid_remove()
    home_page.grid(row=0,column=1,sticky="ns")

def text_to_speech():
    filepath=asksaveasfilename(defaultextension="txt",filetypes=[("Audio Files","*.mp3"),("All Files","*.*")],)
    if not filepath:
         return
    text=txt_edit.get(1.0,tk.END)
    tts = gtts.gTTS(text)
    tts.save(filepath)
    window.title(f"speakNotes - {filepath}")

def read_text():
    speak(txt_edit.get(1.0,tk.END))


#defining window and title of application
window = tk.Tk()
window.title("speakNotes")
var = IntVar()
textFont = ""
#some dimension configuration for the window
window.rowconfigure(0,minsize=600,weight=1)
window.columnconfigure(1,minsize=700,weight=1)

#images
saveStr = save2STR
welcomeStr = welcomeSTR
openStr = openSTR
micStr = micSTR
paintStr = paintSTR
save_img = tk.PhotoImage(data=saveStr)
open_img = tk.PhotoImage(data=openStr)
mic_img = tk.PhotoImage(data=micStr)
paint_img = tk.PhotoImage(data=paintStr)
welcome_img = tk.PhotoImage(data=welcomeStr)
#endImages

txt_edit=tk.Text(window) #the text field which acts as the notepad input area

fr_buttons = tk.Frame(window) # a frame to hold all the buttons of our application

fr_pg = tk.Frame(window)# a frame to hold a progress bar


home_page = tk.Frame(window,width=600, height=700)
home_page.grid(row=0,column=1,sticky="ns")

greet = tk.Label(master=home_page,image=welcome_img)

greet.grid(row=0,column=0,sticky="ew",padx=5,pady=60)
nxt_btn = tk.Button(master=home_page,text="Next>>",command=notepad,bg="#00ffff")
nxt_btn.grid(row=1,column=0,sticky="ew",padx=5)

recognizer=sr.Recognizer() # a speech recognizer object
microphone=sr.Microphone() # a speech input device object

#pg_begin
pg = Progressbar(fr_pg,orient=tk.HORIZONTAL,length=700,mode='determinate')
pg.grid(row=0,column=0,padx=10,pady=10)
#pg_end

#btnBegin
btn_back = tk.Button(fr_buttons,text="<<Back",command=back,bg="#00ffff")
btn_open = tk.Button(fr_buttons,image=open_img,command=open_file)
btn_save = tk.Button(fr_buttons,command=save_file,image=save_img)
btn_speak = tk.Button(fr_buttons,image=mic_img,command=speech_to_text_helper)
btn_paint = tk.Button(fr_buttons,image=paint_img,command=choose_option)
btn_audioToTxt = tk.Button(fr_buttons,text="Audio To Text",command=lambda :Task(window, enviar))
btn_txtToaudio = tk.Button(fr_buttons,text="Text To Audio",command=lambda :Task(window, enviar1))
btn_txtRead = tk.Button(fr_buttons,text="Read Text",command=lambda :Task(window, enviar2))
#btnEnd

#btn placement on the window
btn_open.grid(row=0,column=0,sticky="ew",padx=5,pady=5)
btn_save.grid(row=1,column=0,sticky="ew",padx=5,pady=10)
btn_speak.grid(row=2,column=0,sticky="ew",padx=5,pady=10)
btn_paint.grid(row=3,column=0,sticky="ew",padx=5,pady=10)
btn_audioToTxt.grid(row=4,column=0,sticky="ew",padx=5,pady=10)
btn_txtToaudio.grid(row=5,column=0,sticky="ew",padx=5,pady=10)
btn_txtRead.grid(row=6,column=0,sticky="ew",padx=5,pady=10)
btn_back.grid(row=7,column=0,sticky="ew",padx=5)


window.protocol("WM_DELETE_WINDOW", on_closing)
# main event loop of our function
window.mainloop()
