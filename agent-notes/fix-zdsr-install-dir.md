# Load ZDSR's API DLLs from its install folder

## Goal

Q chose on 2026-11-01 (during the accessibleapps PR triage) to stop bundling
ZDSRAPI.dll / ZDSRAPI_x64.dll and load them from ZDSR's install folder, as
ZDSR's API docs recommend (https://www.zdsr.com/docs/api/zdsr-api: the DLLs
live in `C:\Program Files(x86)\zdsr\zdsr`; ZDSR 26.6 updated them; apps
should read them from the install folder rather than copy them). This
replaces outside PR #18, which only swapped the bundled copies for 2023 builds.

## State

- outputs/zdsr.py loads the DLL from `%ProgramFiles(x86)%\zdsr\zdsr`, then
  `%ProgramFiles%\zdsr\zdsr`. A missing DLL or a ctypes OSError raises
  OutputError, so Auto() skips ZDSR instead of crashing.
- InitTTS now gets the vendor's three arguments (type, channel name,
  key-down interrupt = True). Master passed two.
- Bundled lib/ZDSRAPI*.dll removed.
- tests/test_output.py covers not installed, load failure, and loading from
  the install folder; the file passes locally (12 tests).

## Decisions and why

- No registry lookup: the vendor documents only the folder path.
- GetSpeakState()==1 (version mismatch) still counts as active, unchanged
  from master; Q left it out of scope.

## Next step

PR CI, then merge after review; close #18 pointing at this PR. Not verified
against a real ZDSR install (none on this machine).
