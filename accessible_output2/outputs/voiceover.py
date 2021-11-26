import subprocess, psutil

from accessible_output2.outputs.base import Output

class VoiceOver(Output):
    """Speech output supporting the Apple VoiceOver screen reader."""

    name = "VoiceOver"

    def run_apple_script(self, command, process = "voiceover"):
        return subprocess.Popen(["osascript", "-e",
            f"tell application \"{process}\"\n{command}\nend tell"],
            stdout = subprocess.PIPE).communicate()[0]

    def speak(self, text, interrupt=False):
        # apple script output command seems to interrupt by default
        # if an empty string is provided itseems to force voiceover to not interrupt
        if not interrupt:
                self.silence()
        self.run_apple_script(f"output \"{text}\"")

    def silence (self):
        self.run_apple_script("output \"\"")

    def is_active(self):
        for process in psutil.process_iter():
            if process.name().lower() == "voiceover":
                return True

        return False

output_class = VoiceOver
