# Goal

Integrate the narrow initialization-failure intent of AdamMagued's original
accessible_output2 PR #23 into an owned local branch from merged master
32389657b4ab80a85a88e14e61443bf6c57ae19c. Raise the existing OutputError for
ordinary ESpeak initialization exceptions, preserving its Exception hierarchy.

# State

Local-only repair/task6-output2-espeak-integration is based on the verified merged
default 32389657. The three-line source correction imports existing OutputError
and wraps ordinary initialization Exception. The existing tests/test_output.py
loads actual e_speak beside actual base/auto under its stand-in packages. Two
authored regressions block the optional espeak module and native loader, and
restrict Auto discovery to ESpeak. The focused file passes all nine tests.

# Decisions and why

- Smallest production change is three changed lines: import OutputError and
  replace bare-except/print with ordinary Exception-to-OutputError wrapping,
  following the existing backend initialization convention.
- Original PR #23 head 2b931a2dbc70ddf2441034a4ec0c69484b73372a proposed related
  behavior. This owned integration does not carry its RuntimeError hierarchy
  change, extra guards/branches, tests package or native-discovering test.
- Master already continued Auto discovery: failed ESpeak construction returned
  an inactive instance which Auto retained and selection skipped. The intended
  change makes direct construction report OutputError and Auto exclude that
  failed instance; it is not a claim that Auto previously crashed.
- Existing hosted unittest discovery on Python 3.8/3.9/3.10 collects the existing
  test file. No workflow, packaging, support or native-loading change is needed.

# Surprises

Canonical master remains at 57bda997 with five pre-existing dirty files; fetching
advanced only origin/master to merged 32389657. Existing archives preserve the
old canonical/original fork tips, and all older worktrees remain untouched.
archive/task6-output2-pr23-original retains original fork head
2b931a2dbc70ddf2441034a4ec0c69484b73372a; the older owned ESpeak branch remains
repair/task6-output2-espeak at cf3a25c9e9b138399b34791ab558f571201a7592.

# Verification

Only the actively authored tests/test_output.py ran, using Python 3.13.6.
Before production edits its source diff was empty: nine tests ran in 0.113s,
seven original controls passed and the two new regressions failed. Direct
construction did not raise OutputError; Auto returned successfully, selection
returned None, and its list retained one inactive ESpeak. The historical prints
reported the unavailable optional module twice. This was not an Auto crash.

After the three-line correction the same nine tests passed in 0.079s. Both new
regressions assert that the native loader is not called. sys.modules explicitly
blocks espeak/espeak.core, and discovery returns only ESpeak. No other backend,
real ESpeak module, service or audio was constructed. No local full CI was run;
hosted Python 3.8/3.9/3.10 install/lint/unittest/build remains the later gate.

# Next step

Return the complete local source/test/note diff and clean committed head for
coordinator review before publication. Any future publication must use an owned
branch, never the AdamMagued fork or original PR. Exact-head hosted checks and
actual review remain later coordinator-owned gates. No model, native/audio,
full local CI, fork/PR write, publication or merge occurred in this preparation.
