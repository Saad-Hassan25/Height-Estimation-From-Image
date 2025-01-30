
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def calculate_person_height(image_path, reference_object_height):
    image = cv2.imread(image_path)
    if image is None:
        messagebox.showerror("Error", "Image not found!")
        return
    
    max_height = 800
    scale_factor = 1
    if image.shape[0] > max_height:
        scale_factor = max_height / image.shape[0]
        image = cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    messagebox.showinfo("ROI Selection", "Please select the object in the image you want to calculate the height for.")
    person_box = cv2.selectROI("Select Object/Person", image)
    person_height_pixels = person_box[3]

    if person_height_pixels == 0:
        messagebox.showerror("Error", "No person selected. Exiting...")
        return

    messagebox.showinfo("ROI Selection", "Please select the reference object (e.g., door) in the image.")
    reference_box = cv2.selectROI("Select Reference Object", image)
    reference_height_pixels = reference_box[3]

    if reference_height_pixels == 0:
        messagebox.showerror("Error", "No reference object selected. Exiting...")
        return

    pixel_to_real_ratio = reference_object_height / reference_height_pixels
    person_height_real = person_height_pixels * pixel_to_real_ratio

    messagebox.showinfo("Result", f"Estimated height of the person: {person_height_real:.2f} meters")

    cv2.rectangle(image, (int(person_box[0]), int(person_box[1])), 
                         (int(person_box[0] + person_box[2]), int(person_box[1] + person_box[3])), 
                         (255, 0, 0), 2)
    cv2.rectangle(image, (int(reference_box[0]), int(reference_box[1])), 
                         (int(reference_box[0] + reference_box[2]), int(reference_box[1] + reference_box[3])), 
                         (0, 255, 0), 2)

    cv2.imshow("Selected Areas", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def select_image():
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if image_path:
        load_image(image_path)

def load_image(image_path):
    image = Image.open(image_path)
    image.thumbnail((400, 400))
    img = ImageTk.PhotoImage(image)
    panel.config(image=img)
    panel.image = img
    measure_button.config(state=tk.NORMAL)

def reset_selection():
    panel.config(image='')
    panel.image = None
    measure_button.config(state=tk.DISABLED)
    global image_path
    image_path = None

root = tk.Tk()
root.title("Height Measurement Tool")

image_path = None

frame = tk.Frame(root)
frame.pack(pady=10)

select_button = tk.Button(frame, text="Select Image", command=select_image)
select_button.pack(side="left", padx=10)

measure_button = tk.Button(frame, text="Measure Height", command=lambda: calculate_person_height(image_path, 2.74), state=tk.DISABLED)
measure_button.pack(side="left", padx=10)

reset_button = tk.Button(frame, text="Discard Image", command=reset_selection)
reset_button.pack(side="left", padx=10)

panel = tk.Label(root)
panel.pack(pady=10)

root.mainloop()
