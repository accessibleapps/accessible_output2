# Goal

Repair the documented combined speech/braille dispatch contract on master before integrating external accessible_output2 PRs, and give the existing hosted workflow a real offline regression suite and package build.

# State

Local preparation on master 57bda997d98e87dd78aa049e7021cf777871619b. This branch contains only the three production-line changes proposed in PR #20's original dispatch commit, six controlled tests and the existing workflow's bounded read-only CI amendment. No fork or remote branch has been written. Publication and actual Claude review remain coordinator gates.

# Decisions and why

- Auto.output delegates to the selected backend's output, as promised by readme.rst. Base Output treats only explicit False as unsupported, preserving usual None returns from real speech/braille methods and the exception when neither channel exists.
- Tests import the real base/auto source under controlled package discovery. Native output discovery is never imported, and a DLL loader mock raises if called. These checks establish dispatch, not heard speech or braille.
- Preserve the existing Linux build job and 3.8/3.9/3.10 matrix, with fatal Flake8 selectors and advisory style output. Use pinned actions, contents:read, nonpersisted checkout credentials, timeout/concurrency, standard-library tests and uv package build. Packaging declarations, support policy, bundled binaries and native loading are unchanged.

# Verification

The actively authored tests/test_output.py ran against unchanged master: six tests, one failure (Auto called speak instead of output) and two errors (None-returning speech/braille raised RuntimeError). Three controls passed. After the three-line correction the same file passed all six on Python 3.13. Actionlint 1.7.12 and offline zizmor 1.31.1 passed the authored workflow (one zizmor suppression). Full lint/test/build runs belong to hosted CI and were not run locally.

# Surprises

Canonical C:/Users/Q/code/accessible_output2 has five pre-existing tracked EOL-only modifications. They remain untouched. All six original external PR heads are archived locally as archive/task6-output2-pr<N>-original. PR #20 also bundles unrelated loader/public find_datafiles removal, package dependency changes and ZDSR DLL removal; those are not included here. PR #18's different DLL/InitTTS ABI proposal still needs vendor provenance and native validation.

# Next step

Return the complete local diff and exact committed head for coordinator review, then await concrete publication authority. Do not approve #23's action_required run or execute live AT/native DLL integration.
