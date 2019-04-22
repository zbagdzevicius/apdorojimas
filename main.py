from kivy.app import App

from kivy.uix.screenmanager import ScreenManager, NoTransition, Screen
from kivy.uix.popup import Popup

from kivy.uix.boxlayout import BoxLayout

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import CoreImage
from io import BytesIO

from run import Filter


class EffectChooserPopup(Popup, Filter):
    def __init__(self, image_path, *args, **kwargs):
        super(EffectChooserPopup, self).__init__(image_path=image_path,*args,**kwargs)
        self.image.save(f"{image_path}.jpg")
        self.image_original.texture = CoreImage(f"{image_path}.jpg").texture
    
    def set_effect(self, effect):
        image_name = "edited.jpg"
        if effect == 'Negatyvas':
            image = self.effect_negative()
            self.current_edited_image = self.effect_negative()
        if effect == 'Filtras':
            image = self.effect_blue_light_filter()
            self.current_edited_image = self.effect_blue_light_filter()
        if effect == 'Suliejimas':
            image = self.filter_median()
            self.current_edited_image = self.filter_median()
        if effect == 'Kontrastas':
            image = self.filter_sobel()
            self.current_edited_image = self.filter_sobel()
        image.save(image_name)

        self.image_edited_to_save = image
        self.image_edited.texture = CoreImage(image_name).texture
        self.image_edited.source = image_name
        self.image_edited.reload()
    
    def save_to_current_location(self):
        self.image_edited_to_save.save("edited.bmp")
    
    def save_image(self):
        self.image_edited

class EffectViewerPopup(Popup):
    def __init__(self, *args, **kwargs):
        super(EffectViewerPopup, self).__init__(*args,**kwargs)


class FileChooser(Screen):
    def __init__(self, **kwargs):
        super(FileChooser, self).__init__(**kwargs)
    
    def load(self, path, image_path):
        try:
            print(path, image_path)
            self._popup = EffectChooserPopup(image_path=image_path[0], title="Pasirinkite efektą",
                                size_hint=(1,1))
            self._popup.open()
        except:
            pass
    
    def cancel(self):
        pass

class MainApp(App):
    def build(self):
        self.title = "Paveikslo spalvų transformavimo priemonė"
        manager = ScreenManager()
        manager.transition=NoTransition()
        manager.add_widget(FileChooser(name='FileChooser'))
        # manager.current_screen = 'FileChooser'
        return manager

if __name__ == '__main__':
    try:
        app = MainApp()
        app.run()
    except Exception as e:
        print(e)
        app.get_running_app().stop()