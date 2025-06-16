from __future__ import absolute_import
import subprocess
import platform
from .base import Output


class Orca(Output):
    """Supports Orca screen reader self-voicing on Linux via D-Bus
    
    Uses the new Orca remote service API to present messages directly
    through Orca's speech/braille output system. Falls back gracefully
    if D-Bus service is not available.
    
    Note: This requires Orca to be running and the D-Bus service to be active.
    """

    name = "Orca Screen Reader"
    priority = 99  # Higher priority than speech_dispatcher (100)
    system_output = False
    
    def __init__(self):
        self.service_name = "org.gnome.Orca.Service"
        self.main_path = "/org/gnome/Orca/Service"
        self._is_active = None
        if platform.system() == "Linux":
            self._test_connection()
    
    def _test_connection(self):
        """Test if Orca D-Bus service is available"""
        try:
            result = subprocess.run([
                "gdbus", "call", "--session",
                "--dest", self.service_name,
                "--object-path", self.main_path,
                "--method", "org.gnome.Orca.Service.ListCommands"
            ], check=True, capture_output=True, text=True, timeout=2)
            self._is_active = True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            self._is_active = False
    
    def is_active(self):
        """Check if Orca D-Bus service is available"""
        if self._is_active is None:
            self._test_connection()
        return self._is_active
    
    def speak(self, text, interrupt=0):
        """
        Speak text through Orca's speech output system
        
        Args:
            text (str): The text to speak
            interrupt (int): Whether to interrupt current speech (unused for Orca)
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_active():
            return False
        
        try:
            result = subprocess.run([
                "gdbus", "call", "--session",
                "--dest", self.service_name,
                "--object-path", self.main_path,
                "--method", "org.gnome.Orca.Service.PresentMessage",
                str(text)
            ], check=True, capture_output=True, text=True, timeout=5)
            return "true" in result.stdout.lower()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def braille(self, text, **options):
        """
        Display text on braille display through Orca
        
        Orca's PresentMessage method handles both speech and braille automatically
        based on user preferences.
        
        Args:
            text (str): The text to display
            **options: Additional options (unused)
        
        Returns:
            bool: True if successful, False otherwise
        """
        return self.speak(text)
    
    def silence(self):
        """Interrupt current speech output"""
        if not self.is_active():
            return False
        
        try:
            # Try to execute InterruptSpeech command if available
            result = subprocess.run([
                "gdbus", "call", "--session",
                "--dest", self.service_name,
                "--object-path", self.main_path + "/Speech",
                "--method", "org.gnome.Orca.Module.ExecuteCommand",
                "InterruptSpeech", "false"
            ], check=True, capture_output=True, text=True, timeout=2)
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return False


output_class = Orca