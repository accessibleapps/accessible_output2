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

    def is_speaking(self):
        return self.NSSpeechSynthesizer.isAnyApplicationSpeaking()

    def speak(self, text, interrupt=False):
        # apple script output command seems to interrupt by default
        # if an empty string is provided itseems to force voiceover to not interrupt
        if not interrupt:
                self.silence()

        sanitized_text = sanitize(text)
        self.run_apple_script(f"output \"{sanitized_text}\"")

    def silence (self):
        self.run_apple_script("output \"\"")

    def is_active(self):
        return subprocess.Popen(["pgrep", "--count", "--ignore-case", "--exact", "voiceover"],
            stdout = subprocess.PIPE).communicate()[0].startswith(b"0")

output_class = VoiceOver
