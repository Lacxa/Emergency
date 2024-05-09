import re

import phonenumbers
from kivy import utils

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


class NumberField(MDTextField):
    pat = re.compile('[^0-9]')

    # APP
    screens = ['home']
    screens_size = NumericProperty(len(screens) - 1)
    current = StringProperty(screens[len(screens) - 1])

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
    numbers = ListProperty([])

    # APP
    screens = ['home']
    screens_size = NumericProperty(len(screens) - 1)
    current = StringProperty(screens[len(screens) - 1])


    def on_start(self):
        self.keyboard_hooker()

    def add_number(self, save):
        self.numbers.append(save)

    def save_numbers(self):
        if not self.numbers:
            toast("add number")
        else:

            print("sms.py no internet")

    """ REGISTRATION , VERIFICATION AND REMEMBER ME(login) """

    def phone_number_check_admin(self, phone):
        new_number = ""
        if phone != "" and len(phone) == 10:
            for i in range(phone.__len__()):
                if i == 0:
                    pass
                else:
                    new_number = new_number + phone[i]
            number = "+255" + new_number
            if not carrier._is_mobile(number_type(phonenumbers.parse(number))):
                toast("Please check your phone number!", 1)
                return False
            else:
                self.public_number = number
                return True
            DB.update_attendance(DB(), self.numbers)
            toast("Number aded")

    def send_message(self, sms):
        if network.ping_net():
            data = DB.Alert_numbers(DB())
            for i, y in data.items():
                self.phone = y["Phone"]

                if SM.send_sms(self.phone, sms):
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
