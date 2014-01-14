##placeholder
import SimpleCV


class CameraModule:
	def __init__(self, haar_path):
		self.cam = SimpleCV.Camera()

		self.haar_path = haar_path


	def start_loop(self):
		#loop until face recognized
		return face_found