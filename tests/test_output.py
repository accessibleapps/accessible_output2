"""Output dispatch contracts, without importing native backend discovery."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import Mock, patch


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
        for name in ("base", "auto"):
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


if __name__ == "__main__":
    unittest.main()
