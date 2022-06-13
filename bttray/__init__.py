import os
import subprocess
from functools import partial

from pulsectl import Pulse

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
#gi.require_version('Keybinder', '3.0')

from gi.repository import GLib as glib
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
#from gi.repository import Keybinder as keybinder


def should_show_card(card):
  """Whether we should show a PulseAudio card in the menu"""
  # Only show cards that have both profiles we care about
  profile_names = list(map(lambda x: x.name, card.profile_list))
  return 'a2dp_sink' in profile_names and 'handsfree_head_unit' in profile_names


def card_name(card):
  """User-friendly name of a PulseAudio card"""
  props = card.proplist
  candidates = [
    props.get('device.description'),
    props.get('bluez.alias'),
    card.name,
  ]

  name = 'unknown'
  for candidate in candidates:
    if candidate is not None and candidate != '':
      name = candidate
      break

  return name


def card_menu_display(card):
  """What to display in the systray menu"""
  return f"{card_name(card)} ({card.profile_active.name})"


def card_key(card):
  """
  Key to identify whether a PulseAudio card is the same as a card from a
  previous update.
  """
  return (
    card.name,
    card.profile_active.name,
  )


class Application:
  def __init__(self):
    self.pulse = Pulse('bluetooth-tray')
    self.cards = None

    self.indicator = appindicator.Indicator.new("customtray", "audio-headset-symbolic", appindicator.IndicatorCategory.APPLICATION_STATUS)
    self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

    self.menu = gtk.Menu()
    self.update_menu()
    self.indicator.set_menu(self.menu)

    glib.timeout_add(1000, self.update_menu)

  def update_menu(self, *, force=False):
    """
    Called every second to update the systray menu
    """
    new_cards = self.pulse.card_list()

    # Only show cards that have the two profiles we care about
    new_cards = list(filter(should_show_card, new_cards))
    new_cards.sort(key=lambda c: card_menu_display(c))

    # If nothing changed, then just return
    if force:
      print("[update_menu] force-updating menu")
    elif self.cards is not None:
      new_card_names = list(map(lambda x: card_key(x), new_cards))
      old_card_names = list(map(lambda x: card_key(x), self.cards))
      if old_card_names == new_card_names:
        return True

    print("[update_menu] started")

    # Step 1: remove all menu items
    # TODO: should remove only changed items
    for i in self.menu.get_children():
      self.menu.remove(i)

    if len(new_cards) > 0:
      # Step 2: get all cards
      for card in new_cards:
        item = gtk.MenuItem(label=card_menu_display(card))
        item.connect('activate', lambda widget: self.item_clicked(card))
        self.menu.append(item)
    else:
      item = gtk.MenuItem(label="No Bluetooth headsets")
      child = item.get_child()
      child.set_markup("<i>No Bluetooth headsets</i>")
      self.menu.append(item)

    self.menu.append(gtk.SeparatorMenuItem.new())

    exittray = gtk.MenuItem(label='Exit Tray')
    exittray.connect('activate', self.quit)
    self.menu.append(exittray)
    self.menu.show_all()

    self.cards = new_cards
    print("[update_menu] finished")

    # Return true to keep the timer running
    return True

  def quit(self, _):
    """Quits the application"""
    print("[quit] quitting application")
    self.pulse.close()
    gtk.main_quit()

  def item_clicked(self, card):
    """Called when an item in the menu is clicked"""
    active = card.profile_active.name
    if active == 'a2dp_sink':
      next_profile = 'handsfree_head_unit'
    elif active == 'handsfree_head_unit':
      next_profile = 'a2dp_sink'
    else:
      print("Unknown state:", active)
      return

    print(f"[item_clicked] {card_name(card)!r} from {active} -> {next_profile}")
    self.pulse.card_profile_set(card, next_profile)

    # Refresh by removing all cards from the cache and always re-generating.
    self.cards = None
    self.update_menu(force=True)
