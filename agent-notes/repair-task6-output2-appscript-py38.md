# Goal
Fix the inherited Darwin/Python3.8 appscript installation failure on current default before either macOS feature integration advances. Smallest scope: two setup metadata lines,39 reused hosted Mac job lines and this living note; no backend/test/support-policy change.

# State
Isolated repair/task6-output2-appscript-py38 starts at actual remote default f028c6fc65e204a269ae904c4dee4a1a6b167d64. Canonical master57bda997/five preexisting dirty files, original forks/archives, owned26 ffe328de4e98ad793857bbae522f7f9afdc9db16 and independent13 b55597e788de136b81e2b215c8340d86c2ae111d remain untouched. Root owns publication, actual external review, hosted verification and merge.

# Decisions and why
Current default and owned26 both declare the same unbounded Darwin appscript requirement. Actual26 run39550521452 reaches appscript1.5.0 source build on Intel/Python3.8 and fails ext/ae.c462/472 availability errors: AEDeterminePermissionToAutomateTarget requires macOS10.14 while interpreter/build target is10.9; setup also defines MIN_REQUIRED10.12. This is inherited baseline dependency selection, separate from Cocoa/new TTS.

Official PyPI artifacts for1.3.0/1.4.0/1.5.0 have no cp38 wheels and no declared RequiresPython restriction;1.2.5 has cp38 macosx10_9 Intel/universal2 wheels. Verified each downloaded source archive against PyPI SHA256 and inspected it in memory without executing/extracting code. Upstream1.2.5-to1.3.0 commit5bb58980a79b89502eb59a1e216f9a0af331217b explicitly removes cp38 from CIBW_BUILD, adding cp313; its message says "Added support for Python3.13 and dropped3.8". The1.2.5 release also includes the synchronous-background-Apple-event Mach-port leak fix. All four README requirements still say Python3.7+/macOS10.9+. Their lib/appscript/reference.py is byte-identical, SHA256 bd5994a40c46ad927326620eb6d50b6e752a0c99817ce79a339459668b8bcab4, including app construction, dynamic command dispatch and isrunning. Preserve current appscript.app("voiceover")/output/isrunning backend exactly. Use appscript<1.3 only Darwin/Python<3.9 via separate legacy conditional extras key, selecting the published compatible wheel family without constraining newer runtimes. No deployment-target override or disabled compiler errors.

Primary evidence: https://github.com/hhas/appscript/compare/1.2.5...1.3.0 ; https://github.com/hhas/appscript/commit/5bb58980a79b89502eb59a1e216f9a0af331217b ; https://github.com/hhas/appscript/releases/tag/1.2.5 ; https://pypi.org/pypi/appscript/1.2.5/json ; https://pypi.org/pypi/appscript/1.3.0/json ; https://pypi.org/pypi/appscript/1.4.0/json ; https://pypi.org/pypi/appscript/1.5.0/json . Exact source artifacts/URLs and API equality are included in the handoff report.

Reuse safe Mac Intel3.8/ARM3.10 wheel/dependency/import/current9 controlled-test gate, retaining existing Linux jobs exactly. Smoke imports only current installed appscript/VoiceOver from runner.temp; no constructor, speech, Apple event, Cocoa or new TTS registration.

# Verification
Actual failing hosted installation is the inherited red; no local full CI/build/install/native execution. New candidate hosted results pending root review/publication. Existing9 tests remain unchanged. Once-only actionlint1.7.12 with -shellcheck= -pyflakes= passed exit0. Zizmor1.31.1 --offline --pedantic exits11 for only the inherited informational anonymous-definition on the unchanged Linux build job; no suppression or unrelated fix. No native/AT success inferred.

# Surprises
The source README advertises3.7+/10.9+ even for1.5.0 and its setup MIN_REQUIRED is10.12; wheel availability and actual build errors, rather than an invented support-policy drop, justify this narrow Python3.8 compatibility bound. Native VoiceOver delivery and deployment-runtime behavior are not established by metadata or import/mocked tests.

# Next step
Return complete clean baseline head/diff and primary source evidence for root review before any publication. Require all existing Linux and both new Mac exact-head gates green, then actual review/merge through root. Rebase either feature candidate only after root confirms the prerequisite actually landed. Keep both feature tips and canonical dirty work intact.
