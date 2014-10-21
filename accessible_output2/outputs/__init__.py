import platform
if platform.system() == 'Windows':
 import nvda
 import jaws
 import sapi5
 import window_eyes
 import system_access
 import dolphin
 import pc_talker
 #import sapi4

if platform.system() == 'Darwin':
 import voiceover
 import say

import auto
