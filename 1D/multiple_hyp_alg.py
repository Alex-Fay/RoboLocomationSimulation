# @Alex Fay 7/29/2020
#Algorithm from Paper: https://www-users.cs.umn.edu/~stergios/papers/icra00_hypotheses.pdf
import numpy as np
import math
import cmath
import random 
from scipy import linalg

#===== step 1 =====
landmark_pos = np.array([0,0])

def generateNewBot(num_landmarks, robot_loc, velocity):
  #set up loc and time vars
  num_landmarks = 1 if num_landmarks < 1 else num_landmarks
  velocity_robot = self.velocity
  if(robot_loc == None):
    random_robot_loc = random.randint(-10, 10) #x cordinate
  else: 
    random_robot_loc = self.robot_loc
  first_landmark_loc = [random_robot_loc + random.randint(0, 15),0]
  time_of_first_landmark = 1 #TODO: make updateable

def step_init(num_landmarks):
  #Prob of landmark
  num_landmarks = 2 #temp
  x_pos = np.array([[1,0], [2,3]]) #temp
  Ka_matrix = np.array([[1,2], [2,3]]) #temp, must be square

  #add Ka functionality 
  for i in range(num_landmarks):
    if(i==0): spec_land_pos = first_landmark_loc + random.randint(0, 10)
    spec_land_pos += random.randint(0, 5)
    newrow = [spec_land_pos, 0]
    landmark_pos = np.vstack([newrow])
    print(landmark_pos)

  xa_pos = landmark_pos #array of mapped landmark pos
  covariance_sqrt = cmath.sqrt(np.linalg.det(Ka_matrix))
  pi_landmarks = ((2*math.pi)**(num_landmarks/2))
  exp_distance_scale = linalg.expm(-.5 * np.transpose(np.subtract(x_pos, xa_pos)) * np.linalg.inv(Ka_matrix) * np.subtract(x_pos, xa_pos)) #e^matrix

  denom = pi_landmarks * covariance_sqrt * exp_distance_scale
  print(denom)
  func_x_given_z = 1/denom
