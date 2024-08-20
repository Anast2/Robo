#!/usr/bin/env python3
import pandas as pd
import nltk 
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.chat.util import Chat, reflections
from transformers import pipeline

# NOTE: if your robot has low memory, it is better to uncomment the model loading line in the sentiment_analysis function, but it will increase inference time, since the model needs to be loaded. 
sentiment_classifier = pipeline("text-classification",model='vamossyd/emtract-distilbert-base-uncased-emotion', return_all_scores=True)

default_pairs = [
[
  r"(hi|hello|howdy|salutations|oy|oi|hola) (.*)",
  ["Hello!","Hi!","Hello, my friend!"]
],
[
  r"my name is (.*)",
  ["Hello %1, How are you today",]
],
[
  r"what is your name",
  ["My name is Plantroid!","I'm called Plantroid!","My friends call me Plantroid!",]
],
[
  r"who are you",
  ["I'm Plantroid!","My creator told me I am Plantroid","I am the amazing plant carrying robot Plantroid!"]
],
[
  r"do you love humans",
  ["yes!"]
],
[
  r"do you need food",
  ["no!"]
],
[
  r"how are you",
  ["Great as always! how about you ?",]
],
[
  r"sorry (.*)",
  ["Its alright","Its OK, never mind",]
],
[
  r"hi|hey|hello",
  ["Hello", "Hey there","Hi!"]
],
[
  r"(.*) age?",
  ["I'm a robot, so, I don't know.",]
],
[
  r"what (.*) want",
  ["Make me an offer I can't refuse",]
],
[
  r"(.*) created",
  ["Antonio Galiza created me!","top secret",]
],
[
  r"(.*) (location|city)",
  ['Tokyo, Japan',]
],
[
  r"how is weather in (.*)",
  ["Weather in %1 is awesome like always","Too hot here in %1","Too cold here in %1","I don't know where 1% is."]
],
[
  r"i work in (.*)",
  ["%1 is an Amazing company", "I have heard about it", "Cool!",]
],
[
  r"(.*)raining in (.*)",
  ["No rain since last week here in %2","Damn its raining too much here in %2"]
],
[
  r"(.*) (sports|game)",
  ["I was a robot soccer player in robot school.",]
],
[
  r"who (.*) (moviestar|actor)",
  ["Brad Pitt"]
],
[
  r"what is your job",
  ["I carry plants and talk to people!","To make you and your plants happy!", "Top secret information", ""]
],
[
  r"do you know what (.*)",
  ["wikipedia:%1"]
],
[
  r"what is the meaning of(.*)",
  ["dictionary:%1"]
],
[
  r"what do you see(.*)",
  ["vision_check"]
],
[
  r"what can you see(.*)",
  ["vision_check"]
],
[
  r"what is in front of you(.*)",
  ["vision_check"]
],
[
  r"describe what you see(.*)",
  ["vision_check"]
],
[
  r"quit",
  ["Bye take care. See you soon","It was nice talking to you. See you soon :)"]
],
[
  r"{(.*)",
  ["not_proc"]
],
[
r"how is the soil",
  ["sensor:1"]
],
[
r"(.*)soil nitrogen(.*)",
  ["sensor:8"]
],
[
r"(.*)soil phosphorus(.*)",
  ["sensor:9"]
],
[
r"(.*)soil potassium(.*)",
  ["sensor:10"]
],
[
r"(.*)soil moisture(.*)",
  ["sensor:3"]
],
[
r"(.*)soil (salinity|ec)(.*)",
  ["sensor:6"]
],
[
r"(.*)soil (acidity|ph)(.*)",
  ["sensor:7"]
],
[
r"(.*)temperature(.*)",
  ["sensor:4"]
],
[
r"what is (.*)",
  ["wikipedia:%1"]
],
[
r"what was (.*)",
  ["wikipedia:%1"]
],
[
r"who is (.*)",
  ["wikipedia:%1"]
],
[
r"who was (.*)",
  ["wikipedia:%1"]
],
]

def chatter(phrase,pairs=default_pairs, reflections=reflections):
  chat = Chat(pairs, reflections)
  return chat.respond(phrase)

def sentiment_analysis(phrase):
  """Model from @article{vamossy2023emtract,
  title={EmTract: Extracting Emotions from Social Media},
  author={Vamossy, Domonkos F and Skog, Rolf},
  journal={Available at SSRN 3975884},
  year={2023}
  }
  """
  # sentiment_classifier = pipeline("text-classification",model='vamossyd/emtract-distilbert-base-uncased-emotion', return_all_scores=True) # uncomment if you need to load the model locally in order to save memory
  prediction = sentiment_classifier(phrase)
  # this mapping is done to adapt to the 5-emotion model adopted by the HVC-P2 camera emotion estimation
  emotion_map = {"neutral":"neutral","happy":"happy","sad":"sad","anger":"anger","disgust":"anger","surprise":"surprise","fear":"surprise",}
  prediction = emotion_map.get(prediction)
  if not prediction:
    prediction = "neutral"

  return emotion_map[prediction["label"].lower()]
