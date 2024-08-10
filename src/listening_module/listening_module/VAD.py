#!/usr/bin/env python3
# NOTE: this example requires PyAudio because it uses the Microphone class

import time
import speech_recognition as sr
from audio import record_to_file, recognize_file, record
import os
#import queue #there is only one background thread running so far, so no need for this yet
import subprocess

def noise_calibration(microphone,recognizer):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

def speak(phrase,prosody_parameters=[100,150,90]):
    print("Speak function called")
    voice_engine = ['espeak']
    volume, speed, pitch = prosody_parameters
    vlm,ptc,spd = ["-a", str(volume)], ['-p', str(pitch)], ['-s',str(speed)]
    #filename=['-w',"./speech.wav"]
    cmd=voice_engine+ptc+vlm+spd+[phrase]
    c = subprocess.Popen(cmd)
    c.wait()
    return True

def keyword_obtention():#tentative, I think google uses a semantic-based model for voice recognition
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

# this is called from the background thread
# def listenCallback(recognizer, audio):
#     try:
#         phrase = recognizer.recognize_google(audio,language=language)
#         print("Google Speech Recognition thinks you said " + phrase)
#     except sr.UnknownValueError:
#         print("Google Speech Recognition could not understand audio")
#     except sr.RequestError as e:
#         print("Could not request results from Google Speech Recognition service; {0}".format(e))

# r = sr.Recognizer()
# m = sr.Microphone()
# print(keyword_obtention())

#with m as source:
#    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

#stop_listening = r.listen_in_background(m, listenCallback)

#for _ in range(50): time.sleep(0.1)  #makes the program do nothing for 5 sec while the thread listens

#print("#######################################") #iteration output divider

#stop_listening(wait_for_stop=False) #stops the thread which is constantly listening

#while True: time.sleep(0.1)   #keeps program runnong while doing nothing
