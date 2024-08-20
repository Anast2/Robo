#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import speech_recognition as sr
import uuid
from time import time
import subprocess
import sys 
sys.path.append('/home/plantroid/plantroid_ws/src/plantroid_listener/plantroid_listener')
import VAD as vad
from huggingsound import SpeechRecognitionModel

def save_audio(path, data):
    import wave
    import pyaudio
    from struct import pack
    with open(path, "wb") as file:
        file.write(data.get_wav_data())
        file.close()

def voice_emotion_analysis(audio_file):
  model = SpeechRecognitionModel("r-f/wav2vec-english-speech-emotion-recognition ")
  prediction = model(audio_file)
  emotion_map = {"neutral":"neutral","happy":"happy","sad":"sad","anger":"anger","disgust":"anger","surprise":"surprise","fear":"surprise",}
  return emotion_map[prediction["label"].lower()]

class ListenServer(Node):
    block = False
    language = "en-US"
    def __init__(self):
        super().__init__('listen_server')
        self.block_time = time()
        self.publisher = self.create_publisher(String, 'messageTopic', 10)

    def block_callback(self, message):
        self.block = not self.block
        if self.block: self.block_time = time()
        self.get_logger().info(
        "Changed Listening status to: " + str(not self.block))

    def listenCallback(self, recognizer, audio):
        if self.block:
            if time()-self.block_time>15:
                self.block = not self.block
        else:
            print("callback called")
            try:
                #phrase = recognizer.recognize_sphinx(audio,
                #                                      language=self.language)
                phrase = recognizer.recognize_google(audio,
                                                     language=self.language)
                filename = str(uuid.uuid4())
                print("HEARD: " + phrase)
                save_audio("./mem/audio/"+filename, audio)
                emotion_estimate = voice_emotion_analysis("./mem/audio/"+filename)
                self.Publish(phrase.replace(";",",")+";"+filename+";"+emotion_estimate)
            except sr.UnknownValueError:
                print("PockectShphinx could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from PockectShphinx\
                    Recognition service; {0}".format(e))

    def start_listening(self, recognizer):
        print("Starting Listening subprocess...")
        return recognizer.listen_in_background(m, self.listenCallback)

    def stop_listening(self, listener):
        print("Stopping Listening subprocess...")
        try:
            listener(wait_for_stop=False)
            print("Successfully started Listening subprocess.")
            return True
        except:
            print("ERROR: Could not stop the listener subprocess.")
            return False

    def Publish(self, message):
        print("Trying to publish: ", message)
        if not isinstance(message,str):
            message = str(message)
        try:
            msg = String()
            msg.data = message
            self.publisher.publish(msg)
            self.get_logger().info("Published: " + message)
            return True
        except Exception as e:
            print(e)
            print("ERROR: could not send the message through the publisher node.")
            return False

    def getBlock(self):
        self.subscription = self.create_subscription(String,
                                                     'ListenBlockTopic',
                                                     self.block_callback,
                                                     10)
        self.subscription

def main():
    rclpy.init(args=None)
    m = sr.Microphone()
    r = sr.Recognizer()
    vad.noise_calibration(m,r)

    listen_server = ListenServer()
    listen_server.start_listening(r)
    listen_server.getBlock()
    rclpy.spin(listen_server)

if __name__ == "__main__":
    main()
