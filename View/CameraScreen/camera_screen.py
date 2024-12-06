from View.base_screen import BaseScreenView
from kivymd.toast import toast
from kivy.properties import ObjectProperty
from kivy.utils import platform
from kivy.core.window import Window


class CameraScreenView(BaseScreenView):
    photo_preview = ObjectProperty(None)
    
    def model_is_changed(self) -> None:
        """
        Called whenever any change has occurred in the data model.
        The view in this method tracks these changes and updates the UI
        according to these changes.
        """
    def on_enter(self):
        self.photo_preview.connect_camera(filepath_callback= self.capture_path)

    def on_pre_leave(self):
        self.photo_preview.disconnect_camera()
    
    def capture_path(self,file_path):
        toast(file_path)

    def photo(self):
        print("photo")
        self.photo_preview.capture_photo()

    def flash(self):
        print("flash")
        icon = self.photo_preview.flash()
        if icon == 'on':
            self.ids.flash.background_normal ='assets/images/icons/flash.png'
            self.ids.flash.background_down   ='assets/images/icons/flash.png'
        elif icon == 'auto':
            self.ids.flash.background_normal ='assets/images/icons/flash-auto.png'
            self.ids.flash.background_down   ='assets/images/icons/flash-auto.png'
        else:
            self.ids.flash.background_normal ='assets/images/icons/flash-off.png'
            self.ids.flash.background_down   ='assets/images/icons/flash-off.png'

    def select_camera(self, facing):
        print("select_camera")
        self.photo_preview.select_camera(facing)

    def on_size(self, layout, size):
        if platform in ['android', 'ios']: 
            self.ids.photo.min_state_time = 0.3 
        else:
            self.ids.photo.min_state_time = 1
        self.ids.photo.min_state_time = 1
        if Window.width < Window.height:
            self.ids.other.pos_hint  = {'center_x':.2,'center_y':.5}
            self.ids.other.size_hint = (.2, None)
            self.ids.photo.pos_hint  = {'center_x':.5,'center_y':.5}
            self.ids.photo.size_hint = (.24, None)
            self.ids.flash.pos_hint  = {'center_x':.8,'center_y':.5}
            self.ids.flash.size_hint = (.15, None)
        else:
            self.ids.other.pos_hint  = {'center_x':.5,'center_y':.8}
            self.ids.other.size_hint = (None, .2)
            self.ids.photo.pos_hint  = {'center_x':.5,'center_y':.5}
            self.ids.photo.size_hint = (None, .24)
            self.ids.flash.pos_hint  = {'center_x':.5,'center_y':.2}
            self.ids.flash.size_hint = (None, .15)