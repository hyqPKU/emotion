#coding=utf-8
from utils import *

def emotion_classifier(query):
    polar, confidence = call_TOP(query)
    return polar, confidence, ''

def call_TOP(query):
    return get_content(query)
