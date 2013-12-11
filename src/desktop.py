#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  desktop.py
#
#  Copyright 2013 Antergos
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

""" Desktop screen """

from gi.repository import Gtk, GLib
import os
import logging

_next_page = "features"
_prev_page = "check"

class DesktopAsk(Gtk.Box):
    """ Class to show the Desktop screen """
    def __init__(self, params):
        self.header = params['header']
        self.ui_dir = params['ui_dir']
        self.forward_button = params['forward_button']
        self.backwards_button = params['backwards_button']
        self.settings = params['settings']

        super().__init__()

        self.ui = Gtk.Builder()
        self.ui.add_from_file(os.path.join(self.ui_dir, "desktop.ui"))

        self.desktops_dir = os.path.join(self.settings.get('data'), "desktops/")

        self.desktop_info = self.ui.get_object("desktop_info")
        self.treeview_desktop = self.ui.get_object("treeview_desktop")

        self.ui.connect_signals(self)

        self.desktop_choice = 'gnome'

        self.enabled_desktops = self.settings.get("desktops")

        self.desktops = {
         "nox" : "Base",
         "gnome" : "Gnome",
         "cinnamon" : "Cinnamon",
         "xfce" : "Xfce",
         "lxde" : "Lxde",
         "openbox" : "Openbox",
         "enlightenment" : "Enlightenment (e17)",
         "kde" : "KDE",
         "razor" : "Razor-qt",
         "mate" : "Mate" }

        self.set_desktop_list()

        super().add(self.ui.get_object("desktop"))

    def translate_ui(self, desktop):
        """ Translates all ui elements """
        image = self.ui.get_object("image_desktop")
        label = self.ui.get_object("desktop_info")

        if desktop == 'gnome':
            txt = _("Gnome 3 is an easy and elegant way to use your "
            "computer. It features the Activities Overview which "
            "is an easy way to access all your basic tasks. GNOME 3 is "
            "the default desktop in Antergos.")
            txt = "<span weight='bold'>GNOME</span>\n" + txt

        elif desktop == 'cinnamon':
            txt = _("Cinnamon is a fork of GNOME 3 developed "
            "by (and for) Linux Mint. It provides users a more traditional desktop "
            "interface along with the newest compositing techniques of GNOME 3. "
            "Cinnamon is for users of all experience levels. ")
            txt = "<span weight='bold'>CINNAMON</span>\n" + txt

        elif desktop == 'xfce':
            txt = _("Xfce is a lightweight desktop environment. It aims to "
            "be fast and low on system resources, while remaining visually "
            "appealing and user friendly. It is a great option for use "
            "on older computers or those with low hardware specifications. ")
            txt = "<span weight='bold'>XFCE</span>\n" + txt

        elif desktop == 'lxde':
            txt = _("LXDE is an extremely fast-performing and energy-saving desktop "
            "environment. It uses less CPU and RAM than other environments. "
            "LXDE is especially designed for cloud computers with low hardware "
            "specifications such as netbooks, mobile devices, and older computers.")
            txt = "<span weight='bold'>LXDE</span>\n" + txt

        elif desktop == 'openbox':
            txt = _("Openbox is a highly configurable, next generation window "
            "manager with extensive standards support. It's default theme "
            "is well known for its minimalistic appearance and flexibility. "
            "Your desktop becomes cleaner, faster.")
            txt = "<span weight='bold'>OPENBOX</span>\n" + txt

        elif desktop == 'enlightenment':
            txt = _("Enlightenment is not just a window manager for Linux/X11 "
            "and others, but also a whole suite of libraries to help "
            "you create beautiful user interfaces with much less work")
            txt = "<span weight='bold'>ENLIGHTMENT</span>\n" + txt

        elif desktop == 'kde':
            txt = _("If you are looking for a familiar working environment, KDE's "
            "Plasma Desktop offers all the tools required for a modern desktop "
            "computing experience so you can be productive right from the start.")
            txt = "<span weight='bold'>KDE</span>\n" + txt

        elif desktop == 'razor':
            txt = _("Razor-qt is an advanced, easy-to-use, and fast desktop "
            "environment based on Qt technologies. It has been "
            "tailored for users who value simplicity, speed, and "
            "an intuitive interface.")
            txt = "<span weight='bold'>RAZOR-QT</span>\n" + txt
        
        if desktop == 'nox':
            txt = _("This option will install Antergos as command-line only system, "
            "without any type of graphical interface. After the installation you can "
            "customize Antergos by installing packages with the command-line package manager.")
            txt = "<span weight='bold'>Command-line system</span>\n" + txt
        
        if desktop == 'mate':
            txt = _("MATE is a fork of GNOME 2. It provides an intuitive and attractive "
            "desktop environment using traditional metaphors for Linux and other Unix-like "
            "operating systems.")
            txt = "<span weight='bold'>MATE</span>\n" + txt
            
        label.set_markup(txt)

        image.set_from_file(self.desktops_dir + desktop + ".png")

        txt = _("Choose Your Desktop")
        self.header.set_subtitle(txt)


    def prepare(self, direction):
        """ Prepare screen """
        self.translate_ui(self.desktop_choice)
        self.show_all()

    def set_desktop_list(self):
        """ Set desktop list in the TreeView """
        render = Gtk.CellRendererText()
        col_desktops = Gtk.TreeViewColumn(_("Desktops"), render, text=0)
        liststore_desktop = Gtk.ListStore(str)
        self.treeview_desktop.append_column(col_desktops)
        self.treeview_desktop.set_model(liststore_desktop)

        names = []
        for desktop in self.enabled_desktops:
            names.append(self.desktops[desktop])

        names.sort()

        for name in names:
            liststore_desktop.append([name])

        self.select_default_row(self.treeview_desktop, 'Gnome')

    def set_desktop(self, desktop):
        """ Show desktop info """
        for key in self.desktops.keys():
            if self.desktops[key] == desktop:
                self.desktop_choice = key
                self.translate_ui(self.desktop_choice)
                return

    def on_treeview_desktop_cursor_changed(self, treeview):
        selected = treeview.get_selection()
        if selected:
            (selection, iterator) = selected.get_selected()
            if iterator:
                desktop = selection.get_value(iterator, 0)
                self.set_desktop(desktop)

    def store_values(self):
        """ Store desktop """
        self.settings.set('desktop', self.desktop_choice)
        logging.info(_("Cnchi will install Antergos with the '%s' desktop"), self.desktop_choice)
        return True

    def select_default_row(self, treeview, desktop):
        """ Select default treeview row """
        model = treeview.get_model()
        iterator = model.iter_children(None)
        while iterator is not None:
            if model.get_value(iterator, 0) == desktop:
                path = model.get_path(iterator)
                treeview.get_selection().select_path(path)
                GLib.idle_add(self.scroll_to_cell, treeview, path)
                break
            iterator = model.iter_next(iterator)

    def scroll_to_cell(self, treeview, path):
        """ Scrolls treeview to show the desired cell """
        treeview.scroll_to_cell(path)
        return False

    def get_prev_page(self):
        return _prev_page

    def get_next_page(self):
        return _next_page
