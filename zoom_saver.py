import rumps
from arduino_control import Arduino
import os
from time import sleep
from AppKit import NSWorkspace
from trycourier import Courier
import icalendar
import recurring_ical_events
import urllib.request
import ssl
import datetime
from config import *


class ZoomSaverApp(object):
    def __init__(self):
        self.config = {
            "app_name": "Zoom Saver",
            "hide": "Hide Camera",
            "show": "Show Camera",
            "auto": "Turn On Auto Mode",
            "pause": "Pause Protecting",
            "schedule": "Turn on Schedule Mode",
            "quit": "Quit",
        }
        # Connect to our arudino
        self.arduino = Arduino()

        # Save this for auto mode
        self.last_on_zoom = float("-inf")  # Have not been on zoom yet until this is 0

        self.app = rumps.App(self.config["app_name"], quit_button=None)
        self.isHiding = False
        self.set_up_menu()

        self.show_button = rumps.MenuItem(
            title=self.config["show"], callback=self.show_camera
        )
        self.hide_button = rumps.MenuItem(
            title=self.config["hide"], callback=self.hide_camera
        )
        self.auto_button = rumps.MenuItem(
            title=self.config["auto"], callback=self.auto_zoom
        )
        self.schedule_button = rumps.MenuItem(
            title=self.config["schedule"], callback=self.scheduler
        )
        self.quit_button = rumps.MenuItem(
            title=self.config["quit"], callback=self.clean_quit
        )
        if self.arduino.isHidden():
            self.hide_button.set_callback(None)
        else:
            self.show_button.set_callback(None)
        self.app.menu = [
            self.show_button,
            self.hide_button,
            self.auto_button,
            self.schedule_button,
            self.quit_button,
        ]

    def set_up_menu(self):
        self.app.icon = "icon.icns"

    # Option to manually hide
    def hide_camera(self, sender):
        self.set_up_menu()
        self.arduino.hide()
        self.hide_button.set_callback(None)
        self.show_button.set_callback(self.show_camera)
        self.auto_button.set_callback(self.auto_zoom)
        self.schedule_button.set_callback(self.scheduler)
        self.timer.stop()

        # self.hide_button.title = self.config["hide"]

    # Option to manually show
    def show_camera(self, sender):
        self.set_up_menu()
        self.arduino.show()
        self.show_button.set_callback(None)
        self.hide_button.set_callback(self.hide_camera)
        self.auto_button.set_callback(self.auto_zoom)
        self.schedule_button.set_callback(self.scheduler)
        self.timer.stop()
        # self.show_button.title = self.config["start"]

    # Auto hide your camera when we predict you've forgotten about zoom
    def auto_zoom(self, sender):
        self.set_up_menu()
        self.timer = rumps.Timer(self.check_zoom, 1)
        self.last_on_zoom = float("-inf")  # Resetting this if needed
        self.timer.start()
        self.auto_button.set_callback(None)
        self.hide_button.set_callback(self.hide_camera)
        self.show_button.set_callback(self.show_camera)
        self.schedule_button.set_callback(self.scheduler)

    # Timer to constantly check if we've left zoom
    def check_zoom(self, timer):
        active_app_name = str(
            NSWorkspace.sharedWorkspace().activeApplication()["NSApplicationName"]
        )
        if active_app_name == "zoom.us":
            self.last_on_zoom = 0
            self.arduino.show()
        elif self.last_on_zoom > auto_hide_zoom_time:
            self.arduino.hide()
            self.notify()
            self.last_on_zoom = float(
                "-inf"
            )  # Resetting to not send needless notifications
        else:
            self.last_on_zoom += 1
        self.previous_app = active_app_name

    # Mode for camera to only be on during class times
    def scheduler(self, sender):
        self.set_up_menu()
        self.timer = rumps.Timer(self.check_schedule, 1)
        self.timer.start()
        self.auto_button.set_callback(self.auto_zoom)
        self.hide_button.set_callback(self.hide_camera)
        self.show_button.set_callback(self.show_camera)
        self.schedule_button.set_callback(None)

    # Checks to see if we have any classes going on and if so, show camera
    def check_schedule(self, timer):
        context = ssl._create_unverified_context()
        ical_string = urllib.request.urlopen(calendar_url, context=context).read()
        calendar = icalendar.Calendar.from_ical(ical_string)
        events = recurring_ical_events.of(calendar).at(datetime.datetime.now())
        if events:
            self.arduino.show()
        else:
            self.arduino.hide()

    # Clean quit that will hide our camera
    def clean_quit(self, sender):
        self.arduino.show()
        rumps.quit_application()

    def notify(self):
        # Local notfication
        rumps.notification(
            title=self.config["app_name"],
            subtitle="Zoom Camera Alert",
            message="Looks like you've forgotten to turn of your camera while on Zoom. We've hidden it for you!",
        )
        # Courier notification, sends to phone number
        client = Courier(auth_token=courier_auth)
        resp = client.send(
            event=courier_event,
            recipient="me",
            profile={"phone_number": my_phone_number},
            data={},
        )

    def run(self):
        self.app.run()


if __name__ == "__main__":
    app = ZoomSaverApp()
    app.run()
