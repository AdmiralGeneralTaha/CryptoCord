from flask import Flask
from threading import Thread
from time import time, sleep

app=Flask("")

@app.route("/")
def home():
    return "hello im awake"

def run():
  app.run(host="0.0.0.0",port=8080)

def keep_alive():
  t=Thread(target=run)
  t.start()