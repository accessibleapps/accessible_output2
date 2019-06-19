from accessible_output2 import load_library
import platform


class OutputError(Exception):
    """Raised by outputs if they fail to initialize or output"""
    pass


class Output(object):
    """The base Output object"""
    name = "Unnamed Output"
    lib32 = None
    lib64 = None
    argtypes = {}
    cdll = False
    priority = 100
    system_output = False

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
        Output the given text in both speech and braille depending on what the output supports

        Args:
          text: 
          **options: 

        Returns:

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
        """ """
        return self.system_output

    def speak(self, text, **options):
        """
        Speaks the given text if the output supports speech

        Args:
          text: 
          **options: 

        Returns:

        """
        return False

    def braille(self, text, **options):
        """
        Brailles the given text if the output supports Braille

        Args:
          text: 
          **options: 

        Returns:

        """
        return False
