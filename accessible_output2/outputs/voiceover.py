import subprocess

from accessible_output2.outputs.base import Output

class VoiceOver(Output):
    """Speech output supporting the Apple VoiceOver screen reader."""

    name = "VoiceOver"

    def __init__(self, *args, **kwargs):
        from AppKit import NSSpeechSynthesizer
        self.NSSpeechSynthesizer = NSSpeechSynthesizer

    def run_apple_script(self, command, process = "voiceover"):
        return subprocess.Popen(["osascript", "-e",
            f"tell application \"{process}\"\n{command}\nend tell"],
            stdout = subprocess.PIPE).communicate()[0]

    def sanitize(self, str):
        return str.replace("\\", "\\\\") \
                .replace("\"", "\\\"")

    def speak(self, text, interrupt=False):
        sanitized_text = self.sanitize(text)
        # The silence function does not seem to work.
        # osascript takes time to execute, so voiceover usually starts talking  before being silenced
        if interrupt:
            self.silence()

        self.run_apple_script(f"output \"{sanitized_text}\"")

    def silence (self):
        self.run_apple_script("output \"\"")

    def is_speaking(self):
        return self.NSSpeechSynthesizer.isAnyApplicationSpeaking()

    def is_active(self):
        # If no process is found, an empty string is returned
        return bool(subprocess.Popen(["pgrep", "-x", "VoiceOver"],
            stdout = subprocess.PIPE).communicate()[0])

output_class = VoiceOver
