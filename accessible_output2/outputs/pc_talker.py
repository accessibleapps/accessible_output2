import ctypes
from base import Output

class PCTalker(Output):

 def __init__(self):
  self.lib = ctypes.cdll.pctkusr

 def speak(self, text):
  self.lib.PCTKPRead(text.encode('cp932', 'replace'))

 def silence(self):
  self.lib.PCTKVReset()

 def is_active(self):
  return self.lib.PCTKStatus() != 0
