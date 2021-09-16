from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from apscheduler.schedulers.background import BackgroundScheduler
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from tflite_runtime.interpreter import load_delegate
from tflite_runtime.interpreter import Interpreter
from flask_sqlalchemy  import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from collections import deque
import numpy as np
import subprocess
import threading
import argparse
import datetime
import requests
import pygame
import utils
import json
import time
import cv2
import os 
import io
import re



from gpiozero import Servo
import math
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()
servo = Servo(18, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
position = 0
servo.value = math.sin(math.radians(position))

time.sleep(.5)

servo_b = Servo(12, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
position_b = 0
servo_b.value = math.sin(math.radians(position_b))


app = Flask(__name__, static_folder='static')
port=8000


# output link for webapp
print('\n\n🤖 Pi-Vision 🤖\n')
print('Log in to piEye. Go to:')
print('🏠 http://0.0.0.0:'+ str(port) +'/ if accessing from Raspberry Pi.')
rpi_ip = subprocess.getoutput('hostname -I').split()[0]
print('🏠 http://' + rpi_ip + ':' + str(port) +'/ if accessing from local network.')
# get the external ip of the raspberry pi
public_ip = requests.get('https://api.ipify.org').text
print('🌎 http://' + public_ip + ':'+ str(port) +'/ if accessing from remote network (port forwarding required).')
print('')

# - - - - - - - - - - - - - - LOAD SETTINGS START - - - - - - - - - - - - - - - - - - - - - - - - - -
with open('settings.json') as settings:
    settings = json.load(settings)

keys = list(settings.keys())
print(keys)

print('SYSTEM SETTINGS:')
for key in keys:
    print(key, ':', settings[key])
print('')

# - - - - - - - - - - - - - - LOAD SETTINGS END - - - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - LOG IN MANAGEMENT START - - - - - - - - - - - - - - - - - - - -

SQLALCHEMY_TRACK_MODIFICATIONS = True
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

# - - - - - - - - - - - - - - - LOG IN MANAGEMENT END - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - SCHEDULE CHRON JOBS START - - - - - - - - - - - - - - - - - - - -

# sched = BackgroundScheduler(daemon=True)
# sched.add_job(play_sound,'interval',minutes=60)
# sched.start()

# - - - - - - - - - - - - - - - SCHEDULE CHRON JOBS END - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - CAMERA CONFIGURATIONS START - - - - - - - - - - - - - - - 

# get available cameras 
print('Available Cameras:')
available_cameras = utils.get_cameras()
print(available_cameras)
cap = cv2.VideoCapture(available_cameras[0])
cap.set(cv2.CAP_PROP_EXPOSURE,-4)

# show current camera settings
# print('\nCAMERA SETTINGS')
# print('Contrast:', cap.get(cv2.CAP_PROP_CONTRAST))
# print('Exposure:', cap.get(cv2.CAP_PROP_EXPOSURE))
# print('Brightness:', cap.get(cv2.CAP_PROP_BRIGHTNESS))
# print('Frame Width:', cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# print('Frame Height:', cap.get(cv2.CAP_PROP_FRAME_HEIGHT), '\n')

# video contrast controls
@app.route('/contrast-up')
def contrast_up():
    global cap
    contrast = cap.get(cv2.CAP_PROP_CONTRAST) + 5.0
    if contrast > 95.0:
        contrast = 5.0
    cap.set(cv2.CAP_PROP_CONTRAST, contrast)
    print('Contrast:', cap.get(cv2.CAP_PROP_CONTRAST))
    return ''
@app.route('/contrast-down')
def contrast_down():
    global cap
    contrast = cap.get(cv2.CAP_PROP_CONTRAST) - 5.0
    cap.set(cv2.CAP_PROP_CONTRAST, contrast)
    print('Contrast:', cap.get(cv2.CAP_PROP_CONTRAST))
    return ''

# video exposure controls
@app.route('/exposure-up')
def exposure_up():
    global cap
    # get the current exposure level
    exposure = cap.get(cv2.CAP_PROP_EXPOSURE)
    print(type(exposure))
    print(exposure)
    if 1.0 <= exposure < 15.0:
        increment = 1.0
    elif 15.0 <= exposure <= 200.0:
        increment = 5.0
    else:
        increment = 100.0
    print(increment)
    exposure += increment
    if exposure > 5000.0:
        exposure = 1.0
    # set new exposure level
    cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
    print('Exposure:', cap.get(cv2.CAP_PROP_EXPOSURE))
    return ''
@app.route('/exposure-down')
def exposure_down():
    global cap
    # get the current exposure level
    exposure = cap.get(cv2.CAP_PROP_EXPOSURE)
    if 1.0 <= exposure < 15.0:
        increment = 1.0
    elif 15.0 <= exposure <= 200.0:
        increment = 5.0
    else:
        increment = 100.0
    exposure -= increment
    if exposure <= 1.0:
        exposure = 1.0
    cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
    print('Exposure:', cap.get(cv2.CAP_PROP_EXPOSURE))
    return ''

# video brightness controls
@app.route('/brightness-up')
def brightness_up():
    global cap
    brightness = cap.get(cv2.CAP_PROP_BRIGHTNESS) + 5.0
    cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
    print('Brightness:', cap.get(cv2.CAP_PROP_BRIGHTNESS))
    return ''
@app.route('/brightness-down')
def brightness_down():
    global cap
    brightness = cap.get(cv2.CAP_PROP_BRIGHTNESS) - 5.0
    cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
    print('Brightness:', cap.get(cv2.CAP_PROP_BRIGHTNESS))
    return ''

# video saturation controls
@app.route('/saturation-up')
def saturation_up():
    global cap
    saturation = cap.get(cv2.CAP_PROP_SATURATION) + 5.0
    cap.set(cv2.CAP_PROP_SATURATION, saturation)
    print('Saturation:', cap.get(cv2.CAP_PROP_SATURATION))
    return ''
@app.route('/saturation-down')
def saturation_down():
    global cap
    saturation = cap.get(cv2.CAP_PROP_SATURATION) - 5.0
    cap.set(cv2.CAP_PROP_SATURATION, saturation)
    print('Saturation:', cap.get(cv2.CAP_PROP_SATURATION))
    return ''

pause = .06
pan = False
@app.route('/pan-left') 
def pan_left():
    global pan
    global position

    pan = True
    while pan:
        if position < 89:
            position += 1
            servo.value = math.sin(math.radians(position))
            sleep(pause)
        else:
            pass
    return ''

@app.route('/pan-right') 
def pan_right():
    global pan
    global position

    pan = True
    while pan:
        if position > -89:
            position -= 1
            servo.value = math.sin(math.radians(position))
            sleep(pause)
        else:
            pass
    return ''

@app.route('/tilt-up') 
def tilt_up():
    global pan
    global position_b

    pan = True
    while pan:
        if position_b > -89:
            position_b -= 1
            servo_b.value = math.sin(math.radians(position_b))
            sleep(pause)
        else:
            pass
    return ''

@app.route('/tilt-down') 
def tilt_down():
    global pan
    global position_b

    pan = True
    while pan:
        if position_b < 89:
            position_b += 1
            servo_b.value = math.sin(math.radians(position_b))
            sleep(pause)
        else:
            pass
    return ''

@app.route('/stop-pan')
def stop_pan():
    global pan
    pan = False
    return ''

@app.route('/home')
def home_position():


    return ''
    


# video rotation control 
rotations = [None, cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_180, cv2.ROTATE_90_COUNTERCLOCKWISE]
rotation = rotations[0]
@app.route('/rotate')
def rotate():
    global rotation
    global rotations
    rotations = deque(rotations)
    rotations.rotate()
    rotations = list(rotations)
    rotation = rotations[0] 
    print(rotation)
    return ''


# video recording controls 
record = False
num_frames = 0
@app.route('/record')
def record_start():
    global num_frames
    global record
    print('\n🔴 Recording Activated ...\n')
    if record == False:
        record = True
    else:
        record = False
    return ''

# video recording controls continued
stop_record = False
@app.route('/stop-record')
def record_stop():
    global stop_record
    global record
    print('\n🏁 Recording Completed.\n')
    if stop_record == False:
        stop_record = True
        record = False
    return ''

# - - - - - - - - - - - - - - - CAMERA CONFIGURATIONS END - - - - - - - - - - - - - - - 


# - - - - - - - - - - - - - - OBJECT DETECTION FUNCTIONS START - - - - - - - - - - - - - - - - -

def load_labels(path):
  with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    labels = {}
    for row_number, content in enumerate(lines):
      pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
      if len(pair) == 2 and pair[0].strip().isdigit():
        labels[int(pair[0])] = pair[1].strip()
      else:
        labels[row_number] = pair[0].strip()
  return labels


def set_input_tensor(interpreter, image):
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image


def get_output_tensor(interpreter, index):
  output_details = interpreter.get_output_details()[index]
  tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
  return tensor


def detect_objects(interpreter, image, threshold):
  set_input_tensor(interpreter, image)
  interpreter.invoke()

  # Get all output details
  boxes = get_output_tensor(interpreter, 0)
  classes = get_output_tensor(interpreter, 1)
  scores = get_output_tensor(interpreter, 2)
  count = int(get_output_tensor(interpreter, 3))

  results = []
  for i in range(count):
    if scores[i] >= threshold:
      result = {
          'bounding_box': boxes[i],
          'class_id': int(classes[i]),
          'score': scores[i]
      }
      results.append(result)
  return results

def annotate_box(frame, class_id, box):
    width, height = frame.shape[0], frame.shape[1]
    start_point = (int(box[1]*height), int(box[2]*width))
    end_point = (int(box[3]*height), int(box[0]*width))
    color = (255, 0, 0)
    thickness = 2
    # draw rectangle 
    frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
    # add label
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale  = .5
    fontColor = (255,255,255)
    lineType = 2
    bottom_left = (25, 25)
    cv2.putText(frame, class_id, bottom_left , font, fontScale, fontColor, lineType)
    return frame

# toggle for enabling and disabling object detection
detect = settings['detect']
@app.route('/activate-status') 
def toggle_detection():
    global detect
    if detect == True:
        detect = False
        print('\nObject Detection Dectivated')
        utils.update_settings('detect', detect)
    else:
        detect = True
        print('\nObject Detection Activated')
        utils.update_settings('detect', detect)
    return ""

# load object detection models and labels
labels = load_labels('model/coco_labels.txt')
try:
    interpreter = Interpreter(model_path='model/edgetpu.tflite', experimental_delegates=[load_delegate('libedgetpu.so.1.0')])
    print('\nCoral USB Accelerator Detected.\nRunning model on edge TPU\nModel loaded.\n')
except:
    interpreter = Interpreter('model/detect.tflite')
    print('\nNo accelerator detected.\nModel loaded.\n')
interpreter.allocate_tensors()
_, input_height, input_width, _ = interpreter.get_input_details()[0]['shape']


# - - - - - - - - - - - - - - OBJECT DETECTION FUNCTIONS END - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - LIVE STREAM START - - - - - - - - - - - - - - - - - - - -
x = .5
# generate frame by frame from camera
def gen_frames():  
    global detect
    global record
    global stop_record
    global num_frames
    global camera_capture
    global x


    # settings for video recording 
    fourcc_type = 'avc1' #'mp4v'
    fourcc = cv2.VideoWriter_fourcc(*fourcc_type)

    fps = 20.0
    while True:
        w,h = int(cap.get(3)), int(cap.get(4))
        # read the camera frame
        success, frame = cap.read()  
        frame = cv2.flip(frame,-1)
        if stop_record:
            try:
                # stop the video recording 
                stream.release()
                stop_record = False
                num_frames = 0
            except:
                pass
        if success and record:
            if num_frames == 0:
                # create a new video stream file
                video = utils.name_mp4()
                stream = cv2.VideoWriter(video, fourcc, fps, (w,h))
                num_frames += 1
            stream.write(frame)
        #frame = cv2.resize(frame, (600,600), interpolation = cv2.INTER_AREA)
        if success:
            if detect == True:
                # resize frame 300x300 for model input 
                dim = (input_width, input_height)
                model_input = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
                # detect image for objects 
                confidence_threshold = 0.45
                model_output = detect_objects(interpreter, model_input, confidence_threshold)
                # add labels for each object 
                x_list = []
                y_list = []
                for result in model_output:
                    class_id = labels[result['class_id']]
                    box = result['bounding_box']
                    detect_list = ['person']#,'truck', 'car']#,  'motorcycle', 'car', 'bird', 'dog']
                    if class_id in detect_list:
                        #print('Object Detected')
                        # x = (box[3] + box[1])/2
                        x_list.extend([box[3],box[1]])

                        #y = (box[0] + box[2])/2
                        y_list.extend([box[0],box[2]])

                        frame = annotate_box(frame=frame, class_id=class_id, box=box)

                if x_list:
                    x = (min(x_list) + max(x_list))/2
                    y = (min(y_list) + max(y_list))/2
                    width, height = frame.shape[0], frame.shape[1]
                    frame = cv2.circle(frame, (int(x*height),int(y*width)), radius=5, color=(255, 0, 0), thickness=-1)
                else:
                    x = .5
            
            # encode frame to jpg
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  

def tracker():
    global x
    global position
    while True:
        if x < .35 and position < 89:
            position += 1
            servo.value = math.sin(math.radians(position))
        if x > .65 and position > -89:
            position -= 1
            servo.value = math.sin(math.radians(position))
        #print(x)
        sleep(pause)

track=threading.Thread(target=tracker)
track.start()

# video streaming route. Put this in the src attribute of an img tag
@app.route('/video_feed')
@login_required
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# - - - - - - - - - - - - - - LIVE STREAM END - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - APP PAGES START - - - - - - - - - - - - - - - - -

# user registration page
# disabled sign-up so not everyone can sign up and use the robot
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         hashed_password = generate_password_hash(form.password.data, method='sha256')
#         new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         return '<h1>New user has been created!</h1>'
#         #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
#     return render_template('signup.html', form=form)


# login page 
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

# log out function for users
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# home page 
@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    settings_file = open("settings.json", "r")
    settings = json.load(settings_file)
    settings_file.close()
    return render_template('index.html', settings=settings, cams=available_cameras)

# recordings gallery
@app.route('/video')
@login_required
def video_page():
    video_files = ['recordings/' + v for v in os.listdir('static/recordings/')]
    print(video_files)
    return render_template('video.html', videos=video_files)

# - - - - - - - - - - - APP PAGES END - - - - - - - - - - - - - - - - -


# - - - - - - - - - - RETA APP START - - - - - - - - - - - - - - - -
if __name__ == '__main__':
    # start the app
    app.run(host='0.0.0.0', port=port)

