"""
    Class finds a container with a given name.
"""
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class FindChild:

    @staticmethod
    def find_child(parent, name):

        if parent.get_name() == name:
            return parent

        if issubclass(type(parent), Gtk.Container):
            children = parent.get_children()
            for child in children:
                widget = FindChild.find_child(child, name)
                if widget is not None:
                    return widget

        return None
