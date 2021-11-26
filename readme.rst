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
- Microsoft Speech API
- VoiceOver
- E-Speak


Braille:

- JAWS for Windows
- NVDA
- Window Eyes
- System Access
- Supernova and other Dolphin products

Note for Apple Users:
------------------
VoiceOver is supported by accessible_output2 in two different ways.

The first way is through Apple Script, which requires the user to enable the VoiceOver setting "Allow Voiceover to be controled by Apple Script". This method will provide output to the running     instance of voiceover. This no longer checks if VoiceOver has this setting enabled or not due to the expensive cost of running an Apple Script query everytime is_active is called. This means that if the VoiceOver setting is disabled, and VoiceOver is running, an error will be thrown by VoiceOver if you attempt to speak with VoiceOver, rather than automaticly switching to the secondary speech output system. Application developers that are providing support for VoiceOver are encouraged to provide some notification to the user about enabling Voiceover to be controled by Apple Script, or to just disable VoiceOver altogether to use the default speech output.

If Voiceover is not running, The NSSpeechSynthesizer object is used. This will use a separate instance of VoiceOver, using default VoiceOver settings which are customizable from the provided class similar to SAPI5 for Windows.

Error thrown by VoiceOver if Apple Script is disabled: (This error can not be caught in python )

execution error: VoiceOver got an error: AppleEvent handler failed.
