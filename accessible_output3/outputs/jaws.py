from __future__ import absolute_import
from ..utils import load_com
import pywintypes

from .base import Output, OutputError


class Jaws(Output):
    """Supports the Jaws for Windows screen reader."""

    name = "jaws"

    def __init__(self, *args, **kwargs):
        super(Jaws, self).__init__(*args, **kwargs)
        try:
            self.object = load_com("FreedomSci.JawsApi", "jfwapi")
        except (pywintypes.com_error, TypeError):
            raise OutputError

    def braille(self, text, **options):
        # HACK: replace " with ', Jaws doesn't seem to understand escaping them with \
        text = text.replace('"', "'")
        self.object.RunFunction('BrailleString("%s")' % text)

    def speak(self, text, interrupt=False):
        self.object.SayString("      %s" % text, interrupt)

    def is_active(self):
        try:
            import win32gui
        except ImportError:
            return False
        try:
            return (
                self.object.SayString("", 0) == True
                or win32gui.FindWindow("JFWUI2", "JAWS") != 0
            )
        except:
            return False


output_class = Jaws
