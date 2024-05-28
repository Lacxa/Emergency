import json
import re

from kivy import utils
from kivymd.uix.card import MDCard

import network
from beem import sms as SM

from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.textfield import MDTextField

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
        if utils.platform == 'android':
            self.request_android_permissions()

    def add_category(self, name):
        data = self.load("alert.json")

        new_category = {
            "name": name,
            "message": "I have an Emergency i need you help!",
            "phone_numbers": []
        }

        data["categories"].append(new_category)
        with open('alert.json', 'w') as file:
            json.dump(data, file, indent=2)

        toast("Successful")
        self.display_category()

    def edit_message(self, new_sms):
        data = self.load("alert.json")
        for category in data['categories']:
            if category['name'] == self.category:
                category['message'] = new_sms
                break

        with open('alert.json', 'w') as file:
            json.dump(data, file, indent=2)
        toast("successful")

    def alert_category(self):
        data = self.load("alert.json")

        for category in data["categories"]:
            if network.ping_net():
                if category["name"] == self.category:
                    phone_numbers = category["phone_numbers"]
                    if not phone_numbers:
                        toast("No phone numbers")
                        return
                    message = category["message"]
                    for number in phone_numbers:
                        if SM.send_sms(number, message):
                            toast("sent successful")
            else:
                toast("check ur network")

    def remove_category(self):
        data = self.load("alert.json")

        index_to_remove = None
        for index, category in enumerate(data["categories"]):
            if category["name"] == self.category:
                index_to_remove = index
                break

        if index_to_remove is not None:
            del data["categories"][index_to_remove]
            with open('alert.json', 'w') as file:
                json.dump(data, file, indent=2)
            toast("successful")
            self.display_category()
            self.screen_capture("category")
        else:
            print("Category not found.")

    def add_phone_number(self, phone):
        data = self.load("alert.json")

        for category in data["categories"]:
            if category["name"] == self.category:
                category["phone_numbers"].append(phone)
                break

        with open('alert.json', 'w') as file:
            json.dump(data, file, indent=2)
        toast("successful")

    def display_category(self):
        self.root.ids.customers.data = {}
        data = self.load("alert.json")
        categories = data["categories"]
        for category in categories:
            self.root.ids.customers.data.append(
                {
                    "viewclass": "RowCard",
                    "icon": "moon-full",
                    "name": category["name"],
                }
            )

    def clear_input(self, field_id):
        for input_field_id in ['input']:
            input_field = self.root.ids[field_id]
            input_field.text = ""

    def load(self, data_file_name):
        with open(data_file_name, "r") as file:
            initial_data = json.load(file)
        return initial_data

    def alert_all(self):
        if network.ping_net():
            data = self.load("alert.json")
            for category in data["categories"]:
                category_name = category["name"]
                message = category["message"]
                phone_numbers = category["phone_numbers"]

                # Send message to each phone number
                for phone_number in phone_numbers:
                    if SM.send_sms(phone_number, message):
                        toast("sent successful")

        else:
            print("Check ur Network")

    def location(self):
        pass

    def emergency_call(self, phone):
        from beem import call as CL

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

    def request_android_permissions(self):
        from android.permissions import request_permissions, Permission

        def callback(permissions, results):
            if all([res for res in results]):
                print("callback. All permissions granted.")
            else:
                print("callback. Some permissions refused.")

        request_permissions([Permission.ACCESS_COARSE_LOCATION,
                             Permission.ACCESS_FINE_LOCATION, Permission.CALL_PHONE], callback)

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
