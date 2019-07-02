from accessible_output2 import load_library
import platform


class OutputError(Exception):
    """Raised by outputs if they fail to initialize or output"""
    pass


class Output(object):
    """The base Output object.
    Most functionality is found in child classes.
    If wishing to implement support for a new output, it might be helpful to take a look at an existing one to see how everything works.
    """

    name = "Unnamed Output"
    """str: Name of the output. This attribute should be defined in all child classes for usability purposes."""

    lib32 = None
    """str: Path pointing to a 32 bit DLL used to interface with the output. Can be None."""

    lib64 = None
    """str: Path pointing to a 64 bit DLL used to interface with the output. Can be None."""

    argtypes = {}
    """dict: A mapping of funtion names (str) to signatures (tuple) containing C types."""

    cdll = False
    """bool: Whether the DLL uses __cdecl calling conventions and should be loaded accordingly."""

    priority = 100
    """int: The priority this output should be given when automatically choosing possible outputs.
    See :class:`accessible_output2.outputs.auto.Auto`.
    Priority begins at 100. Anything higher will throw it lower on the list of available outputs. Anything lower will make it more likely to be the first option selected.
    Example, screen readers are sometimes given a higher priority (usuallly 100) than TTS such as SAAPI5 (101) due to a common usability preference."""

    system_output = False
    """bool: Is this output present and accessible on most systems with little or no additional installation or configuration?
    example: SAPI5 is a system output, while NVDA is not."""

    def __init__(self):
        self.is_32bit = platform.architecture()[0] == "32bit"
        if self.lib32 and self.is_32bit:
            self.lib = load_library(self.lib32, cdll=self.cdll)
        elif self.lib64:
            self.lib = load_library(self.lib64, cdll=self.cdll)
        else:
            self.lib = None
        if self.lib is not None:
            for func in self.argtypes:
                try:
                    getattr(self.lib, func).argtypes = self.argtypes[func]
                except AttributeError:
                    pass

    def output(self, text, **options):
        """
        Output the given text in speech, braille or both depending on what the output supports

        Args:
          text (str): The text to output.
          **options: Additional options.

        raises:
            RuntimeError: If the requested output doesn't define either speak or braille.
        """
        output = False
        if self.speak(text, **options):
            output = True
        if self.braille(text, **options):
            output = True
        if not output:
            raise RuntimeError(
                "Output %r does not have any method defined to output" % self
            )

    def is_system_output(self):
        return self.system_output

    def speak(self, text, **options):
        """
        Speaks the given text.

        Args:
          text (str): The text to speak.
          **options: Additional options.
        """
        return False

    def braille(self, text, **options):
        """
        Brailles the given text.

        Args:
          text (str): The text to braille.
          **options: Additional options.
        """
        return False
