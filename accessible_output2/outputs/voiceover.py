import subprocess

from accessible_output2.outputs.base import Output, OutputError

class VoiceOver(Output):
    """Speech output supporting the Apple VoiceOver screen reader."""

    name = "VoiceOver"

    def __init__(self, *args, **kwargs):
        try:
            from AppKit import NSSpeechSynthesizer
        except ImportError as error:
            raise OutputError("AppKit speech synthesis is unavailable") from error
        self.NSSpeechSynthesizer = NSSpeechSynthesizer

    def run_apple_script(self, command, process = "voiceover"):
        try:
            result = subprocess.Popen(["osascript", "-e",
                f"tell application \"{process}\"\n{command}\nend tell"],
                stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            stdout, stderr = result.communicate()
        except OSError as error:
            raise OutputError(str(error)) from error
        if result.returncode:
            raise OutputError("osascript exited %s: %s" % (
                result.returncode, stderr.decode("utf-8", errors="replace")))
        return stdout

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
