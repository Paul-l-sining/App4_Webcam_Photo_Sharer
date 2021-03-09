from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
import time
import webbrowser

from filesharer import FileSharer

Builder.load_file('frontend.kv')


class CameraScreen(Screen):
    def start(self):
        """Starts camera and changes Button Text"""
        self.ids.camera.opacity = 1
        self.ids.camera.play = True
        self.ids.start.text = 'Stop Camera'
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        """Stop camera and changes Button text"""
        self.ids.camera.opacity = 0
        self.ids.camera.play = False
        self.ids.start.text = 'Start Camera'
        self.ids.camera.texture = None

    def capture(self):
        """Creates a filename with the current time and captures
        and saves a photo image under that filename"""
        current_time = time.strftime('%Y%m%d-%H%M%S')
        filepath = f'files/{current_time}.png'
        self.ids.camera.export_to_png(filepath)
        self.manager.current = 'image_screen'  # switch to the next screen
        self.manager.current_screen.ids.img.source = filepath  # inherit img to the next screen
        return filepath


class ImageScreen(Screen):
    error_msg = 'Please create a link first first.'

    def create_link(self):
        """Accesses the photo filepath, uploads it to the web,
         and inserts the link in the Label widget. """
        self.filename = App.get_running_app().root.ids.camera_screen.capture()
        self.url = FileSharer(self.filename).share()
        self.ids.label.text = self.url

    def copy_link(self):
        """Copy the link on the clipboard """
        try:
            Clipboard.copy(self.url)
        except(AttributeError):
            self.ids.label.text = self.error_msg

    def open_link(self):
        """Open link with default browser"""
        try:
            # webbrowser.open(self.url) # if you are on Windows OS
            webbrowser.get('safari').open_new_tab(self.url)  # if you are on Mac OS
        except(AttributeError):
            self.ids.label.text = self.error_msg


class RootWidget(ScreenManager):
    pass


class MainApp(App):

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MainApp().run()
