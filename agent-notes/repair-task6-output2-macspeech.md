# Goal
Integrate original macOS PR #16 onto current default with the smallest dependency/constructor repair and safe hosted compatibility coverage. Keep speech/selection/API behavior and all existing support/source/tests; no live audio or VoiceOver.

# State
Base f028c6fc65e204a269ae904c4dee4a1a6b167d64; original e5a9df5e988994177c17e7331274d6b2a3a0c20e preserved under separate archive/task6-output2-mac16-original-local/-published refs. Canonical master57bda997 and its five dirty files, original external forks, other worktrees and original archives remain untouched. Independent #13 alternative starts at the same default, without duplicate fallback registration here.

# Decisions and why
Retain original MacSpeech class/signature/priority101/system flag/Boolean return/interrupt calls and one Darwin discovery line. Correct direct Darwin AppKit provider in setup/requirements, convert missing import and None construction to existing OutputError (about8-12 lines beyond original). Extend controlled source-import tests using real base/Auto/VoiceOver/MacSpeech and mocked native boundaries (about100 lines). Existing Linux jobs remain; add macOS15 Intel/Python3.8 and ARM/Python3.10 built-wheel dependency/import/unit coverage (about40-50 workflow lines), matching the existing minimum and Intel/ARM contract. No actual speaking, native constructors or Apple events run locally or in the smoke import.

# Verification
Original MacSpeech source was byte-identical to archived #16 blob1710b860cd5e1f14ea1ab7e72d682d69536e4820 before the fix. Python3.13.6, python tests/test_macspeech.py -v: six tests, four controls passed, missing-AppKit escaped Auto as ModuleNotFoundError and None initialization failed its OutputError assertion (one error/one failure in0.105s). After the bounded guards the same actively authored file passed all six in0.052s. AppKit/appscript are mocked at native boundaries; real base/Auto/VoiceOver/MacSpeech source is loaded. No native constructor, speech or Apple event runs.

Actionlint1.7.12 with the established -shellcheck= -pyflakes= flags passed, exit0. Zizmor1.31.1 --offline --pedantic reports one informational anonymous-definition finding for the unchanged Linux build job, exit11; this is visible in the exact default workflow too, not a clean audit claim or a new suppression. Authored workflow adds39 lines, preserves the Linux job exactly, builds wheel/sdist, installs the wheel's declared dependencies, checks consistency and imports installed actual providers from runner.temp before controlled tests on Intel3.8/ARM3.10. Actual hosted package/dependency/import/unit results are pending; no full local CI or additional audit rerun.

# Surprises
Current default object initially required a normal fetch; remote matched the assigned exact f028c6fc head. Appscript metadata does not declare Cocoa; no universal AppKit absence or Python2-support claim. Apple documents nullable voice initialization, not a reproduced native init() failure.

# Next step
Return complete clean local head/diff and focused evidence for root review before publication, then prepare #13 independently at the same base. Root owns publication/review/merge; actual TTS/AT delivery remains unavailable and cannot be inferred from mocked/import/package success. No external fork or duplicate TTS registration is changed.
