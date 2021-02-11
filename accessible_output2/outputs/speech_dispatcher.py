from __future__ import absolute_import
from .base import Output

class SpeechDispatcher(Output):
    """Supports Speech Dispatcher on Linux

    Note this requires python-speechd or python3-speechd to be installed.
    This can be done on Debian distros by using apt-get install python3-speechd.
    """

    name = "Linux Speech Dispatcher"
    _client = None
    _is_speaking = False

    def __init__(self):
        global speechd
        try:
            import speechd
        except:
            print("Cannot find Speech Dispatcher. Please install python-speechd or python3-speechd.")
        else:
            try:
                self._client = speechd.SSIPClient("")
            except Exception as e:
                print(e)

    def is_active(self):
        return self._client is not None

    def is_speaking(self):
        return self._is_speaking

    def _callback(self, callback_type):
        if callback_type == speechd.CallbackType.BEGIN:
            self._is_speaking = True
        elif callback_type == speechd.CallbackType.END:
            self._is_speaking = False
        elif callback_type == speechd.CallbackType.CANCEL:
            self._is_speaking = False

    def speak(self, text, interrupt=0):
        if interrupt:
            self.silence()
        self._client.speak(text, callback=self._callback,
                           event_types=(speechd.CallbackType.BEGIN,
                                        speechd.CallbackType.CANCEL,
                                        speechd.CallbackType.END))

    def silence(self):
        self._client.cancel()

    def close(self):
        # With speechd < 1.10.2, this method must be called
        # for the program to close correctly.
        self._client.close()


output_class = SpeechDispatcher
