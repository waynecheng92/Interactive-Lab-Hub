#https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)

#!/bin/bash
say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }
#say $*
say " Hey can I have your number?"
python rizz_recording.py -m en -f number.txt
say " Got you, so your number is"
value=`cat number.txt`
say "$value"
say " I have saved it in my contact"
