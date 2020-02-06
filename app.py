import tkinter as tk
import cv2
from segment import segmenter

from tkinter import filedialog
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
image_to_segment = cv2.imread(file_path)
segmenter(image_to_segment)

