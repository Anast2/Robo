#!/usr/bin/env python3
import socket
import subprocess 
from balacoon_tts import TTS, SpeechUtterance
from ast import literal_eval

def espeak_ng(msg): #  lightest option of all, worst quality of all
    data = literal_eval(msg.data)
    speech_content = data[0]
    volume, speed, pitch = data[1]
    vlm,ptc,spd = ["-a", str(volume)], ['-p', str(pitch)], ['-s',str(speed)]
    cmd = ["espeak-ng"]+["-v","en-us+f3"]+ptc+vlm+spd+[speech_content]
    return subprocess.Popen(cmd)    

def tortoise(msg): pass  # Heavy model, but high quality results.
#  TODO: implement


def tortoise_request(msg): pass  # Heavy model, but high quality results. Calls remote server, but adds latency.
#  TODO: implement


def balacoon(msg): pass  # lighter model good for edge devices, lower quality results.
#  TODO: implement


def balacoon_request(msg): pass  # lighter model good for edge devices, lower quality results. Calls remote server, but adds latency.
#  TODO: implement


def tts_call(msg, mode="local", model="espeak_ng", IP=None, PORT=None):  # 

    if model == "espeak-ng":
        process = espeak_ng(msg)
        process_done = process.poll() is None
        while process_done:
            process_done = process.poll() is None
        print("done")
    elif model == "tortoise":
        if mode == "local":
            tortoise(msg)
        else: 
            tortoise_request(msg, IP, PORT)
    
    elif model == "balacoon":
        if mode == "local": 
            balacoon(msg)
        else:
            balacoon_request(msg, IP, PORT)
    
    else: 
        pass