from __future__ import absolute_import
import platform
from collections import OrderedDict

from .base import Output, OutputError

class SystemVoiceOver(Output):
    """System text-to-speech output using NSSpeechSynthesizer."""

    name = "VoiceOver"
    priority = 101
    system_output = True

    def __init__(self, *args, **kwargs):
        try:
            from AppKit import NSSpeechSynthesizer
        except ImportError as error:
            raise OutputError("AppKit speech synthesis is unavailable") from error
        self.NSSpeechSynthesizer = NSSpeechSynthesizer
        self.voiceover = NSSpeechSynthesizer.alloc().init()
        if self.voiceover is None:
            raise OutputError("Unable to initialize NSSpeechSynthesizer")
        self.voices = self._available_voices()

    def _available_voices(self):
        voices = OrderedDict()

        for voice in self.NSSpeechSynthesizer.availableVoices():
            voice_attr = self.NSSpeechSynthesizer.attributesForVoice_(voice)
            voice_name = voice_attr["VoiceName"]
            voice_identifier = voice_attr["VoiceIdentifier"]
            voices[voice_name] = voice_identifier

        return voices

    def list_voices(self):
        return list(self.voices.keys())

    def get_voice(self):
        voice_attr = self.NSSpeechSynthesizer.attributesForVoice_(self.voiceover.voice())
        return voice_attr["VoiceName"]

    def set_voice(self, voice_name):
        voice_identifier = self.voices[voice_name]
        self.voiceover.setVoice_(voice_identifier)

    def get_rate(self):
        return self.voiceover.rate()

    def set_rate(self, rate):
        self.voiceover.setRate_(rate)

    def get_volume(self):
        return self.voiceover.volume()

    def set_volume(self, volume):
        self.voiceover.setVolume_(volume)

    def is_speaking(self):
        return self.NSSpeechSynthesizer.isAnyApplicationSpeaking()

    def speak(self, text, interrupt=False):
        if interrupt:
            self.silence()

        return self.voiceover.startSpeakingString_(text)

    def output(self, text, *args, **options):
        speech_result = self.speak(text, *args, **options)
        braille_result = self.braille(text, **options)
        if speech_result is False and braille_result is False:
            raise OutputError("NSSpeechSynthesizer failed to start speech output")

    def silence(self):
        self.voiceover.stopSpeaking()

    def is_active(self):
        return self.voiceover is not None

output_class = SystemVoiceOver
