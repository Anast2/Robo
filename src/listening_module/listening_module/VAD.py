#!/usr/bin/env python3
import speech_recognition as sr
from listening_module.audio import record_to_file, recognize_file, record
import subprocess

def noise_calibration(microphone,recognizer):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

def speak(phrase,prosody_parameters=[100,150,90]):
    print("Speak function called")
    voice_engine = ['espeak']
    volume, speed, pitch = prosody_parameters
    vlm,ptc,spd = ["-a", str(volume)], ['-p', str(pitch)], ['-s',str(speed)]
    cmd=voice_engine+ptc+vlm+spd+[phrase]
    c = subprocess.Popen(cmd)
    c.wait()
    return True

def keyword_obtention():
    name = None
    count = 0
    phrase = "Please, say my name!"
    r = sr.Recognizer()
    m = sr.Microphone()

    while 1:
        speak(phrase)
        record_to_file("myname.wav")
        name_rec = recognize_file("myname.wav")
        if count == 0:
            name = name_rec
            count=1
            phrase = "Please, say my name once again!"
        else:
            if name_rec == name:
                count+=1
            else:
                count = 0
            if count == 2:
                return name

