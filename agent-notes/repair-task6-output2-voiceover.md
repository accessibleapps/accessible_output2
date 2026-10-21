# Goal
Prepare original PR #13 as an independent owned alternative at current default, preserving its VoiceOver/osascript behavior and richer NSSpeech controls while fixing bounded error/dependency/docs defects. Do not combine its fallback with #16 or claim unavailable AT evidence.

# State
Owned #28 is published at70a1115a17e7c67174d8537349177757f21dffc3 on landed baseline27/default2ed2c5785fa48860325c40634ba4e76dbe79fc44; pre-cleanup tip preserved at archive/task6-output2-voiceover-before-unused-appscript-fix. Its actual gated review REQUEST_CHANGES identifies verified F1 unused appscript and a separately held conditional F2 Boolean-contract concern. Earlier rebase/original0f0b34993fb4b271f88b5cb2581d194704d1c70f archives, canonical master57bda997/five dirty files, forks and other worktrees remain preserved. Root owns publication/review/merge; owned26 is unchanged.

# Decisions and why
Keep original VoiceOver signatures/osascript argv/escaping/pgrep selection and SystemVoiceOver controls/priority/Boolean return. Add direct Darwin Cocoa metadata, missing-import/None guards and stderr/status/launch-error propagation through OutputError (about20-30 source/metadata lines beyond original). No speech-time automatic fallback, API rename, platform permission change or native API replacement. Controlled real-source tests fake AppKit/Popen only; safe Mac CI builds and installs wheel metadata, imports providers without constructing or speaking, and runs controlled tests. Existing Linux gate stays unchanged.

# Verification
Python3.13.6, python tests/test_voiceover.py -v against original proposal behavior:7 tests,5 failed assertions/3 errors across subtests in0.115s, with successful stdout and richer controls passing. Failures establish missing-AppKit escaping constructors, unguarded None, discarded status/stderr, raw launch OSError and absent stderr capture. After bounded fixes, the same actively authored file passed all7 in0.082s. Real base/Auto/VoiceOver/SystemVoiceOver source; AppKit/Popen boundaries mocked, no native constructors or subprocesses.

Initial authored-workflow actionlint1.7.12 -shellcheck= -pyflakes= passed0; once-only zizmor1.31.1 --offline --pedantic exits11 only for the unnamed Linux build job's informational finding. The39-line Mac Intel3.8/ARM3.10 job is now inherited from baseline27; this feature changes its provider smoke imports. No local full CI/native/osascript/model action or audit rerun for this cleanup.

Published70a1115a actual run39553949462 succeeded on all5jobs (Linux3.8/3.9/3.10, Intel3.8, ARM3.10); existing16 controlled tests per leg and installed-wheel provider imports passed. ARM installed/built appscript1.5.0 despite no package-source consumer. Fresh PR/head/run read confirmed these results before cleanup. These characterize pre-cleanup behavior; new cleanup head hosted results and review are pending.

The matching owned #26 gate established historical dependency red: run39548966763 Intel3.8 job119053528045 resolved Cocoa10.3.2 to core11.1, whose build exits "PyObjC: Need at least Python 3.9"; all Linux and ARM3.10 jobs passed. Official11.0 release notes drop3.8 and11.0/11.1 core setup MIN_PYTHON=(3,9), although11.1 PyPI declares>=3.8. Core10.3.2 provides cp38 Intel/universal2 wheels. Retain the proven narrow Darwin/Python<3.9 core<11 constraint in setup/requirements; other runtimes stay unconstrained.

Primary evidence: https://pyobjc.readthedocs.io/en/latest/changelog.html#version-11-0 ; https://raw.githubusercontent.com/ronaldoussoren/pyobjc/v11.1/pyobjc-core/setup.py ; https://pypi.org/pypi/pyobjc-core/11.1/json ; https://pypi.org/pypi/pyobjc-core/10.3.2/json .

# Surprises
Verified F1 cleanup only: rg appscript has no matches anywhere in package source; VoiceOver uses osascript/AppKit. Remove unused appscript, its Python3.8 bound/comment and smoke import/version print. Retain Cocoa/core bound/comment, all source/APIs/tests/assertions/selection/returns, requirements and other CI commands. Baseline27 and owned26 still need their appscript-based VoiceOver and are untouched.

F2 remains held: SystemVoiceOver.speak returns the original native Boolean; base.Output.output maps literal False plus unsupported braille to RuntimeError. Source/tests characterize that conditional contract, but no real native False producer/downstream outage was established. Converting speak's False to OutputError would alter the explicitly preserved Boolean API. No policy change or new test is authorized here; actual native delivery/permission/interruption and False behavior need genuine evidence.

Baseline27 really landed after actual review/all5green run39551826791 (root evidence), supplying appscript<1.3 and safe Mac job. Real setup/workflow replay conflicts resolved with appscript<1.3 plus pyobjc-core<11 together in one Darwin/Python<3.9 conditional extras key, marker-free Darwin Cocoa/appscript entries and one inherited baseline Mac job with only reviewed alternative-specific smoke import/name delta. Backend source, tests/assertions, requirements and prior feature workflow stay byte-identical to pre-rebase archive. No source/test correction or local test/fullCI/audit/native action.

Local32c13249a1694281d9c540f0b93748cb1e733f0a is preserved at archive/task6-output2-voiceover-before-extras-key-fix. Historical owned #26 run39550053972 at2e01b7d failed Intel3.8 and Linux3.8: older setuptools combined the inline requirement marker inside a legacy conditional extras key into invalid metadata `pyobjc-core <11 ; sys_platform == "darwin":python_version < "3.9"`;3.9/3.10/ARM passed. The representation correction uses marker-free Darwin entries plus separate Darwin/Python<3.9 conditional extras key for core<11; retain this syntax and flat requirements.txt marker.

NSSpeechSynthesizer is TTS, not another VoiceOver instance; its global isAnyApplicationSpeaking is not a VoiceOver-specific state signal. Preserve the proposed method's selector without promoting that meaning into selection or docs. Native nullable-init/error/permission/interrupt behavior is not reproduced by mocks.

# Next step
Return clean fast-forward F1-only cleanup head and full tiny diff/preservation evidence for root review before guarded #28 publication. Require fresh exact-head hosted results and actual review. Genuine TTS/VoiceOver/permission/interruption gates and F2 conditional contract concern remain explicitly held. Active VoiceOver launch/status failure still surfaces OutputError without automatic TTS retry; no fork writes or merge waiver.
