import os
import time
import SimpleCV
from ConfigParser import ConfigParser


class Client:
    def __init__(self):
        self.get_cfg()

        self.cam = SimpleCV.Camera()

    def get_cfg(self):
        if os.path.exists("client.cfg"):
            cfg = ConfigParser()
            cfg.read("client.cfg")
            self.host = cfg.get("network", "host")
            self.haar_path = cfg.get("face_settings", "haar_path")

    def check_dir(self):
        if os.path.exists("data"):
            data_con = os.listdir("data")
            if "usr" not in data_con:
                os.makedir("data/usr")
        else:
            os.makedirs("data/usr")
            print("data folders created...")


    def start(self):
        while True:
            face = face_detected()
            if face:
                result = self.check_face(face)
                if result:
                    self.send_auth(result)
    
    def face_detected(self):
        img = self.cam.getImage()
        faces = img.findHaarFeatures(self.haar_path)
        if faces:
            faces.draw()
            face = faces[-1]
            return face
        else:
            return None

    def check_face(self, face):
        usr_list = os.listdir("data/usr")
        result_list = []
        for usr in os.listdir("data/usr"):


    def send_auth(self, name):
        pass