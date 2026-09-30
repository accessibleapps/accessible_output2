from __future__ import absolute_import
from .base import Output, OutputError

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
            if self._ec is None:
                raise OutputError("espeak.core is not available")
        except OutputError:
            raise
        except Exception as e:
            raise OutputError(e)

    def is_active(self):
        return self._ec is not None

    def speak(self, text, interrupt=0):
        if not self.is_active():
            return
        if interrupt:
            self.silence()
        self._ec.synth(text)

    def silence(self):
        if not self.is_active():
            return
        self._ec.cancel()


output_class = ESpeak
