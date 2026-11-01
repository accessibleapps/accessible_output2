"""Output dispatch contracts, without importing native backend discovery."""
import ctypes
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import MagicMock, Mock, patch


class OutputTests(unittest.TestCase):
    def setUp(self):
        source = Path(__file__).resolve().parents[1] / "accessible_output2"
        package = types.ModuleType("accessible_output2")
        package.__path__ = [str(source)]
        package.load_library = Mock(side_effect=AssertionError("native DLL load"))
        outputs = types.ModuleType("accessible_output2.outputs")
        outputs.__path__ = [str(source / "outputs")]
        modules = patch.dict(sys.modules, {
            "accessible_output2": package,
            "accessible_output2.outputs": outputs,
        })
        modules.start()
        self.addCleanup(modules.stop)
        self.package = package
        for name in ("base", "auto", "e_speak", "zdsr"):
            fullname = "accessible_output2.outputs." + name
            spec = importlib.util.spec_from_file_location(
                fullname, source / "outputs" / (name + ".py"))
            module = importlib.util.module_from_spec(spec)
            sys.modules[fullname] = module
            spec.loader.exec_module(module)
            setattr(self, name, module)

    def output_with(self, speech_result, braille_result):
        output = self.base.Output()
        output.speak = Mock(return_value=speech_result)
        output.braille = Mock(return_value=braille_result)
        return output

    def test_speech_without_return_value_is_supported(self):
        output = self.output_with(None, False)
        output.output("message", interrupt=True)
        output.speak.assert_called_once_with("message", interrupt=True)
        output.braille.assert_called_once_with("message", interrupt=True)

    def test_braille_without_return_value_is_supported(self):
        output = self.output_with(False, None)
        output.output("message")
        output.braille.assert_called_once_with("message")

    def test_both_channels_are_called(self):
        output = self.output_with(True, True)
        output.output("message")
        output.speak.assert_called_once_with("message")
        output.braille.assert_called_once_with("message")

    def test_no_supported_channel_still_raises(self):
        with self.assertRaises(RuntimeError):
            self.output_with(False, False).output("message")

    def test_auto_delegates_combined_output_to_selected_backend(self):
        backend = Mock()
        backend.is_active.return_value = True
        self.package.get_output_classes = lambda: [lambda: backend]
        self.auto.Auto().output("message", interrupt=True)
        backend.output.assert_called_once_with("message", interrupt=True)
        backend.speak.assert_not_called()
        backend.braille.assert_not_called()

    def test_auto_without_active_output_remains_a_noop(self):
        backend = Mock()
        backend.is_active.return_value = False
        self.package.get_output_classes = lambda: [lambda: backend]
        self.auto.Auto().output("message")
        backend.output.assert_not_called()

    def test_auto_preserves_positional_interrupt_for_keyboard_help(self):
        class Backend(self.base.Output):
            def is_active(self):
                return True

            def speak(self, text, interrupt=False):
                self.spoken = (text, interrupt)

            def braille(self, text, **options):
                self.brailled = (text, options)

        backend = Backend()
        self.package.get_output_classes = lambda: [lambda: backend]
        output = self.auto.Auto()
        for text in ("Keyboard help activated", "Keyboard help deactivated"):
            with self.subTest(text=text):
                self.assertIsNone(output.output(text, False))
                self.assertEqual(backend.spoken, (text, False))
                self.assertEqual(backend.brailled, (text, {}))

    def test_espeak_missing_optional_module_raises_output_error(self):
        with patch.dict(sys.modules, {"espeak": None, "espeak.core": None}):
            with self.assertRaises(self.base.OutputError):
                self.e_speak.ESpeak()
        self.package.load_library.assert_not_called()

    def test_auto_excludes_espeak_when_optional_module_is_missing(self):
        self.package.get_output_classes = lambda: [self.e_speak.ESpeak]
        with patch.dict(sys.modules, {"espeak": None, "espeak.core": None}):
            output = self.auto.Auto()
        self.assertIsNone(output.get_first_available_output())
        self.assertEqual(output.outputs, [])
        self.package.load_library.assert_not_called()

    def zdsr_install(self, root):
        folder = Path(root) / "zdsr" / "zdsr"
        folder.mkdir(parents=True)
        for name in ("ZDSRAPI.dll", "ZDSRAPI_x64.dll"):
            (folder / name).write_bytes(b"")
        return folder

    def test_auto_excludes_zdsr_when_not_installed(self):
        self.package.get_output_classes = lambda: [self.zdsr.ZDSR]
        with tempfile.TemporaryDirectory() as root:
            environment = {"ProgramFiles(x86)": root, "ProgramFiles": root}
            with patch.dict(os.environ, environment):
                output = self.auto.Auto()
        self.assertEqual(output.outputs, [])

    def test_zdsr_dll_load_failure_raises_output_error(self):
        windll = Mock(side_effect=OSError("not a valid Win32 application"))
        with tempfile.TemporaryDirectory() as root:
            self.zdsr_install(root)
            with patch.dict(os.environ, {"ProgramFiles(x86)": root}), \
                    patch.object(ctypes, "WinDLL", windll, create=True):
                with self.assertRaises(self.base.OutputError):
                    self.zdsr.ZDSR()

    def test_zdsr_loads_dll_from_install_folder(self):
        windll = Mock(return_value=MagicMock())
        with tempfile.TemporaryDirectory() as root:
            folder = self.zdsr_install(root)
            environment = {"ProgramFiles(x86)": "", "ProgramFiles": root}
            with patch.dict(os.environ, environment), \
                    patch.object(ctypes, "WinDLL", windll, create=True):
                output = self.zdsr.ZDSR()
        loaded = Path(windll.call_args.args[0])
        self.assertEqual(loaded.parent, folder)
        self.assertIn(loaded.name, ("ZDSRAPI.dll", "ZDSRAPI_x64.dll"))
        output.lib.GetSpeakState.return_value = 3
        self.assertTrue(output.is_active())
        output.lib.InitTTS.assert_called_once_with(0, "", True)


if __name__ == "__main__":
    unittest.main()
