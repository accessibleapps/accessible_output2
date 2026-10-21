# Goal

Repair the documented combined speech/braille dispatch contract on master before integrating external accessible_output2 PRs, and give the existing hosted workflow a real offline regression suite and package build.

# State

Published as accessibleapps-owned draft PR #24 on master 57bda997d98e87dd78aa049e7021cf777871619b, initial head d9af7c24cfe58b0f0a679d6aaca57f736995d85b. The three production-line changes, six controlled tests and workflow are unchanged. No external fork was written. This note-only update awaits coordinator publication review; actual Claude review, exact final-head hosted green and merge authorization remain gates.

# Decisions and why

- Auto.output delegates to the selected backend's output, as promised by readme.rst. Base Output treats only explicit False as unsupported, preserving usual None returns from real speech/braille methods and the exception when neither channel exists.
- Tests import the real base/auto source under controlled package discovery. Native output discovery is never imported, and a DLL loader mock raises if called. These checks establish dispatch, not heard speech or braille.
- Preserve the existing Linux build job and 3.8/3.9/3.10 matrix, with fatal Flake8 selectors and advisory style output. Use pinned actions, contents:read, nonpersisted checkout credentials, timeout/concurrency, standard-library tests and uv package build. Packaging declarations, support policy, bundled binaries and native loading are unchanged.

# Verification

Historical local evidence: the actively authored tests/test_output.py against unchanged master had one failure (Auto called speak instead of output), two errors (None-returning channels raised RuntimeError) and three passing controls; after the three-line correction all six passed on Python 3.13. Actionlint 1.7.12 and offline zizmor 1.31.1 passed the authored workflow (one suppression). Hosted run 39528266498 passed on initial head d9af7c24 for Python 3.8/3.9/3.10: package install/root import, fatal Flake8, six tests and wheel/sdist build. Advisory style output and existing setuptools deprecation warnings remain. Full CI was not run locally.

# Surprises

Canonical C:/Users/Q/code/accessible_output2 has five pre-existing tracked EOL-only modifications. They remain untouched. All six original external PR heads are archived locally as archive/task6-output2-pr<N>-original. PR #20 also bundles unrelated loader/public find_datafiles removal, package dependency changes and ZDSR DLL removal; those are not included here. PR #18's different DLL/InitTTS ABI proposal still needs vendor provenance and native validation.

# Next step

Return the note-only fast-forward head for coordinator publication review; then obtain actual Claude review and exact final-head hosted green before any merge. Do not publish the separate local ESpeak stack, approve #23's action_required run or execute live AT/native DLL integration.
