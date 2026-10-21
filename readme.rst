Accessible Output 2: Make your app speak
==================================================

Accessible Output 2 is an MIT licensed library for speaking and brailling through multiple screen readers and other accessibility systems.

Accessible Output 2 makes selection of the appropriate speech and Braille output a snap, and also allows the programmer to select and use a specific output, for instance to force speaking through the Microsoft Speech API even if the user has a screen reader loaded.

.. code-block:: python

    >>> import accessible_output2.outputs.auto
    >>> o = accessible_output2.outputs.auto.Auto()
    >>> o.output("Some text") #attempts to both speak and braille the given text through the first available output
    >>> o.speak("Some other text", interrupt=True) #Speak some text through the output, without brailling it, and interrupt the currently-speaking text if any

Accessible Output 2 makes it simple to add spoken and brailled notifications to your applications on multiple platforms, facilitating accessibility for the visually impaired and also providing a nice alternative means of providing notifications to a sighted user.

Supported Outputs:
------------------
Speech:

- JAWS for Windows
- NVDA
- Window Eyes
- System Access
- Supernova and other Dolphin products
- PC Talker
- ZDSR
- Microsoft Speech API
- VoiceOver
- macOS NSSpeechSynthesizer


Braille:

- JAWS for Windows
- NVDA
- Window Eyes
- System Access
- Supernova and other Dolphin products

Note for Apple Users:
---------------------
VoiceOver sends AppleScript output to the running screen reader and requires
the existing "Allow AppleScript to control VoiceOver" setting. Its activity
check detects the process; it does not verify scripting permission. A failed
osascript launch or nonzero command result raises OutputError with the error
message. Auto does not retry another backend after a speech-time error.

When VoiceOver is inactive, SystemVoiceOver provides system text-to-speech
through NSSpeechSynthesizer. This is separate from VoiceOver and uses the
system's default speech voice. Its voice, rate and volume controls configure
that synthesizer. The proposed is_speaking methods use NSSpeechSynthesizer's
global speech-activity query, not a VoiceOver-specific state check.

