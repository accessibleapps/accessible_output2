from __future__ import absolute_import
import ctypes
import os
import platform

from .base import Output, OutputError


class ZDSR(Output):
    """Supports The ZDSR screen reader

    The API DLLs are loaded from ZDSR's install folder. ZDSR's API
    documentation (https://www.zdsr.com/docs/api/zdsr-api) recommends this
    over bundling copies, which stop matching when ZDSR updates its DLLs.
    """

    name = "ZDSR"
    is_loaded=False

    def __init__(self):
        if platform.architecture()[0] == "32bit":
            libname = "ZDSRAPI.dll"
        else:
            libname = "ZDSRAPI_x64.dll"
        for variable in ("ProgramFiles(x86)", "ProgramFiles"):
            folder = os.environ.get(variable)
            if folder:
                libfile = os.path.join(folder, "zdsr", "zdsr", libname)
                if os.path.exists(libfile):
                    break
        else:
            raise OutputError("ZDSR is not installed")
        try:
            self.lib = ctypes.WinDLL(libfile)
        except OSError as error:
            raise OutputError(error)

    def load(self):
        # InitTTS(int type, const WCHAR *channelName, BOOL bKeyDownInterrupt)
        self.lib.InitTTS(0, "", True)
        self.is_loaded=True

    def is_active(self):
        try:
            if not self.is_loaded: self.load()
            return self.lib.GetSpeakState() != 2
        except:
            return False

    def speak(self, text, interrupt=False):
        if not self.is_loaded: self.load()
        self.lib.Speak(text,interrupt)

    def braille(self, text, **options):
        if not self.is_loaded: self.load()
        self.lib.Braille(text,True)

    def silence(self):
        if not self.is_loaded: self.load()
        self.lib.StopSpeak()


output_class = ZDSR
