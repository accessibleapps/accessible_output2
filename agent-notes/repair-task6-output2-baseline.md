# Goal

Repair the documented combined speech/braille dispatch contract on master before integrating external accessible_output2 PRs, preserve existing positional speech options, and give the existing hosted workflow a real offline regression suite and package build.

# State

Published as accessibleapps-owned draft PR #24 on master 57bda997d98e87dd78aa049e7021cf777871619b, current published head ab1f68e3bba79cf43fb559e7774f48790d4f8a75 (initial d9af7c24cfe58b0f0a679d6aaca57f736995d85b). The lint correction is published and hosted run 39536028829 succeeded at ab1f68e. Isolated repair/task6-output2-positional starts at that exact head. Separate archive/task6-output2-positional-published and -local refs preserve ab1f68e, -original-local preserves 1c5dfad7, and -canonical preserves 57bda997. Original worktrees/branches, the separate ESpeak stack and five dirty canonical files are untouched. No external fork was written; final-head review/hosted/merge gates remain coordinator-owned.

# Decisions and why

- Auto.output delegates to the selected backend's output, as promised by readme.rst. Base Output treats only explicit False as unsupported, preserving usual None returns from real speech/braille methods and the exception when neither channel exists.
- Chicken Nugget default dcb4c237f0b7d4907e156990716a8cf80886a708, chicken_nugget/interface.py:1352/1354, calls output with translated keyboard-help text and positional False. Preserve this real speech interrupt argument by accepting *args in base Output.output and forwarding it only to speak; keyword options still reach both channels. NVDA and JAWS speak accept positional interrupt, while their braille methods accept text and keyword options. No new option mapping or native behavior is introduced.
- Tests import the real base/auto source under controlled package discovery. Native output discovery is never imported, and a DLL loader mock raises if called. These checks establish dispatch, not heard speech or braille.
- Preserve the existing Linux build job and 3.8/3.9/3.10 matrix, with fatal Flake8 selectors and advisory style output. Use pinned actions, contents:read, nonpersisted checkout credentials, timeout/concurrency, standard-library tests and uv package build. Packaging declarations, support policy, bundled binaries and native loading are unchanged.

# Verification

Historical local evidence: the actively authored tests/test_output.py against unchanged master had one failure (Auto called speak instead of output), two errors (None-returning channels raised RuntimeError) and three passing controls; after the three-line correction all six passed on Python 3.13. Actionlint 1.7.12 and offline zizmor 1.31.1 passed the authored workflow (one suppression). Hosted run 39528266498 passed on initial head d9af7c24 for Python 3.8/3.9/3.10: package install/root import, fatal Flake8, six tests and wheel/sdist build. Advisory style output and existing setuptools deprecation warnings remain. Full CI was not run locally.

Historical pre-lint-correction run 39528780879 is green for Python 3.8/3.9/3.10. Its actual 3.8 log, job 118989580264, shows advisory Flake8 paths under ./.venv/lib/python3.8/site-packages/platformdirs and ./build/lib/accessible_output2. The workflow creates .venv with uv venv and build/lib during package installation, then ran both flake8 . commands without excluding them. Published ab1f68e adds --extend-exclude=.venv,build,dist to both commands. Fatal selectors E9,F63,F7,F82 and advisory --exit-zero/limits remain unchanged. Its static validation passed actionlint 1.7.12; offline zizmor 1.31.1 reported no findings (one tool-reported suppression, no inline ignore added). Hosted run 39536028829 subsequently succeeded at ab1f68e.

Positional compatibility regression: before product edits, accessible_output2 source diff against ab1f68e was empty. Only the actively authored tests/test_output.py ran with Python 3.13.6: seven tests, six original controls passing and two errors in the new keyboard-help subtests (0.080s). Both real text/False calls reached Auto.output then raised TypeError: Output.output() takes 2 positional arguments but 3 were given. The new fake backend inherits real base Output.output and defines strict speak(text, interrupt=False)/braille(text, **options) methods returning None, with no Mock.output masking the signature.

In-memory characterization extracted the exact master 57bda997 Auto.output method by AST, using the existing controlled source-import fixture: both keyboard-help text/False calls returned None and reached speak with False; the mocked native loader was never called. This confirms compatibility with the old Auto path without running application/native discovery. After the two-line base correction, the same actively authored file passed all seven tests in 0.059s. The new test also checks braille receives only text and keyword options. All six original tests/assertions, literal-False unsupported handling, workflow, packaging and support declarations remain unchanged.

# Surprises

Canonical C:/Users/Q/code/accessible_output2 has five pre-existing tracked EOL-only modifications. They remain untouched. All six original external PR heads are archived locally as archive/task6-output2-pr<N>-original. PR #20 also bundles unrelated loader/public find_datafiles removal, package dependency changes and ZDSR DLL removal; those are not included here. PR #18's different DLL/InitTTS ABI proposal still needs vendor provenance and native validation.

# Next step

Return the complete base-source/existing-test/existing-note correction and exact local head for coordinator review before publication. This coding-only task invokes no model, blocked review worker, merge, old-description/comment, settings/security or native action. Fresh final-head hosted results and review are still required after separately authorized publication. Do not change the separate ESpeak stack, approve #23's action_required run or execute live AT/native DLL integration.
