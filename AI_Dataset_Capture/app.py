from flask import Flask, render_template, Response, redirect, send_file
from picamera2 import Picamera2
import io
import cv2
import threading
import serial
import time
import tempfile
import libcamera

app = Flask(__name__)

# Init port série
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

# Init Picamera2
picam2 = None
lock = threading.Lock() # Mutex pour la camera

# Envoi commande via série avec protocole START(0x02) ... STOP(0x03)
def send_command(cmd_char):
    message = bytearray([0x02]) + cmd_char.encode('ascii') + bytearray([0x03])
    ser.write(message)

# Générateur de frames MJPEG pour Flask
def gen_frames():
    global picam2
    # Init caméra
    while True:
        with lock:
            try :
                frame = picam2.capture_array()  # retourne un ndarray (BGR)
                # On encode en JPEG
                ret, jpeg = cv2.imencode('.jpg', frame)
                if not ret:
                    print("Impossible de capturer l'image")
                    continue
                frame_bytes = jpeg.tobytes()
                # Flux MJPEG multipart
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            except Exception as e :
                print("Erreur dans gen_frames: {e}")
                break

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/command/<cmd>', methods=['POST'])
def command(cmd):
    cmds_valides = ['F', 'B', 'L', 'R', 'S']
    if cmd.upper() in cmds_valides:
        send_command(cmd.upper())
        return "OK", 205
    else:
        return "Command invalide", 400

@app.route('/photo', methods=['POST'])
def photo() :
    global picam2
    with lock :
        try:
            # Encode en JPEG
            frame = picam2.capture_array()
            ret, jpeg = cv2.imencode('.jpg', frame)
            if not ret:
                return "Erreur de capture", 500

            # Écriture dans fichier temporaire pour envoi
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            temp_file.write(jpeg.tobytes())
            temp_file.flush()
            temp_file.close()

            return send_file(temp_file.name, mimetype='image/jpeg', as_attachment=True, download_name='photo.jpg')
        except Exception as e:
            print(f"Erreur lors de la capture de photo : {e}")
            return "Erreur interne", 500

if __name__ == '__main__':
    picam2 = Picamera2()
    picam2.configure(picam2.create_still_configuration(
        main={"size": (640, 480)},
        transform=libcamera.Transform(hflip=1, vflip=1)
    ))
    picam2.start()
    app.run(host='0.0.0.0', port=5000, debug=False)
