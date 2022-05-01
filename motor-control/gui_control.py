#!/usr/bin/env python3
import gi
import serial
import argparse

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


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

        b_button = Gtk.Button.new_with_label("Stop")
        b_button.connect("clicked", self.b_clicked)
        hb.pack_end(b_button)
        hb.show_all()

        dir_label = Gtk.Label()
        dir_label.set_markup("<span weight='ultrabold' font='20'>Directions</span>")
        dir_label.set_justify(Gtk.Justification.CENTER)
        vbox.pack_start(dir_label, True, True, 0)
        w_button = Gtk.Button.new_from_icon_name("go-up", Gtk.IconSize.BUTTON)
        w_button.connect("clicked", self.w_clicked)

        a_button = Gtk.Button.new_from_icon_name("go-previous", Gtk.IconSize.BUTTON)
        a_button.connect("clicked", self.a_clicked)

        s_button = Gtk.Button.new_from_icon_name("go-next", Gtk.IconSize.BUTTON)
        s_button.connect("clicked", self.s_clicked)

        d_button = Gtk.Button.new_from_icon_name("go-down", Gtk.IconSize.BUTTON)
        d_button.connect("clicked", self.d_clicked)

        hbox.pack_start(w_button, True, True, 0)
        hbox.pack_start(a_button, True, True, 0)
        hbox.pack_start(s_button, True, True, 0)
        hbox.pack_start(d_button, True, True, 0)

        vbox.pack_start(hbox, True, True, 0)
        vbox.show_all()

        self.connect("destroy", self.release_serial)

    def release_serial(self, _this_window):
        self.arduino.close()

    def b_clicked(self, button):
        self.arduino.write(b"b")

    def w_clicked(self, button):
        self.arduino.write(b"w")

    def a_clicked(self, button):
        self.arduino.write(b"a")

    def s_clicked(self, button):
        self.arduino.write(b"s")

    def d_clicked(self, button):
        self.arduino.write(b"d")


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
