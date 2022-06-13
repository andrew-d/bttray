import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk as gtk

from . import Application

def main():
  app = Application()
  try:
    gtk.main()
  except KeyboardInterrupt:
    app.quit(None)
    pass

if __name__ == "__main__":
  main()
