# Goal
PR #28 (branch repair/task6-output2-voiceover) is the macOS speech direction for accessible_output2: original PR #13's VoiceOver (osascript) output plus SystemVoiceOver (NSSpeechSynthesizer) text-to-speech, with fixed error, dependency and docs defects. Q chose #28 over #26 on 2026-11-01; #26, #16 and #13 are closed.

# State
2026-11-01: PR #28 open against master, not merged. The branch carries the original proposal, the Darwin/Python 3.8 pyobjc-core<11 constraint, removal of unused appscript, and the combined-output error repair (SystemVoiceOver.output raises OutputError only when speech and braille both return False).

Review fixes applied 2026-11-01 in one commit (CI result for it comes from the PR checks after the lead pushes):
- SystemVoiceOver.name is "macOS NSSpeechSynthesizer", so app_framework's output log no longer reports plain TTS as "VoiceOver". Style follows "Linux ESpeak"/"Linux Speech Dispatcher" and the readme's output list.
- The comment in VoiceOver.speak describes what the code does: silence() waits for its osascript process to exit before the new text is sent. The old comment's timing claim contradicted the blocking communicate() call.
- readme.rst (PyPI long description) describes the shipped is_speaking behaviour instead of "proposed" methods.

Pending: a real-Mac test with VoiceOver and with system speech. Mocks do not show native delivery, AppleScript permission, interruption or voice-control behaviour.

# Decisions and why
Keep original VoiceOver signatures, osascript argv/escaping and pgrep selection, and SystemVoiceOver controls, priority and Boolean speak return. Errors from osascript launch, nonzero exit (with stderr) and missing AppKit/None init surface as OutputError. No speech-time automatic fallback to another output, no API rename.

Dependencies: pyobjc-core 11.x needs Python 3.9 (11.0 release notes; 11.0/11.1 setup.py MIN_PYTHON=(3,9)), so Darwin/Python<3.9 is constrained to pyobjc-core<11 through a separate conditional extras key; an inline marker inside a conditional extras key produced invalid metadata on older setuptools. Primary evidence: https://pyobjc.readthedocs.io/en/latest/changelog.html#version-11-0 ; https://raw.githubusercontent.com/ronaldoussoren/pyobjc/v11.1/pyobjc-core/setup.py ; https://pypi.org/pypi/pyobjc-core/11.1/json ; https://pypi.org/pypi/pyobjc-core/10.3.2/json .

Tests (tests/test_voiceover.py) run the real package source with AppKit and Popen faked; the Mac CI jobs build and install the wheel and import both providers without constructing or speaking.

# Surprises
NSSpeechSynthesizer is plain TTS, not VoiceOver; isAnyApplicationSpeaking is global speech activity, not VoiceOver state. That is why the docs and the new output name avoid calling it VoiceOver.

# Next step
Lead pushes the review-fix commit and reads PR #28's checks. Then real-Mac testing of VoiceOver and system speech before merge.
