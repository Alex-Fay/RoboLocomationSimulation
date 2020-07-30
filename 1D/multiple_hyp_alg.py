# @Alex Fay 7/29/2020
#Algorithm from Paper: https://www-users.cs.umn.edu/~stergios/papers/icra00_hypotheses.pdf
import numpy as np
import math
import cmath
import random 
from scipy import linalg

#======Helper Functions=====
landmark_pos = np.array([0,0])

def Ka(x_pos, xa_pos): #Ka = E[(x-xa)(x-xa)^T]
  pos_difference = np.subtract(x_pos, xa_pos)
  expector = pos_difference.dot(np.transpose(pos_difference))
  expectation_matrix = expector.mean(1)
  return print(expectation_matrix)

def fxz(num_landmarks, x_pos, xa_pos):
  Ka_matrix = Ka(x_pos, xa_pos)
  covariance_sqrt = cmath.sqrt(np.linalg.det(Ka_matrix))
  pi_landmarks = ((2*math.pi)**(num_landmarks/2))
  exp_distance_scale = linalg.expm(-.5 * np.transpose(np.subtract(x_pos, xa_pos)) * np.linalg.inv(Ka_matrix) * np.subtract(x_pos, xa_pos)) #e^matrix
  denom = pi_landmarks * covariance_sqrt * exp_distance_scale
  return 1/denom

#==== init=====
def generateNewBot(num_landmarks, robot_loc, velocity):
  #set up loc and time vars
  num_landmarks = 1 if num_landmarks < 1 else num_landmarks
  velocity_robot = velocity
  if(robot_loc == None):
    random_robot_loc = random.randint(-10, 10) #x cordinate
  else: 
    random_robot_loc = robot_loc
  first_landmark_loc = [random_robot_loc + random.randint(0, 15),0]
  time_of_first_landmark = 1 #TODO: make updateable
  return first_landmark_loc

#===Step 1====
def step_init(num_landmarks, first_landmark_loc):
  #Prob of landmark
  num_landmarks = 2 #temp
  x_pos = np.array([[6,1], [-4,1]]) #temp
  Ka_matrix = np.array([[1,8], [2,3]]) #temp, must be square

  #add random landmark positions
  for i in range(num_landmarks):
    if(i==0): spec_land_pos = first_landmark_loc[0] + random.randint(0, 10) #x cord
    spec_land_pos += random.randint(0, 5)
    newrow = [spec_land_pos, 0]
    landmark_pos = np.vstack([newrow])
  xa_pos = landmark_pos #array of mapped landmark pos
  fxz_prob = fxz(2,x_pos, xa_pos)
  print("Ka", Ka(x_pos, xa_pos))

  #probability of being landmark
  P_landmark = 1/num_landmarks #changeable to matrix
  return numpy.sum(P_landmark * fxz_prob)

#step init
landmark = generateNewBot(2,0,1)
step_init(2, landmark)
