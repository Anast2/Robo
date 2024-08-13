#!/usr/bin/env python3
import socket
import subprocess 
from balacoon_tts import TTS, SpeechUtterance

def espeak_ng(msg): #  lightest option of all, worst quality of all
    speech_content = msg[0]
    volume, speed, pitch = msg[1]
    vlm,ptc,spd = ["-a", str(volume)], ['-p', str(pitch)], ['-s',str(speed)]
    cmd = ["espeak-ng"]+["-v","en-us+f3"]+ptc+vlm+spd+[speech_content]
    return subprocess.Popen(cmd)    


def tortoise(msg): pass #  Heavy model, but high quality results
#  TODO: implement


def tortoise_request(msg): pass #  Heavy model, but high quality results, call from remote server, adds latency
#  TODO: implement


def balacoon(msg): pass  #  lighter model good for edge devices, lower quality results
#  TODO: implement