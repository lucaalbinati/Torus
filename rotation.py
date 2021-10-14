import time
import math
import numpy as np

class Rotation:

	def __init__(self, scene, rotation_matrix_func, start_theta, end_theta, FPS=5, animation_duration_in_sec=2):
		self.scene = scene
		self.rotation_matrix_func = rotation_matrix_func
		self.start_theta = start_theta
		self.FPS = FPS

		self.nb_frames = self.FPS * animation_duration_in_sec
		self.theta_incr = (end_theta - start_theta) / self.nb_frames

	def animate(self):
		excessive_computation_count = 0
		excessive_computations = []

		for i in range(0, self.nb_frames + 1):
			before_comp_time = time.time()

			if i > 0:
				self.scene.obj.rotate(self.rotation_matrix_func, self.theta_incr)
			self.scene.show()

			after_comp_time = time.time()

			comp_time = after_comp_time - before_comp_time
			sleep_time = (1 / self.FPS) - comp_time

			if sleep_time < 0:
				excessive_computation_count += 1
				excessive_computations.append(comp_time)
				if excessive_computation_count >= 3:
					print("WARNING: computation regularly takes more time than {}s (1/FPS) (takes an average of {:.3f}s)".format(1 / self.FPS, np.mean(excessive_computations)))

			time.sleep(max(sleep_time, 0))

	@staticmethod
	def full_around_x(scene):
		return Rotation(scene, Rotation.rotation_x_matrix, start_theta=0, end_theta=math.pi)

	@staticmethod
	def full_around_y(scene):
		return Rotation(scene, Rotation.rotation_y_matrix, start_theta=0, end_theta=math.pi)

	@staticmethod
	def full_around_z(scene):
		return Rotation(scene, Rotation.rotation_z_matrix, start_theta=0, end_theta=math.pi)

	@staticmethod
	def cool_around_yz(scene):
		def rotation_func(theta):
			rot_y = Rotation.rotation_y_matrix(theta)
			rot_z = Rotation.rotation_z_matrix(theta*2/3)
			return np.matmul(rot_y, rot_z)

		return Rotation(scene, rotation_func, start_theta=0, end_theta=4*math.pi, animation_duration_in_sec=10)

	@staticmethod
	def rotation_x_matrix(theta):
		return np.array([
				[1, 0, 0],
				[0, math.cos(theta), -math.sin(theta)],
				[0, math.sin(theta), math.cos(theta)]
			])

	@staticmethod
	def rotation_y_matrix(theta):
		return np.array([
				[math.cos(theta), 0, math.sin(theta)],
				[0, 1, 0],
				[-math.sin(theta), 0, math.cos(theta)]
			])

	@staticmethod
	def rotation_z_matrix(theta):
		return np.array([
				[math.cos(theta), -math.sin(theta), 0],
				[math.sin(theta), math.cos(theta), 0],
				[0, 0, 1]
			])

