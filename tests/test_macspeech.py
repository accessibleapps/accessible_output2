"""Real macOS dispatch source with speech/Apple-event boundaries replaced."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import Mock, call, patch


class MacSpeechTests(unittest.TestCase):
    def setUp(self):
        source = Path(__file__).resolve().parents[1] / "accessible_output2"
        package = types.ModuleType("accessible_output2")
        package.__path__ = [str(source)]
        package.load_library = Mock(side_effect=AssertionError("native DLL load"))
        outputs = types.ModuleType("accessible_output2.outputs")
        outputs.__path__ = [str(source / "outputs")]
        appkit = types.ModuleType("AppKit")
        self.factory = appkit.NSSpeechSynthesizer = Mock()
        self.synth = self.factory.alloc.return_value.init.return_value
        self.synth.startSpeakingString_.return_value = True
        appscript = types.ModuleType("appscript")
        self.voiceover_app = appscript.app = Mock()
        self.voiceover_app.return_value.isrunning.return_value = False
        modules = patch.dict(sys.modules, {
            "accessible_output2": package, "accessible_output2.outputs": outputs,
            "AppKit": appkit, "appscript": appscript,
        })
        modules.start()
        self.addCleanup(modules.stop)
        self.package = package
        for name in ("base", "auto", "voiceover", "nsspeechsynthesizer"):
            fullname = "accessible_output2.outputs." + name
            spec = importlib.util.spec_from_file_location(
                fullname, source / "outputs" / (name + ".py"))
            module = importlib.util.module_from_spec(spec)
            sys.modules[fullname] = module
            spec.loader.exec_module(module)
            setattr(self, name, module)
        system = patch.object(self.nsspeechsynthesizer, "get_current_system", return_value="Darwin")
        system.start()
        self.addCleanup(system.stop)
        self.package.get_output_classes = lambda: [
            self.voiceover_module, self.nsspeechsynthesizer.MacSpeech]

    @property
    def voiceover_module(self):
        return sys.modules["accessible_output2.outputs.voiceover"].VoiceOver

    def test_missing_appkit_does_not_abort_auto(self):
        with patch.dict(sys.modules, {"AppKit": None}):
            output = self.auto.Auto()
        self.assertEqual([type(item) for item in output.outputs], [self.voiceover_module])

    def test_none_synthesizer_raises_output_error(self):
        self.factory.alloc.return_value.init.return_value = None
        with self.assertRaises(self.base.OutputError):
            self.nsspeechsynthesizer.MacSpeech()

    def test_speech_returns_native_boolean(self):
        output = self.nsspeechsynthesizer.MacSpeech()
        for result in (True, False):
            with self.subTest(result=result):
                self.synth.startSpeakingString_.return_value = result
                self.assertIs(output.speak("message", False), result)
        self.synth.stopSpeaking.assert_not_called()

    def test_false_native_result_remains_unsupported_combined_output(self):
        self.synth.startSpeakingString_.return_value = False
        with self.assertRaises(RuntimeError):
            self.nsspeechsynthesizer.MacSpeech().output("message")

    def test_auto_fallback_preserves_positional_and_keyword_interrupt(self):
        output = self.auto.Auto()
        self.assertIsNone(output.output("Keyboard help activated", False))
        self.assertIsNone(output.output("Keyboard help deactivated", interrupt=True))
        self.assertEqual(self.synth.method_calls, [
            call.startSpeakingString_("Keyboard help activated"),
            call.stopSpeaking(), call.startSpeakingString_("Keyboard help deactivated")])
        self.voiceover_app.return_value.output.assert_not_called()

    def test_active_voiceover_remains_preferred(self):
        self.voiceover_app.return_value.isrunning.return_value = True
        self.auto.Auto().output("message", False)
        self.voiceover_app.return_value.output.assert_called_once_with("message")
        self.synth.startSpeakingString_.assert_not_called()
        self.package.load_library.assert_not_called()


if __name__ == "__main__":
    unittest.main()
