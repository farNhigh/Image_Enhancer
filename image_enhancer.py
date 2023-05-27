import os
import time
import datetime
from PIL import Image, ImageEnhance
import tkinter as tk
from tkinter import Tk, Button
from tkinter import filedialog
from tkinter import messagebox
import pygame
from pygame import mixer
import pygame_gui
import locale

# SIZE PARAMETERS
window_size = width, height = (800, 600)
button_size1 = b_width, b_height = (150, 50)
button_size2 = b_width, b_height = (80, 50)
margin = 15

pygame.init()
pygame.display.set_caption("Image Enhancer")
window_surface = pygame.display.set_mode(window_size)

# INITIALIZE UI
gradient_surface = pygame.Surface((width, height))
for y in range(height):
    r = int((255 * y) / height)
    g = int((255 * y) / height)
    b = 0
    gradient_surface.fill((r, g, b), (0, y, width, 1))
manager = pygame_gui.UIManager(window_size)

# Load the image
image1 = pygame.image.load("uk_flag.png")
image2 = pygame.image.load("ro_flag.png")
image3 = pygame.image.load("image_enhancer.png")

# Resize the image to 64x64 pixels
image1 = pygame.transform.scale(image1, (60, 45))
image2 = pygame.transform.scale(image2, (60, 45))
image3 = pygame.transform.scale(image3, (80, 80))

# Initial position of the image
image1_x = 30
image1_y = 125
image2_x = 100
image2_y = 125
image3_x = 705
image3_y = 420

# CREATE GUI WIDGETS
browse_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 454), button_size1),
                                           text="Browse",
                                           manager=manager)
enhance_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 501), button_size1),
                                             text="Enhance",
                                             manager=manager)
language_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((20, 70), button_size1),
                                              text="Change Language",
                                              manager=manager)
about_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((705, 501), button_size2),
                                             text="About",
                                             manager=manager)
brightness_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((20, 240), (764, 20)),
                                                          start_value=1.2,
                                                          value_range=(0.0, 3.0),
                                                          manager=manager)
contrast_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((20, 310), (764, 20)),
                                                        start_value=1.2,
                                                        value_range=(0.0, 3.0),
                                                        manager=manager)
sharpness_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((20, 380), (764, 20)),
                                                         start_value=1.2,
                                                         value_range=(0.0, 3.0),
                                                         manager=manager)
clock = pygame.time.Clock()


def select_file():
    global file_path
    root1 = tk.Tk()
    root1.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Pictures", "*.jpeg;*.jpg;*.png;*.gif;*.bmp;*.tiff;*.tif;*.webp;*.svg")])
    if file_path:
        enhance_button.enable()

def enhance_image():
    global file_path, brightness_value, contrast_value, sharpness_value
    if file_path:
        try:
            image = Image.open(file_path)
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(brightness_value)
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(contrast_value)
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(sharpness_value)
            image.save("enhanced_image.jpg")
            messagebox.showinfo("Success", "Image enhancement successful!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during image enhancement:\n{str(e)}")

        # Update the displayed image
        global enhanced_image
        enhanced_image = pygame.image.load("enhanced_image.jpg")
        enhanced_image = pygame.transform.scale(enhanced_image, (200, 200))
        window_surface.blit(enhanced_image, (350, 240))

def show_about():
    if language == "English":
        messagebox.showinfo("About", "This software was created by Ionut-Alexandru VIZUROIU.\nContact alexandru.vizuroiu@gmail.com for further info.")
    if language == "Romanian":
        messagebox.showinfo("Despre", "Acest software a fost creat de Ionut-Alexandru VIZUROIU.\nPentru mai multe informații: alexandru.vizuroiu@gmail.com.")

# Function to update the language
def update_language():
    global language
    if language == "English":
        browse_button.set_text(text="Browse")
        enhance_button.set_text(text="Enhance")
        language_button.set_text(text="Change Language")
        about_button.set_text(text="About")
    elif language == "Romanian":
        browse_button.set_text(text="Încarcă")
        enhance_button.set_text(text="Optimizează")
        language_button.set_text(text="Schimbă limba")
        about_button.set_text(text="Despre")

# Function to handle language change events
def handle_language_change():
    global language
    if language == "English":
        language = "Romanian"
    else:
        language = "English"
    update_language()

# STATE PARAMETERS
language = "English"
file_path = None
brightness_value = 1.2
contrast_value = 1.2
sharpness_value = 1.2
enhance_button.disable()

is_running = True
while is_running:

    # update display
    time_delta = clock.tick(60) / 900.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == enhance_button:
                enhance_image()
            elif event.ui_element == browse_button:
                select_file()
            elif event.ui_element == language_button:
                handle_language_change()
            elif event.ui_element == about_button:
                show_about()
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == brightness_slider:
                brightness_value = event.value
            elif event.ui_element == contrast_slider:
                contrast_value = event.value
            elif event.ui_element == sharpness_slider:
                sharpness_value = event.value

        manager.process_events(event)

    manager.update(time_delta)
    window_surface.blit(gradient_surface, (0, 0))
    manager.draw_ui(window_surface)

    locale.setlocale(locale.LC_TIME, 'en-US')

    current_time = time.strftime("%H:%M:%S", time.localtime())
    current_date = datetime.date.today().strftime("%b %d %Y")
    font = pygame.font.SysFont(None, 40)
    date_text_surface = font.render(current_date, True, (55, 255, 255))
    time_text_surface = font.render(current_time, True, (55, 255, 255))
    date_x = width - date_text_surface.get_width() - 20
    time_x = width - time_text_surface.get_width() - 20

    window_surface.blit(image1, (image1_x, image1_y))
    window_surface.blit(image2, (image2_x, image2_y))
    window_surface.blit(image3, (image3_x, image3_y))
    window_surface.blit(date_text_surface, (date_x, 70))
    window_surface.blit(time_text_surface, (time_x, 110))

    # Render the slider values
    brightness_label = font.render(f"Brightness: {brightness_value:.2f}", True, (255, 255, 255))
    contrast_label = font.render(f"Contrast: {contrast_value:.2f}", True, (255, 255, 255))
    sharpness_label = font.render(f"Sharpness: {sharpness_value:.2f}", True, (255, 255, 255))
    window_surface.blit(brightness_label, (20, 260))
    window_surface.blit(contrast_label, (20, 330))
    window_surface.blit(sharpness_label, (20, 400))
    
    pygame.display.update()

pygame.quit()
