# Goal
Prepare original PR #13 as an independent owned alternative at current default, preserving its VoiceOver/osascript behavior and richer NSSpeech controls while fixing bounded error/dependency/docs defects. Do not combine its fallback with #16 or claim unavailable AT evidence.

# State
Base f028c6fc65e204a269ae904c4dee4a1a6b167d64; original0f0b34993fb4b271f88b5cb2581d194704d1c70f retained in separate archive/task6-output2-mac13-original-local/-published refs. Canonical master57bda997/five dirty files, original forks and other worktrees are preserved. Independent #16 candidate remains separate; root owns serialization/publication/review/merge.

# Decisions and why
Keep original VoiceOver signatures/osascript argv/escaping/pgrep selection and SystemVoiceOver controls/priority/Boolean return. Add direct Darwin Cocoa metadata, missing-import/None guards and stderr/status/launch-error propagation through OutputError (about20-30 source/metadata lines beyond original). No speech-time automatic fallback, API rename, platform permission change or native API replacement. Controlled real-source tests fake AppKit/Popen only; safe Mac CI builds and installs wheel metadata, imports providers without constructing or speaking, and runs controlled tests. Existing Linux gate stays unchanged.

# Verification
Python3.13.6, python tests/test_voiceover.py -v against original proposal behavior:7 tests,5 failed assertions/3 errors across subtests in0.115s, with successful stdout and richer controls passing. Failures establish missing-AppKit escaping constructors, unguarded None, discarded status/stderr, raw launch OSError and absent stderr capture. After bounded fixes, the same actively authored file passed all7 in0.082s. Real base/Auto/VoiceOver/SystemVoiceOver source; AppKit/Popen boundaries mocked, no native constructors or subprocesses.

Actionlint1.7.12 -shellcheck= -pyflakes= passed0; once-only zizmor1.31.1 --offline --pedantic exits11 only for the unchanged unnamed Linux build job's informational finding. Added39-line independent Mac Intel3.8/ARM3.10 wheel/install/import/controlled-test gate, with Linux job unchanged. No full local CI/native/osascript/model action. This is a clean intermediate checkpoint before the proven Python3.8 dependency constraint below is carried over.

# Surprises
NSSpeechSynthesizer is TTS, not another VoiceOver instance; its global isAnyApplicationSpeaking is not a VoiceOver-specific state signal. Preserve the proposed method's selector without promoting that meaning into selection or docs. Native nullable-init/error/permission/interrupt behavior is not reproduced by mocks.

# Next step
Pause this independent candidate at a clean commit while repairing the actual hosted #26 Intel3.8 Cocoa/core compatibility failure first. Root requested primary verification of the PyObjC11 Python3.9 minimum and the narrow Darwin/Python<3.9 core<11 constraint; carry that verified constraint here on resume. Return final clean local head/full diff to root before any publication. Exact-head hosted results and real TTS/VoiceOver/permission/interrupt gates remain separate; no fork writes or merge.
