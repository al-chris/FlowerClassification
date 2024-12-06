import importlib
import os
import time
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform
from android.permissions import request_permissions, Permission
from android_permissions import AndroidPermissions
from camera4kivy import CameraProviderInfo
from View.screens import screens


if platform == 'android':
    from jnius import autoclass
    from android.runnable import run_on_ui_thread
    from android import mActivity
    View = autoclass('android.view.View')

    @run_on_ui_thread
    def hide_landscape_status_bar(instance, width, height):
        # width,height gives false layout events, on pinch/spread 
        # so use Window.width and Window.height
        if Window.width > Window.height: 
            # Hide status bar
            option = View.SYSTEM_UI_FLAG_FULLSCREEN
        else:
            # Show status bar 
            option = View.SYSTEM_UI_FLAG_VISIBLE
        mActivity.getWindow().getDecorView().setSystemUiVisibility(option)
elif platform != 'ios':
    # Dispose of that nasty red dot, required for gestures4kivy.
    from kivy.config import Config 
    Config.set('input', 'mouse', 'mouse, disable_multitouch')


class FlowerClassification(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(self.directory)
        # This is the screen manager that will contain all the screens of your
        # application.
        self.camera_index = 0 # start with back camera
        self.capture = None
        self.camera_event = None # to keep track of the camera
        self.manager_screens = MDScreenManager()
        
    def build(self) -> MDScreenManager:
        # Theming
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.primary_hue = "200"
        
        self.enable_swipe = False
        self.generate_application_screens()
        if platform == 'android':
            Window.bind(on_resize=hide_landscape_status_bar)
        return self.manager_screens

    def generate_application_screens(self) -> None:
        """
        Creating and adding screens to the screen manager.
        You should not change this cycle unnecessarily. He is self-sufficient.

        If you need to add any screen, open the `View.screens.py` module and
        see how new screens are added according to the given application
        architecture.
        """

        for i, name_screen in enumerate(screens.keys()):
            model = screens[name_screen]["model"]()
            controller = screens[name_screen]["controller"](model)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)
        
        self.manager_screens.current = "home screen"

    def switch_to_camera_screen(self):
        self.manager_screens.current = "camera screen"

    def stop_camera(self):
        if self.camera_event:
            self.camera_event.cancel()
            self.camera_event = None

    def on_start(self):
        self.dont_gc = AndroidPermissions(self.start_app)

    def start_app(self):
        self.dont_gc = None
        self.enable_swipe = True

    def on_stop(self):
        # Release the camera when the app stops
        self.capture.release()


FlowerClassification().run()