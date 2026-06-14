from __future__ import absolute_import
import ctypes
import os
from pathlib import Path

from .base import Output


class ZDSR(Output):
    """Supports The ZDSR screen reader"""

    _dll_loc = Path(os.path.expandvars(R"%ProgramFiles(x86)%\zdsr\zdsr"))
    name = "ZDSR"
    lib32 = _dll_loc / "ZDSRAPI.dll"
    lib64 = _dll_loc / "ZDSRAPI_x64.dll"
    is_loaded = False
    argtypes = {
        "speak": (ctypes.c_wchar_p,),
    }

    def load(self):
        self.lib.InitTTS(0, "")
        self.is_loaded = True

    def is_active(self):
        try:
            if not self.is_loaded:
                self.load()
            return self.lib.GetSpeakState() != 2
        except:
            return False

    def speak(self, text, interrupt=False):
        if not self.is_loaded:
            self.load()
        self.lib.Speak(text, interrupt)

    def silence(self):
        if not self.is_loaded:
            self.load()
        self.lib.StopSpeak()


output_class = ZDSR
