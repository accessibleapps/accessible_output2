from __future__ import absolute_import
from builtins import str
from .base import Output

class SystemAccess (Output):
 """Supports System Access and System Access Mobile"""

 name = "System Access"
 lib32 = 'saapi32.dll'
 priority = 99

 def braille(self, text, **options):
  self.lib.SA_BrlShowTextW(str(text))

 def speak(self, text, interrupt=False):
  if self.is_active():
   self.dll.SA_SayW(str(text))

 def is_active(self):
  try:
   return self.dll.SA_IsRunning()
  except:
   return False

output_class = SystemAccess
