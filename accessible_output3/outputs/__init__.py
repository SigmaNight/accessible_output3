import platform

if platform.system() == "Windows":
    from accessible_output3.utils import com

    def _load_com(*names):
        try:
            return com.load_com(*names)
        except AttributeError:
            # remove cache
            import os
            import sys
            import shutil
            for module in [m.__name__ for m in sys.modules.values()]:
                if module.startswith("win32com.gen_py."):
                    del sys.modules[module]
            cache_path = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp', 'gen_py')
            if os.path.exists(cache_path):
                shutil.rmtree(cache_path)
            # try again
            return com.load_com(*names)
    com.load_com = _load_com

    from . import nvda
    from . import jaws
    from . import sapi5
    from . import window_eyes
    from . import system_access
    from . import dolphin
    from . import pc_talker
    from . import zdsr

    # import sapi4

if platform.system() == "Darwin":
    from . import voiceover
    from . import nsspeechsynthesizer

if platform.system() == "Linux":
    from . import speech_dispatcher
    from . import e_speak

from . import auto
