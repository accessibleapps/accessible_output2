from __future__ import absolute_import
from .base import Output

class ESpeak(Output):
    """Supports ESpeak on Linux

    Note this requires python-espeak to be installed
    This can be done on Debian distros by using apt-get install python-espeak
    Or through `this tarball <https://launchpad.net/python-espeak>`_.
	"""

    name = "Linux ESpeak"
    priority = 101
    _ec = None

    def __init__(self):
        try:
            import espeak.core
            self._ec = espeak.core
        except:
            print("Cannot find espeak.core. Please install python-espeak or python3-espeak.")

    def is_active(self):
        return self._ec is not None

    def speak(self, text, interrupt=0):
        if interrupt:
            self.silence()
        self._ec.synth(text)

    def silence(self):
        self._ec.cancel()


output_class = ESpeak
