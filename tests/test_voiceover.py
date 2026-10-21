"""Original macOS APIs through real source, with no native/osascript calls."""
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import Mock, call, patch


class VoiceOverTests(unittest.TestCase):
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
        self.factory.availableVoices.return_value = ["voice.id"]
        self.factory.attributesForVoice_.return_value = {
            "VoiceName": "Test voice", "VoiceIdentifier": "voice.id"}
        self.synth.voice.return_value = "voice.id"
        modules = patch.dict(sys.modules, {
            "accessible_output2": package, "accessible_output2.outputs": outputs,
            "AppKit": appkit,
        })
        modules.start()
        self.addCleanup(modules.stop)
        self.package = package
        for name in ("base", "auto", "voiceover", "system_voiceover"):
            fullname = "accessible_output2.outputs." + name
            spec = importlib.util.spec_from_file_location(
                fullname, source / "outputs" / (name + ".py"))
            module = importlib.util.module_from_spec(spec)
            sys.modules[fullname] = module
            spec.loader.exec_module(module)
            setattr(self, name, module)
        popen = patch.object(self.voiceover.subprocess, "Popen")
        self.popen = popen.start()
        self.addCleanup(popen.stop)
        self.command = Mock(returncode=0)
        self.command.communicate.return_value = (b"ok", b"")
        self.activity = Mock(returncode=0)
        self.activity.communicate.return_value = (b"123\n", b"")
        self.popen.side_effect = lambda argv, **kwargs: (
            self.activity if argv[0] == "pgrep" else self.command)
        self.package.get_output_classes = lambda: [
            self.voiceover.VoiceOver, self.system_voiceover.SystemVoiceOver]

    def test_missing_appkit_and_none_initialization_are_output_errors(self):
        for backend in (self.voiceover.VoiceOver, self.system_voiceover.SystemVoiceOver):
            with self.subTest(backend=backend.__name__):
                with patch.dict(sys.modules, {"AppKit": None}):
                    with self.assertRaises(self.base.OutputError):
                        backend()
        self.factory.alloc.return_value.init.return_value = None
        with self.assertRaises(self.base.OutputError):
            self.system_voiceover.SystemVoiceOver()

    def test_osascript_success_returns_stdout(self):
        self.assertEqual(self.voiceover.VoiceOver().run_apple_script('output "message"'), b"ok")

    def test_osascript_failure_surfaces_stderr_for_speech_and_silence(self):
        self.command.returncode = 1
        self.command.communicate.return_value = (b"", b"AppleEvent handler failed")
        backend = self.voiceover.VoiceOver()
        for action in (lambda: backend.speak("message"), backend.silence):
            with self.subTest(action=action):
                with self.assertRaisesRegex(self.base.OutputError, "AppleEvent handler failed"):
                    action()

    def test_osascript_launch_failure_is_output_error(self):
        self.popen.side_effect = FileNotFoundError("osascript missing")
        with self.assertRaisesRegex(self.base.OutputError, "osascript missing"):
            self.voiceover.VoiceOver().speak("message")

    def test_existing_text_escaping_and_interrupt_commands_are_preserved(self):
        self.voiceover.VoiceOver().speak('A "quote" \\ path\ncaf\u00e9', True)
        pipe = self.voiceover.subprocess.PIPE
        self.assertEqual(self.popen.call_args_list, [
            call(["osascript", "-e", 'tell application "voiceover"\noutput ""\nend tell'],
                 stdout=pipe, stderr=pipe),
            call(["osascript", "-e", 'tell application "voiceover"\noutput "A \\"quote\\" \\\\ path\ncaf\u00e9"\nend tell'],
                 stdout=pipe, stderr=pipe)])

    def test_auto_selects_voiceover_then_tts_without_runtime_retry(self):
        output = self.auto.Auto()
        self.assertIsNone(output.output("Keyboard help activated", False))
        self.synth.startSpeakingString_.assert_not_called()
        self.command.returncode = 1
        self.command.communicate.return_value = (b"", b"denied")
        with self.assertRaises(self.base.OutputError):
            output.output("message", False)
        self.synth.startSpeakingString_.assert_not_called()
        self.activity.communicate.return_value = (b"", b"")
        self.assertIsNone(output.output("Keyboard help deactivated", interrupt=True))
        self.assertEqual(self.synth.method_calls[-2:], [
            call.stopSpeaking(), call.startSpeakingString_("Keyboard help deactivated")])

    def test_tts_boolean_result_and_existing_voice_controls(self):
        backend = self.system_voiceover.SystemVoiceOver()
        self.assertEqual(backend.list_voices(), ["Test voice"])
        self.assertEqual(backend.get_voice(), "Test voice")
        self.assertIsNone(backend.set_voice("Test voice"))
        self.synth.setVoice_.assert_called_once_with("voice.id")
        self.synth.rate.return_value = 180.0
        self.synth.volume.return_value = 0.5
        self.assertEqual(backend.get_rate(), 180.0)
        self.assertEqual(backend.get_volume(), 0.5)
        backend.set_rate(200)
        backend.set_volume(0.75)
        self.synth.setRate_.assert_called_once_with(200)
        self.synth.setVolume_.assert_called_once_with(0.75)
        self.factory.isAnyApplicationSpeaking.return_value = True
        self.assertIs(backend.is_speaking(), True)
        for result in (True, False):
            self.synth.startSpeakingString_.return_value = result
            self.assertIs(backend.speak("message", False), result)
        self.activity.communicate.return_value = (b"", b"")
        output = self.auto.Auto()
        self.synth.startSpeakingString_.reset_mock()
        for name, emit in (("provider", backend.output), ("auto", output.output)):
            with self.subTest(output=name):
                with self.assertRaisesRegex(self.base.OutputError, "speech"):
                    emit("message", False)
        self.assertEqual(self.synth.startSpeakingString_.call_args_list, [
            call("message"), call("message")])
        for result in (True, None):
            with self.subTest(braille_result=result):
                backend.braille = Mock(return_value=result)
                self.assertIsNone(backend.output("message", interrupt=True))
                backend.braille.assert_called_once_with("message", interrupt=True)
        self.package.load_library.assert_not_called()


if __name__ == "__main__":
    unittest.main()
