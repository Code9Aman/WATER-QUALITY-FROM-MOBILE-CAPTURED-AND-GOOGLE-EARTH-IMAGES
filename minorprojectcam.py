import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from tkinter import messagebox, filedialog

def create_widgets():
    root.feed_label = Label(root, bg="steelblue", fg="white", text="WEBCAM FEED", font=('Comic Sans MS', 20))
    root.feed_label.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

    root.camera_label = Label(root, bg="steelblue", borderwidth=3, relief="groove")
    root.camera_label.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

    root.save_location_entry = Entry(root, width=55, textvariable=dest_path)
    root.save_location_entry.grid(row=3, column=1, padx=10, pady=10)

    root.browse_button = Button(root, width=10, text="BROWSE", command=browse_destination)
    root.browse_button.grid(row=3, column=2, padx=10, pady=10)

    root.capture_btn = Button(root, text="CAPTURE", command=capture_image, bg="LIGHTBLUE", font=('Comic Sans MS', 15), width=20)
    root.capture_btn.grid(row=4, column=1, padx=10, pady=10)

    root.cam_btn = Button(root, text="STOP CAMERA", command=stop_camera, bg="LIGHTBLUE", font=('Comic Sans MS', 15), width=13)
    root.cam_btn.grid(row=4, column=2)

    root.preview_label = Label(root, bg="steelblue", fg="white", text="IMAGE PREVIEW", font=('Comic Sans MS', 20))
    root.preview_label.grid(row=1, column=4, padx=10, pady=10, columnspan=2)

    root.image_label = Label(root, bg="steelblue", borderwidth=3, relief="groove")
    root.image_label.grid(row=2, column=4, padx=10, pady=10, columnspan=2)

    root.open_image_entry = Entry(root, width=55, textvariable=image_path)
    root.open_image_entry.grid(row=3, column=4, padx=10, pady=10)

    root.open_image_button = Button(root, width=10, text="BROWSE", command=browse_image)
    root.open_image_button.grid(row=3, column=5, padx=10, pady=10)

    show_feed()

def show_feed():
    ret, frame = root.cap.read()

    if ret:
        frame = cv2.flip(frame, 1)
        cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (20, 30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 255))
        cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        video_img = Image.fromarray(cv2_image)
        imgtk = ImageTk.PhotoImage(image=video_img)
        root.camera_label.configure(image=imgtk)
        root.camera_label.imgtk = imgtk
        root.camera_label.after(10, show_feed)
    else:
        root.camera_label.configure(image='')

def browse_destination():
    dest_directory = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH")
    dest_path.set(dest_directory)

def browse_image():
    open_directory = filedialog.askopenfilename(initialdir="YOUR DIRECTORY PATH")
    image_path.set(open_directory)
    image_view = Image.open(open_directory)
    image_resize = image_view.resize((640, 480), Image.ANTIALIAS)
    image_display = ImageTk.PhotoImage(image_resize)
    root.image_label.config(image=image_display)
    root.image_label.photo = image_display

def capture_image():
    image_name = datetime.now().strftime('%d-%m-%Y %H-%M-%S')

    if dest_path.get() != '':
        image_path_ = dest_path.get()
    else:
        messagebox.showerror("ERROR", "NO DIRECTORY SELECTED TO STORE IMAGE!!")

    img_name = image_path_ + '/' + image_name + ".jpg"

    ret, frame = root.cap.read()

    cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (430, 460), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 255))

    success = cv2.imwrite(img_name, frame)

    saved_image = Image.open(img_name)
    saved_image = ImageTk.PhotoImage(saved_image)
    root.image_label.config(image=saved_image)
    root.image_label.photo = saved_image

    if success:
        messagebox.showinfo("SUCCESS", "IMAGE CAPTURED AND SAVED IN " + img_name)

def stop_camera():
    root.cap.release()
    root.cam_btn.config(text="START CAMERA", command=start_camera)
    root.camera_label.config(text="OFF CAM", font=('Comic Sans MS', 70))

def start_camera():
    root.cap = cv2.VideoCapture(0)
    width_1, height_1 = 640, 480
    root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width_1)
    root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height_1)
    root.cam_btn.config(text="STOP CAMERA", command=stop_camera)
    root.camera_label.config(text="")
    show_feed()

root = tk.Tk()
root.cap = cv2.VideoCapture(0)
width, height = 640, 480
root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
root.title("Pycam")
root.geometry("1340x700")
root.resizable(True, True)
root.configure(background="sky blue")

dest_path = StringVar()
image_path = StringVar()

create_widgets()
root.mainloop()
