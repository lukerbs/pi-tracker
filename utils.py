import cv2
import json
import requests
import datetime

# returns list of available cameras by index
def get_cameras():
    available_cams = []
    for camera_idx in range(10):
        cap = cv2.VideoCapture(camera_idx)
        if cap.isOpened():
            available_cams.append(camera_idx)
            cap.release()
        else:
            # suppress warnings from cv2
            print ('\033[A' + ' '*158 +  '\033[A')
    return available_cams

# play sound
def play_sound():
    sounds = os.listdir('sounds/')
    selection= random.randint(0, len(sounds)-1)
    sound = 'sounds/' + sounds[selection]
    pygame.mixer.init()
    pygame.mixer.music.load(sound)
    print('\nPlaying sound:', sound, '\n')
    pygame.mixer.music.play()

def name_mp4():
    now = datetime.datetime.now()
    mp4_file = now.strftime("%m-%d-%Y_%H:%M")
    path = 'static/recordings/'
    mp4_file = path + mp4_file + '.mp4'
    return mp4_file

def update_settings(key, value):
    print('Auto saving system settings ...\n')
    settings_file = open("settings.json", "r")
    updated_settings = json.load(settings_file)
    updated_settings[key] = value
    settings_file.close()

    settings_file = open("settings.json", "w")
    json.dump(updated_settings, settings_file)
    settings_file.close()
    return

def send_message(reciever, message):
	print('\nSending Alert\n')
	return requests.post(
		"https://api.mailgun.net/v3/mg.lukekerbs.net/messages",
		auth=("api", "key-bbad6aacdfa986754883861a281e45e0"),
		data= {
        	"from": "alert@pieye.com",
            "to": [reciever],
            "text": message
        })