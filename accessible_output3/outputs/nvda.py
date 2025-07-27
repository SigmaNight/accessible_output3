from __future__ import absolute_import
import os
import platform
import ctypes

from accessible_output3.utils import load_library
from .base import Output

# symbol level constants
SYMBOL_LEVEL_NONE= 0
SYMBOL_LEVEL_SOME = 100
SYMBOL_LEVEL_MOST = 200
SYMBOL_LEVEL_ALL = 300
SYMBOL_LEVEL_CHAR = 1000
SYMBOL_LEVEL_UNCHANGED = -1

# priority level constants
PRIORITY_LEVEL_NORMAL = 0
PRIORITY_LEVEL_NEXT = 1
PRIORITY_LEVEL_NOW = 2


class NVDA(Output):
    """Supports The NVDA screen reader"""

    name = "NVDA"
    lib32 = "nvdaControllerClient32.dll"
    lib64 = "nvdaControllerClient64.dll"
    argtypes = {
        "nvdaController_brailleMessage": (ctypes.c_wchar_p,),
        "nvdaController_speakText": (ctypes.c_wchar_p,),
        "nvdaController_speakSsml": (ctypes.c_wchar_p, ctypes.c_int, ctypes.c_int, ctypes.c_bool, ),
        "nvdaController_OnSsmlMarkReached": (ctypes.c_wchar_p),
    }

    def is_active(self):
        try:
            return self.lib.nvdaController_testIfRunning() == 0
        except:
            return False

    def braille(self, text, **options):
        self.lib.nvdaController_brailleMessage(text)

    def speak(self, text, interrupt=False):
        if interrupt:
            self.silence()
        self.lib.nvdaController_speakText(text)

    def speak_ssml(self, text, symbol_level=SYMBOL_LEVEL_UNCHANGED, priority_level=PRIORITY_LEVEL_NORMAL, asynchronous=True):
        result = self.lib.nvdaController_speakSsml(
            text,
            symbol_level,
            priority_level,
            asynchronous
        )
        if result == 1717:
            return False

    def speak_character(self, text):
        if not self.speak_ssml(f"<speak>{text}</speak>", SYMBOL_LEVEL_CHAR):
            self.speak(text, False)


    def silence(self):
        self.lib.nvdaController_cancelSpeech()


output_class = NVDA
