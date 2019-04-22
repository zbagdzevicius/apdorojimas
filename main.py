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
        self.draft_file = "edited.jpg"
    
    def set_effect(self, effect):
        if effect == 'Negatyvas':
            image = self.effect_negative()
        if effect == 'Filtras':
            image = self.effect_blue_light_filter()
        if effect == 'Suliejimas':
            image = self.filter_median()
        if effect == 'Kontrastas':
            image = self.filter_sobel()
        image.save(self.draft_file)
        self.image_draft = image

        self.image_edited_to_save = image
        self.image_edited.texture = CoreImage(self.draft_file).texture
        self.image_edited.source = self.draft_file
        self.image_edited.reload()
    
    def open_save_dialog(self):
        self._popup = FileSavePopup(image_to_save=self.image_draft, title="Failo išsaugojimas",
                            size_hint=(1,1))
        self._popup.open()
    

class FileSavePopup(Popup):
    def __init__(self, image_to_save, *args, **kwargs):
        super(FileSavePopup, self).__init__(*args,**kwargs)
        self.image_to_save = image_to_save

    def save_image(self, path, filename):
        self.image_to_save.save(f"{path}/{filename}")
        self.dismiss()

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