# Goal

Repair the documented combined speech/braille dispatch contract on master before integrating external accessible_output2 PRs, and give the existing hosted workflow a real offline regression suite and package build.

# State

Published as accessibleapps-owned draft PR #24 on master 57bda997d98e87dd78aa049e7021cf777871619b, current head 1c5dfad7d810bbdcfe3a7d6fadf41873522ac871 (initial d9af7c24cfe58b0f0a679d6aaca57f736995d85b). Current head's three Python jobs are hosted green, but its reviewed workflow scope needs the bounded correction below. The isolated follow-up branch repair/task6-output2-lint-scope starts at exact current head; separate archive/task6-output2-lint-local and archive/task6-output2-lint-published refs retain it, with a canonical archive as well. Original worktrees/branches and dirty canonical files are untouched. No external fork was written; final-head review/hosted/merge gates remain coordinator-owned.

# Decisions and why

- Auto.output delegates to the selected backend's output, as promised by readme.rst. Base Output treats only explicit False as unsupported, preserving usual None returns from real speech/braille methods and the exception when neither channel exists.
- Tests import the real base/auto source under controlled package discovery. Native output discovery is never imported, and a DLL loader mock raises if called. These checks establish dispatch, not heard speech or braille.
- Preserve the existing Linux build job and 3.8/3.9/3.10 matrix, with fatal Flake8 selectors and advisory style output. Use pinned actions, contents:read, nonpersisted checkout credentials, timeout/concurrency, standard-library tests and uv package build. Packaging declarations, support policy, bundled binaries and native loading are unchanged.

# Verification

Historical local evidence: the actively authored tests/test_output.py against unchanged master had one failure (Auto called speak instead of output), two errors (None-returning channels raised RuntimeError) and three passing controls; after the three-line correction all six passed on Python 3.13. Actionlint 1.7.12 and offline zizmor 1.31.1 passed the authored workflow (one suppression). Hosted run 39528266498 passed on initial head d9af7c24 for Python 3.8/3.9/3.10: package install/root import, fatal Flake8, six tests and wheel/sdist build. Advisory style output and existing setuptools deprecation warnings remain. Full CI was not run locally.

Current-head hosted run 39528780879 is green for Python 3.8/3.9/3.10. Its actual 3.8 log, job 118989580264, shows advisory Flake8 paths under ./.venv/lib/python3.8/site-packages/platformdirs and ./build/lib/accessible_output2. The workflow creates .venv with uv venv and build/lib during package installation, then runs both flake8 . commands without excluding them. The narrow correction adds --extend-exclude=.venv,build,dist to both commands. Fatal selectors E9,F63,F7,F82 and advisory --exit-zero/limits remain unchanged. Product source, six tests, imports/native behavior, packaging/support assertions and all other workflow steps are unchanged. Static follow-up validation: actionlint 1.7.12 passed; offline zizmor 1.31.1 reported no findings (one tool-reported suppression, no inline ignore added). No local lint/full tests/imports/native execution; corrected-head hosted results remain pending publication.

# Surprises

Canonical C:/Users/Q/code/accessible_output2 has five pre-existing tracked EOL-only modifications. They remain untouched. All six original external PR heads are archived locally as archive/task6-output2-pr<N>-original. PR #20 also bundles unrelated loader/public find_datafiles removal, package dependency changes and ZDSR DLL removal; those are not included here. PR #18's different DLL/InitTTS ABI proposal still needs vendor provenance and native validation.

# Next step

Return the complete two-file workflow/note correction and exact local head for coordinator review before publication. This coding-only task invokes no model, blocked review worker, merge, old-description/comment, settings/security or native action. Fresh final-head hosted results and review are still required after separately authorized publication. Do not change the separate ESpeak stack, approve #23's action_required run or execute live AT/native DLL integration.
