
"""
Script for managing hot reloading of the project.
For more details see the documentation page -

https://kivymd.readthedocs.io/en/latest/api/kivymd/tools/patterns/create_project/

To run the application in hot boot mode, execute the command in the console:
DEBUG=1 python main.py
"""

import importlib
import os

import time
import cv2
from kivy import Config
from kivy.graphics.texture import Texture
from kivy.clock import Clock

from PIL import ImageGrab

# TODO: You may know an easier way to get the size of a computer display.
resolution = ImageGrab.grab().size

# Change the values of the application window size as you need.
Config.set("graphics", "height", "648")
Config.set("graphics", "width", "300")

from kivy.core.window import Window

# Place the application window on the right side of the computer screen.
Window.top = 30
Window.left = resolution[0] - Window.width - 330

from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager


class FlowerClassification(MDApp):
    DEBUG = True
    KV_DIRS = [os.path.join(os.getcwd(), "View")]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "400"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.accent_palette = "Teal"
        self.theme_cls.accent_hue = "400"

    def build_app(self) -> MDScreenManager:
        """
        In this method, you don't need to change anything other than the
        application theme.
        """

        ## My changes

        self.camera_index = 0 # start with back camera
        self.capture = cv2.VideoCapture(self.camera_index)
        self.camera_event = None # to keep track of the camera

        ## End

        import View.screens

        self.manager_screens = MDScreenManager()
        Window.bind(on_key_down=self.on_keyboard_down)
        importlib.reload(View.screens)
        screens = View.screens.screens

        for i, name_screen in enumerate(screens.keys()):
            model = screens[name_screen]["model"]()
            controller = screens[name_screen]["controller"](model)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)
        
        self.manager_screens.current = "home screen"

        return self.manager_screens
    
    def switch_to_camera_screen(self):
        self.manager_screens.current = "camera screen"
        # camera = self.manager_screens.get_screen("camera screen").ids["camera"]
        # camera.play = True
        # if self.camera_event:
        #     pass
        # else:
        #     self.camera_event = Clock.schedule_interval(self.update_frame, 1.0/30.0) # 30 FPS
        
    def stop_camera(self):
        if self.camera_event:
            self.camera_event.cancel()
            self.camera_event = None

    def update_frame(self, dt):
        # Read a frame from the camera
        ret, frame = self.capture.read()
        if ret:
            # Convert the frame from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Get the frame dimensions
            h, w, _ = frame.shape
            
            # Convert the frame to a Kivy texture
            texture = Texture.create(size=(w, h), colorfmt="rgb")
            texture.blit_buffer(frame.tobytes(), colorfmt="rgb", bufferfmt="ubyte")
            texture.flip_vertical()  # Flip the texture to align with the camera feed
            
            # Display the texture on the Image widget
            self.manager_screens.get_screen("camera screen").ids["image"].texture = texture

    def toggle_camera(self, instance):
        # Release the current capture
        self.capture.release()
        
        # Toggle the camera index
        self.camera_index = 1 - self.camera_index  # Switch between 0 and 1
        
        # Re-initialize the capture with the new camera index
        self.capture = cv2.VideoCapture(self.camera_index)

    def capture(self):
        camera = self.manager_screens.get_screen("camera screen").ids["camera"]
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")

    def on_stop(self):
        # Release the camera when the app stops
        self.capture.release()

    def on_keyboard_down(self, window, keyboard, keycode, text, modifiers) -> None:
        """
        The method handles keyboard events.

        By default, a forced restart of an application is tied to the
        `CTRL+R` key on Windows OS and `COMMAND+R` on Mac OS.
        """

        if "meta" in modifiers or "ctrl" in modifiers and text == "r":
            self.rebuild()


FlowerClassification().run()

# After you finish the project, remove the above code and uncomment the below
# code to test the application normally without hot reloading.

# """
# The entry point to the application.
# 
# The application uses the MVC template. Adhering to the principles of clean
# architecture means ensuring that your application is easy to test, maintain,
# and modernize.
# 
# You can read more about this template at the links below:
# 
# https://github.com/HeaTTheatR/LoginAppMVC
# https://en.wikipedia.org/wiki/Model–view–controller
# """
#
# import importlib
# import os
# import time
# import cv2
# from kivymd.app import MDApp
# from kivymd.uix.screenmanager import MDScreenManager
# from kivy.graphics.texture import Texture
# from kivy.clock import Clock
# from kivy.utils import platform
# from android.permissions import request_permissions, Permission
# from android_permissions import AndroidPermissions
# from camera4kivy import CameraProviderInfo
# from View.screens import screens


# class FlowerClassification(MDApp):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.load_all_kv_files(self.directory)
#         # This is the screen manager that will contain all the screens of your
#         # application.
#         self.camera_index = 0 # start with back camera
#         self.capture = None
#         self.camera_event = None # to keep track of the camera
#         self.manager_screens = MDScreenManager()
        
#     def build(self) -> MDScreenManager:
#         request_permissions([
#             Permission.CAMERA,
#             Permission.RECORD_AUDIO,
#             Permission.WRITE_EXTERNAL_STORAGE,
#             Permission.READ_EXTERNAL_STORAGE
#         ])
#         self.generate_application_screens()
#         return self.manager_screens

#     def generate_application_screens(self) -> None:
#         """
#         Creating and adding screens to the screen manager.
#         You should not change this cycle unnecessarily. He is self-sufficient.

#         If you need to add any screen, open the `View.screens.py` module and
#         see how new screens are added according to the given application
#         architecture.
#         """

#         for i, name_screen in enumerate(screens.keys()):
#             model = screens[name_screen]["model"]()
#             controller = screens[name_screen]["controller"](model)
#             view = controller.get_view()
#             view.manager_screens = self.manager_screens
#             view.name = name_screen
#             self.manager_screens.add_widget(view)
        
#         self.manager_screens.current = "home screen"

#     def switch_to_camera_screen(self):
#         self.manager_screens.current = "camera screen"

#         if self.camera_event:
#             pass
#         else:
#             self.capture = cv2.VideoCapture(self.camera_index, cv2.CAP_ANDROID)
#             self.camera_event = Clock.schedule_interval(self.update_frame, 1.0/30.0) # 30 FPS
        
#     def stop_camera(self):
#         if self.camera_event:
#             self.camera_event.cancel()
#             self.camera_event = None
#             self.capture = None

#     def update_frame(self, dt):
#         # Read a frame from the camera
#         print(f"Camera State: {self.capture.isOpened() if self.capture != None else None}")
#         ret, frame = self.capture.read()
#         if ret:
#             # Convert the frame from BGR to RGB
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
#             # Get the frame dimensions
#             h, w, _ = frame.shape
            
#             # Convert the frame to a Kivy texture
#             texture = Texture.create(size=(w, h), colorfmt="rgb")
#             texture.blit_buffer(frame.tobytes(), colorfmt="rgb", bufferfmt="ubyte")
#             texture.flip_vertical()  # Flip the texture to align with the camera feed
            
#             # Display the texture on the Image widget
#             self.manager_screens.get_screen("camera screen").ids["image"].texture = texture

#     def toggle_camera(self, instance):
#         # Release the current capture
#         self.capture.release()
        
#         # Toggle the camera index
#         self.camera_index = 1 - self.camera_index  # Switch between 0 and 1
        
#         # Re-initialize the capture with the new camera index
#         self.capture = cv2.VideoCapture(self.camera_index)

#     def capture(self):
#         camera = self.manager_screens.get_screen("camera screen").ids["camera"]
#         timestr = time.strftime("%Y%m%d_%H%M%S")
#         camera.export_to_png("IMG_{}.png".format(timestr))
#         print("Captured")

#     def on_stop(self):
#         # Release the camera when the app stops
#         self.capture.release()


# FlowerClassification().run()