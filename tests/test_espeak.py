import sys
import unittest
from unittest.mock import MagicMock, patch
import pytest

from accessible_output2.outputs.base import OutputError
from accessible_output2.outputs.e_speak import ESpeak
from accessible_output2.outputs.auto import Auto
import accessible_output2


class TestESpeak(unittest.TestCase):
    def test_output_error_hierarchy(self):
        """Verify OutputError inherits from RuntimeError and Exception."""
        self.assertTrue(issubclass(OutputError, RuntimeError))
        self.assertTrue(issubclass(OutputError, Exception))
        err = OutputError("test")
        self.assertIsInstance(err, OutputError)
        self.assertIsInstance(err, RuntimeError)
        self.assertIsInstance(err, Exception)

    def test_espeak_raises_output_error_when_module_not_found(self):
        """Verify ESpeak raises OutputError when python-espeak is not installed."""
        with patch.dict(sys.modules, {"espeak": None, "espeak.core": None}):
            with pytest.raises(OutputError):
                ESpeak()

    def test_espeak_raises_output_error_when_init_raises_runtime_error(self):
        """Verify ESpeak wraps RuntimeError on initialization into OutputError."""
        def mock_import(name, *args, **kwargs):
            if "espeak" in name:
                raise RuntimeError("Failed to initialize espeak C library")
            return original_import(name, *args, **kwargs)

        original_import = __import__
        with patch("builtins.__import__", side_effect=mock_import):
            with pytest.raises(OutputError) as exc_info:
                ESpeak()
            # Verify the raised exception is both an OutputError and a RuntimeError
            self.assertIsInstance(exc_info.value, OutputError)
            self.assertIsInstance(exc_info.value, RuntimeError)
            self.assertIn("Failed to initialize espeak C library", str(exc_info.value))

    def test_espeak_raises_output_error_when_core_is_none(self):
        """Verify OutputError is raised if espeak.core ends up being None."""
        mock_espeak = MagicMock()
        mock_espeak.core = None
        with patch.dict(sys.modules, {"espeak": mock_espeak, "espeak.core": None}):
            with pytest.raises(OutputError):
                ESpeak()

    def test_espeak_success_flow(self):
        """Verify ESpeak works properly when espeak.core is available."""
        mock_core = MagicMock()
        mock_espeak = MagicMock()
        mock_espeak.core = mock_core
        with patch.dict(sys.modules, {"espeak": mock_espeak, "espeak.core": mock_core}):
            speaker = ESpeak()
            self.assertTrue(speaker.is_active())

            # Test speak without interrupt
            speaker.speak("hello", interrupt=0)
            mock_core.synth.assert_called_with("hello")
            mock_core.cancel.assert_not_called()

            # Test speak with interrupt
            mock_core.reset_mock()
            speaker.speak("world", interrupt=1)
            mock_core.cancel.assert_called_once()
            mock_core.synth.assert_called_with("world")

            # Test silence
            mock_core.reset_mock()
            speaker.silence()
            mock_core.cancel.assert_called_once()

    def test_auto_output_discovery_does_not_crash_when_espeak_fails(self):
        """Verify Auto() discovery does not crash when ESpeak fails with OutputError."""
        # Ensure espeak fails to load
        with patch.dict(sys.modules, {"espeak": None, "espeak.core": None}):
            auto = Auto()
            # ESpeak should not be in the discovered outputs
            for out in auto.outputs:
                self.assertNotIsInstance(out, ESpeak)

    def test_espeak_raises_output_error_on_os_error(self):
        """Verify arbitrary exceptions during import are wrapped into OutputError."""
        def mock_import(name, *args, **kwargs):
            if "espeak" in name:
                raise OSError("Cannot open shared object file: libespeak.so.1")
            return original_import(name, *args, **kwargs)

        original_import = __import__
        with patch("builtins.__import__", side_effect=mock_import):
            with pytest.raises(OutputError) as exc_info:
                ESpeak()
            self.assertIn("libespeak.so.1", str(exc_info.value))

    def test_espeak_silence_and_speak_when_inactive(self):
        """Verify speak and silence gracefully no-op if instance is somehow inactive."""
        mock_core = MagicMock()
        mock_espeak = MagicMock()
        mock_espeak.core = mock_core
        with patch.dict(sys.modules, {"espeak": mock_espeak, "espeak.core": mock_core}):
            speaker = ESpeak()
        speaker._ec = None
        self.assertFalse(speaker.is_active())
        # Should not raise AttributeError:
        speaker.speak("test")
        speaker.silence()

    def test_auto_output_discovery_with_only_failing_espeak(self):
        """Verify Auto() handles an environment where ESpeak is the only configured class and fails."""
        with patch.object(accessible_output2, "get_output_classes", return_value=[ESpeak]):
            with patch.dict(sys.modules, {"espeak": None, "espeak.core": None}):
                auto = Auto()
                self.assertEqual(auto.outputs, [])
                self.assertIsNone(auto.get_first_available_output())
