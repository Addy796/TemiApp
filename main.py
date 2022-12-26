import kivy
kivy.require('1.11.1') # specify the Kivy version

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

import os
import cv2
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

class MyApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text='Enter your email address:')
        self.layout.add_widget(self.label)

        self.email_input = TextInput(text='', multiline=False)
        self.layout.add_widget(self.email_input)

        self.take_picture_button = Button(text='Take Picture', on_press=self.take_picture)
        self.layout.add_widget(self.take_picture_button)

        return self.layout

    def take_picture(self, instance):
        # Capture an image using the TEMI robot's camera
        cap = cv2.VideoCapture(0)
        ret, image = cap.read()
        cap.release()
        cv2.destroyAllWindows()

        # Save the image to a file
        image_path = 'captured_image.jpg'
        cv2.imwrite(image_path, image)

        # Get the email address entered by the user
        email_address = self.email_input.text

        # Send the image to the email address
        self.send_email(email_address, image_path)

    def send_email(self, email_address, image_path):
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = 'robottemi2022@gmail.com'
        msg['To'] = email_address
        msg['Subject'] = 'Image report during Safety Walk'

        # Open the image file and attach it to the email
        with open(image_path, 'rb') as f:
            img = MIMEImage(f.read())
            msg.attach(img)

        # Send the email using SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('robottemi2022@gmail.com', "zzsrkojnfsmiungp")
        server.sendmail('robottemi2022@gmail.com', email_address, msg.as_string())
        server.quit()

if __name__ == '__main__':
    MyApp().run()
