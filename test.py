################################################
"""
File to test the core.py of Tarl project...
"""
################################################

from back import TarlCore as Tc


tc = Tc("t_1", fps=10,  keyboard_captions=False,  show_mouse=False,  mouse_icon="mouse_pointer.png")

tc.record_screen() # for scr rec
tc.audio_recording_mic() # for voice rec
