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
        """
        Finds the ffirst available output.
        This is automatically called in braille, output and speak.
        """
        for output in self.outputs:
            if output.is_active():
                return output
        return None

    def speak(self, *args, **kwargs):
        """
        Speaks the given text if the output supports speech

        Args:
          text (str): The text to speak.
          **options: Additional options.
        """
        output = self.get_first_available_output()
        if output:
            output.speak(*args, **kwargs)

    def braille(self, *args, **kwargs):
        """
        Brailles the given text if the output supports Braille

        Args:
          text (str): The text to braille.
          **options: Additional options.
        """
        output = self.get_first_available_output()
        if output:
            output.braille(*args, **kwargs)

    def output(self, *args, **kwargs):
        output = self.get_first_available_output()
        if output:
            output.speak(*args, **kwargs)

    def is_system_output(self):
        """Returns True if this output is a system output."""
        output = self.get_first_available_output()
        if output:
            return output.is_system_output()
