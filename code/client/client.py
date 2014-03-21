import os
import time
import socket
import SimpleCV
from ConfigParser import ConfigParser


class Client:
    def __init__(self):
        self.get_cfg()

        self.cam = SimpleCV.Camera()

        self.alarm_state = self.get_status()

    ##CONFIG

    def get_cfg(self):
        if os.path.exists("client.cfg"):
            cfg = ConfigParser()
            cfg.read("client.cfg")
            self.host = cfg.get("network", "host")
            self.host_port = cfg.getint("network", "port")
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
        print("Starting loop...")
        while True:
            face = self.face_detected()
            print(face)
            time.sleep(2)
            if face:
                result = self.check_face(face)
                if result:
                    self.send_auth(result[0])
                    time.sleep(10)

    ##FACERECOG
    
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
        print(usr_list)
        for usr in usr_list:
            usr_img = SimpleCV.Image("data/usr/"+usr)
            match = usr_img.findKeypointMatch(face.crop())
            if match:
                result_list.append((usr[:-4], match))
        print(result_list)
        if len(result_list) == 1:
            return result_list[0]
        else:
            return False

    def create_usr(self, name):
        face = None
        while not face:
            face = self.face_detected()
        print(face)
        face.crop().save("data/usr/"+name+".jpg")


    ##NETWORK

    def send_auth(self, name):
        print("sending auth for "+name)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.host_port))
        s.sendall("request "+name+"\n")
        data = s.recv(1024)
        s.close()
        print(data)
        return data

    def get_status(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.host_port))
        s.sendall("state\n")
        data = s.recv(1024)
        s.close()
        return data

if __name__ == "__main__":
    c = Client()
    c.create_usr("harry")
    c.start()