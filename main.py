from tkinter import *
from tkinter import ttk, filedialog
from tkinter.ttk import Combobox
from pydub import AudioSegment
import tkinter as tk

import pyttsx3
import speech_recognition as sr
import PyPDF2
from gtts import gTTS
from playsound import playsound
from googletrans import Translator
import os


# ==== Setup ====
root = Tk()
root.title("Text tool")
root.geometry("1030x570")
root.config(bg="#ade4e9")

# Layout responsiveness
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=1)

framebg = "#2995bb"     
bodybg = "#ade4e9"

# ==== Resources ====

image_icon = PhotoImage(file="Images/icon.png")
logo_icon = PhotoImage(file="Images/icon.png")
speak = PhotoImage(file="Images/speak.png")
download = PhotoImage(file="Images/download.png")
pdf = PhotoImage(file="Images/pdfimage.png")
trans = PhotoImage(file="Images/trans.png")
speak2 = PhotoImage(file="Images/otherspeaker.png")
mic = PhotoImage(file="Images/mic.png")

root.iconphoto(False, image_icon)

# ==== Top Bar ====
top_frame = Frame(root, bg=framebg)
top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
top_frame.grid_columnconfigure(1, weight=1)

Label(top_frame, image=logo_icon, bg=framebg).grid(row=0, column=0, rowspan=2, padx=20)
Label(top_frame, text="ECHO", font="arial 20 bold", bg=framebg, fg="#fff").grid(row=0, column=1, sticky="w")

combo1 = ttk.Combobox(top_frame, values=["English","Hindi"], font="Roboto 10", state='r', width=10)
combo1.set("ENGLISH")
combo1.grid(row=1, column=1, sticky="w", padx=(10, 0))

languageV = list({'en': 'English', 'hi': 'Hindi', 'fr': 'french'}.values())
combo = ttk.Combobox(top_frame, values=languageV, font="Roboto 10", state='r', width=10)
combo.set("ENGLISH")
combo.grid(row=1, column=1, padx=(130, 0), sticky="w")

transimg = Button(top_frame, image=trans, bg=framebg, bd=0)
transimg.grid(row=0, column=2, padx=5, sticky="e")

uplode = Button(top_frame, image=pdf, bg=framebg, bd=0)
uplode.grid(row=0, column=4, padx=5, sticky="e")


# ==== Text Areas ====
text_frame = Frame(root, bg=bodybg)
text_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
text_frame.grid_rowconfigure(0, weight=1)
text_frame.grid_rowconfigure(1, weight=1)
text_frame.grid_columnconfigure(0, weight=1)

def add_placeholder(event=None):
    if text_area.get("1.0", "end-1c").strip() == "":
        text_area.insert("1.0", "Enter your text here 😊...")
        text_area.config(fg="gray")

def remove_placeholder(event=None):
    if text_area.get("1.0", "end-1c").strip() == "Enter your text here 😊...":
        text_area.delete("1.0", "end")
        text_area.config(fg="black")

text_area = Text(text_frame, font="Robote 14", bg="#d9eeef", relief=GROOVE, wrap=WORD)
text_area.grid(row=0, column=0, sticky="nsew", padx=(0, 40), pady=(0, 5))

add_placeholder()
text_area.bind("<FocusIn>", remove_placeholder)
text_area.bind("<FocusOut>", add_placeholder)

text_area1 = Text(text_frame, font="Robote 14", bg="#d9eeef", relief=GROOVE, wrap=WORD)
text_area1.grid(row=1, column=0, sticky="nsew", padx=(0, 40), pady=(5, 0))



# ==== Sidebar ====
sidebar = Frame(root, bg=bodybg)
sidebar.grid_propagate(False)
sidebar.config(width=280)
sidebar.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

Label(sidebar, text="VOICE", font="arial 15 bold", bg=bodybg, fg="#59bd61").grid(row=0, column=0, sticky="w", pady=(10, 5))
gender_combobox = Combobox(sidebar, values=['Male', 'Female'], font="arial 14", state="r", width=10)
gender_combobox.set("Female")
gender_combobox.grid(row=1, column=0, sticky="w", pady=(0, 10))

Label(sidebar, text="SPEED", font="arial 15 bold", bg=bodybg, fg="#59bd61").grid(row=2, column=0, sticky="w", pady=(10, 5))

current_value = tk.DoubleVar()
current_value.set(100)

def get_current_value():
    base_speed = 100  
    multiplier = current_value.get() / base_speed
    return f"{multiplier:.1f}x"

def slider_changed(event):
    value_label.config(text=get_current_value())

slider = ttk.Scale(root, from_=50, to=200, orient="horizontal", command=slider_changed, variable=current_value)


Label(sidebar, text="SPEED", font="arial 15 bold", bg=bodybg, fg="#59bd61").grid(row=2, column=0, sticky="w", pady=(10, 5))
style=ttk.Style()
style.configure("TScale", background=bodybg)
slider = ttk.Scale(sidebar, from_=30, to=250, orient="horizontal", command=slider_changed, variable=current_value)
slider.grid(row=3, column=0, sticky="ew", padx=(0.10), pady=(0, 5))
value_label = ttk.Label(sidebar, text=get_current_value())
value_label.grid(row=3, column=1, padx=(5, 0), sticky="w")

value_label = ttk.Label(sidebar, text=get_current_value())
value_label.grid(row=3, column=1, padx=(5, 0), sticky="w")

speakbtn = Button(sidebar, compound=LEFT, image=speak, width=130, bg=bodybg, bd=0)
speakbtn.grid(row=4, column=0, pady=(30, 10), sticky="w")

save = Button(sidebar, compound=LEFT, image=download, width=130, bg=bodybg, bd=0)
save.grid(row=5, column=0, pady=10, sticky="w")

# ==== Functionality ====
engine = pyttsx3.init()
def speaknow():
    text = text_area.get(1.0, END).strip()
    gender = gender_combobox.get()
    speed = current_value.get()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id if gender == 'Male' else voices[1].id)
    engine.setProperty('rate', speed)
    engine.say(text)
    engine.runAndWait()
speakbtn.config(command=speaknow)

translator = Translator()
def translate_text():
    src = combo1.get().lower()
    dest = combo.get().lower()
    text = text_area.get(1.0, END).strip()
    result = translator.translate(text, src=src, dest=dest)
    text_area1.delete(1.0, END)
    text_area1.insert(END, result.text)
transimg.config(command=translate_text)

# def recognize_speech():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         try:
#             text_area.delete(1.0, END)
#             text_area.insert(END, "Listening...")
#             audio = r.listen(source)
#             result = r.recognize_google(audio)
#             text_area.delete(1.0, END)
#             text_area.insert(END, result)
#         except:
#             text_area.delete(1.0, END)
#             text_area.insert(END, "Could not recognize speech.")
# micBtn.config(command=recognize_speech)

def save_audio():
    text = text_area.get(1.0, END).strip()
    if text:
        tts = gTTS(text=text, lang='en')
        filename = "voice.mp3"
        tts.save(filename)
        playsound(filename)
        os.remove(filename)
save.config(command=save_audio)


def read_pdf():
    path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not path: return
    with open(path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        extracted = "".join([p.extract_text() for p in reader.pages])
    text_area.delete(1.0, END)
    text_area.insert(END, extracted)
uplode.config(command=read_pdf)

# ==== Run ====
root.mainloop()
