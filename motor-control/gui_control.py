#!/usr/bin/env python3
import gi
import serial
import argparse

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class MotorCommand:
    def __init__(self, board):
        self.board = board


class ControlWindow(Gtk.Window):
    def __init__(self, sp):
        super().__init__(title="Motor Control")
        self.set_border_width(5)
        self.set_default_size(400, 200)

        self.arduino = serial.Serial()
        self.arduino.baudrate = 115200
        self.arduino.port = sp
        self.arduino.open()

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(vbox)
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Motor Control"
        hb.set_subtitle(sp)
        self.set_titlebar(hb)

        hbox = Gtk.Box(spacing=5)

        self.b_button = Gtk.Button.new_with_mnemonic("Sto_p")
        self.b_button.connect("clicked", self.motor_command_btn)
        hb.pack_end(self.b_button)
        hb.show_all()

        dir_label = Gtk.Label()
        dir_label.set_markup("<span weight='ultrabold' font='20'>Directions</span>")
        dir_label.set_justify(Gtk.Justification.CENTER)
        vbox.pack_start(dir_label, True, True, 0)
        self.w_button = Gtk.Button.new_from_icon_name("go-up", Gtk.IconSize.BUTTON)
        self.w_button.connect("clicked", self.motor_command_btn)

        self.a_button = Gtk.Button.new_from_icon_name(
            "go-previous", Gtk.IconSize.BUTTON
        )
        self.a_button.connect("clicked", self.motor_command_btn)

        self.s_button = Gtk.Button.new_from_icon_name("go-next", Gtk.IconSize.BUTTON)
        self.s_button.connect("clicked", self.motor_command_btn)

        self.d_button = Gtk.Button.new_from_icon_name("go-down", Gtk.IconSize.BUTTON)
        self.d_button.connect("clicked", self.motor_command_btn)

        hbox.pack_start(self.w_button, True, True, 0)
        hbox.pack_start(self.a_button, True, True, 0)
        hbox.pack_start(self.s_button, True, True, 0)
        hbox.pack_start(self.d_button, True, True, 0)

        vbox.pack_start(hbox, True, True, 0)
        vbox.show_all()

        self.connect("destroy", self.release_serial)
        self.connect("key-press-event", self.motor_command)

    def motor_command_btn(self, btn):
        if btn is self.w_button:
            self.arduino.write(b"w")
        elif btn is self.a_button:
            self.arduino.write(b"a")
        elif btn is self.s_button:
            self.arduino.write(b"s")
        elif btn is self.d_button:
            self.arduino.write(b"d")
        elif btn is self.b_button:
            self.arduino.write(b"b")
            self.motor1.set_state("STOP")
            self.motor2.set_state("STOP")
            self.motor3.set_state("STOP")
            self.motor4.set_state("STOP")

    def motor_command(self, _, event):
        if Gdk.keyval_name(event.keyval) == "w":
            self.w_button.activate()
        elif Gdk.keyval_name(event.keyval) == "a":
            self.a_button.activate()
        elif Gdk.keyval_name(event.keyval) == "s":
            self.s_button.activate()
        elif Gdk.keyval_name(event.keyval) == "d":
            self.d_button.activate()
        elif Gdk.keyval_name(event.keyval) == "b":
            self.b_button.activate()

    def release_serial(self, _this_window):
        self.arduino.close()


aparser = argparse.ArgumentParser(
    description="Control motors using pySerial and Arduino"
)
aparser.add_argument(
    "serialport", metavar="s", type=str, nargs=1, help="arduino's serialport address"
)
args = aparser.parse_args()

window = ControlWindow(args.serialport[0])
window.show()

window.connect("destroy", Gtk.main_quit)
Gtk.main()
