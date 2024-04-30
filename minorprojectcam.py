import numpy 
import cv2 
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from tkinter import messagebox, filedialog

def createwidgets():
    root.feedlabel = Label(root, bg="steelblue", fg="white", text="WEBCAM FEED", font=('Comic Sans MS',20))
    root.feedlabel.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

    root.cameraLabel = Label(root, bg="steelblue", borderwidth=3, relief="groove")
    root.cameraLabel.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

    root.saveLocationEntry = Entry(root, width=55, textvariable=destPath)
    root.saveLocationEntry.grid(row=3, column=1, padx=10, pady=10)

    root.browseButton = Button(root, width=10, text="BROWSE", command=destBrowse)
    root.browseButton.grid(row=3, column=2, padx=10, pady=10)

    root.captureBTN = Button(root, text="CAPTURE", command=Capture, bg="LIGHTBLUE", font=('Comic Sans MS',15), width=20)
    root.captureBTN.grid(row=4, column=1, padx=10, pady=10)

    root.CAMBTN = Button(root, text="STOP CAMERA", command=StopCAM, bg="LIGHTBLUE", font=('Comic Sans MS',15), width=13)
    root.CAMBTN.grid(row=4, column=2)

    root.previewlabel = Label(root, bg="steelblue", fg="white", text="IMAGE PREVIEW", font=('Comic Sans MS',20))
    root.previewlabel.grid(row=1, column=4, padx=10, pady=10, columnspan=2)

    root.imageLabel = Label(root, bg="steelblue", borderwidth=3, relief="groove")
    root.imageLabel.grid(row=2, column=4, padx=10, pady=10, columnspan=2)

    root.openImageEntry = Entry(root, width=55, textvariable=imagePath)
    root.openImageEntry.grid(row=3, column=4, padx=10, pady=10)

    root.openImageButton = Button(root, width=10, text="BROWSE", command=imageBrowse)
    root.openImageButton.grid(row=3, column=5, padx=10, pady=10)

    ShowFeed()

def ShowFeed():
    ret, frame = root.cap.read()

    if ret:
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (20,30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        videoImg = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=videoImg)
        root.cameraLabel.configure(image=imgtk)
        root.cameraLabel.imgtk = imgtk
        root.cameraLabel.after(10, ShowFeed)
    else:
        root.cameraLabel.configure(image='')

def destBrowse():
    destDirectory = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH")
    destPath.set(destDirectory)

def imageBrowse():
    openDirectory = filedialog.askopenfilename(initialdir="YOUR DIRECTORY PATH")
    imagePath.set(openDirectory)
    imageView = Image.open(openDirectory)
    imageResize = imageView.resize((640, 480), Image.ANTIALIAS)
    imageDisplay = ImageTk.PhotoImage(imageResize)
    root.imageLabel.config(image=imageDisplay)
    root.imageLabel.photo = imageDisplay

def Capture():
    image_name = datetime.now().strftime('%d-%m-%Y %H-%M-%S')

    if destPath.get() != '':
        image_path = destPath.get()
    else:
        messagebox.showerror("ERROR", "NO DIRECTORY SELECTED TO STORE IMAGE!!")

    imgName = image_path + '/' + image_name + ".jpg"


    ret, frame = root.cap.read()

    cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (430,460), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))

    success = cv2.imwrite(imgName, frame)

    saved_image = Image.open(imgName)
    saved_image = ImageTk.PhotoImage(saved_image)
    root.imageLabel.config(image=saved_image)
    root.imageLabel.photo = saved_image

    if success:
        messagebox.showinfo("SUCCESS", "IMAGE CAPTURED AND SAVED IN " + imgName)

def StopCAM():
    root.cap.release()
    root.CAMBTN.config(text="START CAMERA", command=StartCAM)
    root.cameraLabel.config(text="OFF CAM", font=('Comic Sans MS',70))

def StartCAM():
    root.cap = cv2.VideoCapture(0)
    width_1, height_1 = 640, 480
    root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width_1)
    root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height_1)
    root.CAMBTN.config(text="STOP CAMERA", command=StopCAM)
    root.cameraLabel.config(text="")
    ShowFeed()

root = tk.Tk()
root.cap = cv2.VideoCapture(0)
width, height = 640, 480
root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
root.title("Pycam")
root.geometry("1340x700")
root.resizable(True, True)
root.configure(background="sky blue")

destPath = StringVar()
imagePath = StringVar()

createwidgets()
root.mainloop()
