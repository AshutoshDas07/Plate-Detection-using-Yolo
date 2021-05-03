from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from prune_and_extract_text import extract_text, match

import os


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class LoadDB(FloatLayout):
    get_text = ObjectProperty(None)
    get_db_text = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    input_image = ObjectProperty(None)
    input_file_path = ""
    input_file_name = ""

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        self.ids.input_image.source = os.path.join(path, filename[0])
        self.dismiss_popup()
        self.input_file_path = path
        self.input_file_name = filename[0]

    def save(self):
        input_image_path = os.path.join(self.input_file_path, self.input_file_name)
        os.system("python detect.py --source " + input_image_path + " --weights weights/last.pt --save-txt")
        output_image_path = "./inference/output/" + self.input_file_name.replace(self.input_file_path,"")
        cropped_image_path = output_image_path.replace(".jpg", "_cropped.jpg")
        print(cropped_image_path)
        self.ids.output_image.source = output_image_path
        extract_num = extract_text(cropped_image_path, 'out')
        suspected_plates = ""
        if len(extract_num) > 2:
            suspected_plates = match(extract_num)
        if suspected_plates == "":
            suspected_plates = "NO MATCH FOUND, NOT STOLEN"
        self.ids.plate_number.text = "\nPLATE NUMBER: " + extract_num + "\n" + "SUSPECTED PLATES: " + suspected_plates
        f = open('plate_numbers.csv').readlines()
        present = False
        for line in f:
            if extract_num.replace('\n','') in line.replace('\n',''):
                present = True
                break
        if not present:
            open('plate_numbers.csv', 'a').write(extract_num + '\n')

    def showdb(self):
        self.content = LoadDB(get_db_text=self.get_db_text,get_text=self.get_text, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=self.content,
                            size_hint=(0.9, 0.9))
        #content.ids.dbdisplay.text = "nilesh"
        self._popup.open()

    def get_text(self):
        return open('lic.csv').read()

    def get_db_text(self, tested_text=False):
        if tested_text:
            self.content.ids.dbdisplay.text = open('plate_numbers.csv').read()
        else:
            self.content.ids.dbdisplay.text = open('lic.csv').read()

class PlateDetect(App):
    pass


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('LoadDB', cls=LoadDB)


if __name__ == '__main__':
    PlateDetect().run()

