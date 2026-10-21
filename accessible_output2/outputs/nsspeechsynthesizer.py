from platform import system as get_current_system
from .base import Output, OutputError

class MacSpeech(Output):

    """Speech output supporting Apple MacOS NSSpeechSynthesizer."""

    name = "MacSpeech"
    priority = 101
    system_output = True

    def __init__(self, *args, **kwargs):
        try:
            from AppKit import NSSpeechSynthesizer
        except ImportError as error:
            raise OutputError("AppKit speech synthesis is unavailable") from error
        self.synth = NSSpeechSynthesizer.alloc().init()
        if self.synth is None:
            raise OutputError("Unable to initialize NSSpeechSynthesizer")

    def speak(self, text: str, interrupt: bool = False) -> bool:
        if interrupt:
            self.silence()
        return self.synth.startSpeakingString_(text)

    def output(self, text, *args, **options):
        speech_result = self.speak(text, *args, **options)
        braille_result = self.braille(text, **options)
        if speech_result is False and braille_result is False:
            raise OutputError("NSSpeechSynthesizer failed to start speech output")

    def silence(self):
        self.synth.stopSpeaking()

    def is_active(self):
        return get_current_system() == "Darwin"


output_class = MacSpeech
