from flask import Flask, render_template, Response, request, redirect
app = Flask(__name__)
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
#   A |----| B
#      |  |
#      |  |
#   C |----| D
A_in1 = 22# go forward when high
A_in2 = 23
B_in1 = 17
B_in2 = 18
GPIO.setup(A_in1, GPIO.OUT)
GPIO.setup(A_in2, GPIO.OUT)
GPIO.setup(B_in1, GPIO.OUT)
GPIO.setup(B_in2, GPIO.OUT)

@app.route('/')
def json():
  return render_template('index.html')

#background process happening without any refreshing
@app.route('/background_forward')
def background_forward():
  print ("Forward")
  GPIO.output(A_in1, True)
  GPIO.output(A_in2, False)
  GPIO.output(B_in1, True)
  GPIO.output(B_in2, False)
  time.sleep(1)
  GPIO.output(A_in1, False)
  GPIO.output(A_in2, False)
  GPIO.output(B_in1, False)
  GPIO.output(B_in2, False)
  return ("nothing")
  
@app.route('/background_backward')
def background_backward():
  print ("Backward")
  GPIO.output(A_in1, False)
  GPIO.output(A_in2, True)
  GPIO.output(B_in1, False)
  GPIO.output(B_in2, True)
  time.sleep(1)
  GPIO.output(A_in1, False)
  GPIO.output(A_in2, False)
  GPIO.output(B_in1, False)
  GPIO.output(B_in2, False)
  return ("nothing")
  
@app.route('/background_right')
def background_right():
  print ("Right")
  GPIO.output(A_in1, True)
  GPIO.output(A_in2, False)
  GPIO.output(B_in1, False)
  GPIO.output(B_in2, False)
  time.sleep(0.3)
  GPIO.output(A_in1, False)
  GPIO.output(A_in2, False)
  GPIO.output(B_in1, False)
  GPIO.output(B_in2, False)
  return ("nothing")
  
@app.route('/background_left')
def background_left():
  print ("Left")
  GPIO.output(A_in1, False)
  GPIO.output(A_in2, False)
  GPIO.output(B_in1, True)
  GPIO.output(B_in2, False)
  time.sleep(0.3)
  GPIO.output(A_in1, False)
  GPIO.output(A_in2, False)
  GPIO.output(B_in1, False)
  GPIO.output(B_in2, False)
  return ("nothing")

