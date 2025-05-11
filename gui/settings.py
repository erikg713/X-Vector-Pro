# gui/settings.py

from core import update_configuration

def toggle_stealth_mode(enable):
    update_configuration({"stealth_mode": enable})
