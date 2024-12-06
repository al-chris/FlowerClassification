# The screens dictionary contains the objects of the models and controllers
# of the screens of the application.


from Model.home_screen import HomeScreenModel
from Controller.home_screen import HomeScreenController
from Model.camera_screen import CameraScreenModel
from Controller.camera_screen import CameraScreenController
from Model.result_screen import ResultScreenModel
from Controller.result_screen import ResultScreenController

screens = {
    "home screen": {
        "model": HomeScreenModel,
        "controller": HomeScreenController,
    },

    "camera screen": {
        "model": CameraScreenModel,
        "controller": CameraScreenController,
    },

    "result screen": {
        "model": ResultScreenModel,
        "controller": ResultScreenController,
    },
}