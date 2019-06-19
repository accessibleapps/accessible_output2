from __future__ import absolute_import
import accessible_output2
from .base import Output, OutputError


class Auto(Output):
    """An output which automatically selects the first available output on the system"""
    def __init__(self):
        output_classes = accessible_output2.get_output_classes()
        self.outputs = []
        for output in output_classes:
            try:
                self.outputs.append(output())
            except OutputError:
                pass

    def get_first_available_output(self):
        """Find the ffirst available output"""
        for output in self.outputs:
            if output.is_active():
                return output
        return None

    def speak(self, *args, **kwargs):
        output = self.get_first_available_output()
        if output:
            output.speak(*args, **kwargs)

    def braille(self, *args, **kwargs):
        output = self.get_first_available_output()
        if output:
            output.braille(*args, **kwargs)

    def output(self, *args, **kwargs):
        output = self.get_first_available_output()
        if output:
            output.speak(*args, **kwargs)

    def is_system_output(self):
        """Is the current output a system output?"""
        output = self.get_first_available_output()
        if output:
            return output.is_system_output()
