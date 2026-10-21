# Goal
Prepare original PR #13 as an independent owned alternative at current default, preserving its VoiceOver/osascript behavior and richer NSSpeech controls while fixing bounded error/dependency/docs defects. Do not combine its fallback with #16 or claim unavailable AT evidence.

# State
Base f028c6fc65e204a269ae904c4dee4a1a6b167d64; original0f0b34993fb4b271f88b5cb2581d194704d1c70f retained in separate archive/task6-output2-mac13-original-local/-published refs. Canonical master57bda997/five dirty files, original forks and other worktrees are preserved. Independent #16 integration is owned draft #26; this #13 alternative stays local and root owns serialization/publication/review/merge.

# Decisions and why
Keep original VoiceOver signatures/osascript argv/escaping/pgrep selection and SystemVoiceOver controls/priority/Boolean return. Add direct Darwin Cocoa metadata, missing-import/None guards and stderr/status/launch-error propagation through OutputError (about20-30 source/metadata lines beyond original). No speech-time automatic fallback, API rename, platform permission change or native API replacement. Controlled real-source tests fake AppKit/Popen only; safe Mac CI builds and installs wheel metadata, imports providers without constructing or speaking, and runs controlled tests. Existing Linux gate stays unchanged.

# Verification
Python3.13.6, python tests/test_voiceover.py -v against original proposal behavior:7 tests,5 failed assertions/3 errors across subtests in0.115s, with successful stdout and richer controls passing. Failures establish missing-AppKit escaping constructors, unguarded None, discarded status/stderr, raw launch OSError and absent stderr capture. After bounded fixes, the same actively authored file passed all7 in0.082s. Real base/Auto/VoiceOver/SystemVoiceOver source; AppKit/Popen boundaries mocked, no native constructors or subprocesses.

Actionlint1.7.12 -shellcheck= -pyflakes= passed0; once-only zizmor1.31.1 --offline --pedantic exits11 only for the unchanged unnamed Linux build job's informational finding. Added39-line independent Mac Intel3.8/ARM3.10 wheel/install/import/controlled-test gate, with Linux job unchanged. No full local CI/native/osascript/model action.

The matching owned #26 gate established actual dependency red: run39548966763 Intel3.8 job119053528045 resolved Cocoa10.3.2 to core11.1, whose build exits "PyObjC: Need at least Python 3.9"; all Linux and ARM3.10 jobs passed. Official11.0 release notes drop3.8 and11.0/11.1 core setup MIN_PYTHON=(3,9), although11.1 PyPI declares>=3.8. Core10.3.2 provides cp38 Intel/universal2 wheels. Carry the proven narrow Darwin/Python<3.9 core<11 constraint in setup/requirements; other runtimes stay unconstrained. This candidate has no hosted result yet; root must publish/review and require exact-head compatibility gates.

Primary evidence: https://pyobjc.readthedocs.io/en/latest/changelog.html#version-11-0 ; https://raw.githubusercontent.com/ronaldoussoren/pyobjc/v11.1/pyobjc-core/setup.py ; https://pypi.org/pypi/pyobjc-core/11.1/json ; https://pypi.org/pypi/pyobjc-core/10.3.2/json .

# Surprises
Local32c13249a1694281d9c540f0b93748cb1e733f0a is preserved at archive/task6-output2-voiceover-before-extras-key-fix. Matching owned #26 run39550053972 at2e01b7d failed Intel3.8 and Linux3.8: older setuptools combined the inline requirement marker inside a legacy conditional extras key into invalid metadata `pyobjc-core <11 ; sys_platform == "darwin":python_version < "3.9"`;3.9/3.10/ARM passed. Carry the representation correction here: marker-free Darwin entries plus separate combined Darwin/Python<3.9 conditional extras key for core<11. The flat requirements.txt marker stays unchanged. No source/test/workflow change or local CI/audit rerun; this independent candidate still has no hosted result.

NSSpeechSynthesizer is TTS, not another VoiceOver instance; its global isAnyApplicationSpeaking is not a VoiceOver-specific state signal. Preserve the proposed method's selector without promoting that meaning into selection or docs. Native nullable-init/error/permission/interrupt behavior is not reproduced by mocks.

# Next step
Return amended clean local head/full diff and the tiny setup/note correction for root review before any publication. The independent #26 metadata representation correction is separately committed for root review. Exact-head hosted wheel/dependency/import/controlled-test results and real TTS/VoiceOver/permission/interrupt gates remain separate. In particular an active VoiceOver launch/status failure surfaces OutputError without automatic TTS retry; no fork writes or merge.
