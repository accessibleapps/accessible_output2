from platform import system as get_current_system
from .base import Output

class MacSpeech(Output):

    """Speech output supporting Apple MacOS NSSpeechSynthesizer."""

    name = "MacSpeech"
    priority = 101
    system_output = True

    def __init__(self, *args, **kwargs):
        from AppKit import NSSpeechSynthesizer
        self.synth = NSSpeechSynthesizer.alloc().init()

    def speak(self, text: str, interrupt: bool = False) -> bool:
        if interrupt:
            self.silence()
        return self.synth.startSpeakingString_(text)

    def silence(self):
        self.synth.stopSpeaking()

    def is_active(self):
        return get_current_system() == "Darwin"


output_class = MacSpeech
