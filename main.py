from datetime import datetime
import json
import re

import phonenumbers
from kivy import utils
from kivymd.uix.card import MDCard

import network
from beem import sms as SM

from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.textfield import MDTextField
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type

Window.keyboard_anim_args = {"d": .2, "t": "linear"}
Window.softinput_mode = "below_target"
Clock.max_iteration = 250

if utils.platform != 'android':
    Window.size = [420, 720]


class RowCard(MDCard):
    icon = StringProperty("")
    name = StringProperty("")


class NumberField(MDTextField):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):

        if len(self.text) == 0 and substring != "0":
            return

        if len(self.text) == 10:
            return

        if len(self.text) == 1 and substring != "6" and substring != "7":
            return

        if not substring.isdigit():
            return

        return super(NumberField, self).insert_text(substring, from_undo=from_undo)


class NumberOnlyField(MDTextField):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):

        if len(self.text) == 0 and substring == "0":
            return

        if not substring.isdigit():
            return

        return super(NumberOnlyField, self).insert_text(substring, from_undo=from_undo)


class MainApp(MDApp):
    size_x, size_y = Window.size
    phone = StringProperty("")

    idd = StringProperty("")
    category = StringProperty("")

    # APP
    screens = ['home']
    screens_size = NumericProperty(len(screens) - 1)
    current = StringProperty(screens[len(screens) - 1])

    def on_start(self):
        self.keyboard_hooker()
        self.display_category()

    def add_category(self, name):
        #data = "category": name,
        print("save !")
        pass

    def edit_message(self, sms):
        print(sms)
        category = self.category
        pass

    def alert_category(self):
        print("alert category !")
        category = self.category
        pass

    def remove_category(self):
        print("remove category !")
        category = self.category
        pass

    def add_phone_number(self, phone):
        with open("alert.json", "r") as file:
            existing_data = json.load(file)
            self.gen_id()
            data = {self.idd: phone}
            existing_data.update(data)
        with open("alert.json", "w") as file:
            data_dump = json.dumps(existing_data, indent=6)
            file.write(data_dump)
            file.close()

    def display_category(self):
        self.root.ids.customers.data = {}
        self.root.ids.customers.data.append(
            {
                "viewclass": "RowCard",
                "icon": "moon-full",
                "name": "wow",
                "id": "id"
            }
        )

    def gen_id(self):
        timestamp = datetime.now().strftime('%d%H%f')
        self.idd = timestamp

        return self.idd

    def load(self, data_file_name):
        with open(data_file_name, "r") as file:
            initial_data = json.load(file)
        return initial_data

    def alert_all(self):
        if network.ping_net():
            data = self.load("alert.json")
            message = "I have an Emergency am at"  # + self.location
            for i, y in data.items():
                self.phone = str(y)
                #sms = message + y

                if SM.send_sms(self.phone, message):
                    toast("sent successful")
        else:
            print("Check ur Network")

    def emergency_call(self):
        from beem import call as CL
        phone = "0714069014"

        CL.Actions.call(CL.Actions(), phone)

    """ KEYBOARD INTEGRATION """

    def keyboard_hooker(self, *args):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        print(self.screens_size)
        if key == 27 and self.screens_size > 0:
            print(f"your were in {self.current}")
            last_screens = self.current
            self.screens.remove(last_screens)
            print(self.screens)
            self.screens_size = len(self.screens) - 1
            self.current = self.screens[len(self.screens) - 1]
            self.screen_capture(self.current)
            return True
        elif key == 27 and self.screens_size == 0:
            toast('Press Home button!')
            return True

    """ SCREEN FUNCTIONS """

    def screen_capture(self, screen):
        sm = self.root
        sm.current = screen
        if screen in self.screens:
            pass
        else:
            self.screens.append(screen)
        print(self.screens)
        self.screens_size = len(self.screens) - 1
        self.current = self.screens[len(self.screens) - 1]
        print(f'size {self.screens_size}')
        print(f'current screen {screen}')

    def screen_leave(self):
        print(f"your were in {self.current}")
        last_screens = self.current
        self.screens.remove(last_screens)
        print(self.screens)
        self.screens_size = len(self.screens) - 1
        self.current = self.screens[len(self.screens) - 1]
        self.screen_capture(self.current)


MainApp().run()
