import win32gui
from libloader.com import load_com

from base import Output

class Jaws (Output):
 """Output supporting the Jaws for Windows screen reader."""

 name = 'jaws'

 def __init__(self, *args, **kwargs):
  super (Jaws, self).__init__(*args, **kwargs)
  self.object = load_com("FreedomSci.JawsApi", "jfwapi")

 def braille(self, text, **options):
  # HACK: replace " with ', Jaws doesn't seem to understand escaping them with \
  text = text.replace('"', "'")
  self.object.RunFunction("BrailleString(\"%s\")" % text)

 def speak(self, text, interrupt=False):
  self.object.SayString('      %s' % text, interrupt)

 def is_active(self):
  try:
   return self.object.SayString('',0) == True or win32gui.FindWindow("JFWUI2", "JAWS") != 0
  except:
   return False

output_class = Jaws
