# @Alex Fay 7/29/2020
#Algorithm from Paper: https://www-users.cs.umn.edu/~stergios/papers/icra00_hypotheses.pdf
import numpy as np
import math
import cmath
import random 
from scipy import linalg
import kalman_plot

#====== Helper Functions ======
landmark_pos = np.array([[0],[0],[0]])
area = 25 # surface area
first_landmark_loc = np.array([[3],[0],[0]])
x_pos = np.array([[1,5], [0,0], [0,0]]) #temp [x1][y][z]
xa_pos = np.array([[7,4], [0,0], [0,0]]) #[x1][y][z]

def Ka(x_pos, xa_pos): #Ka = E[(x-xa)(x-xa)^T]
  pos_difference = np.subtract(x_pos, xa_pos)
  expector = pos_difference.dot(np.transpose(pos_difference)) #must be square after transpose 
  print(expector)
  expectation_matrix = expector.mean(1)
  return print(expectation_matrix) #ask what output should be in order to take the determinent

def fxz(num_landmarks, x_pos, xa_pos):
  Ka_matrix = Ka(x_pos, xa_pos)
  covariance_sqrt = cmath.sqrt(np.linalg.det(Ka_matrix)) #current error since Ka is not square
  pi_landmarks = ((2*math.pi)**(num_landmarks/2))
  exp_distance_scale = linalg.expm(-.5 * np.transpose(np.subtract(x_pos, xa_pos)) * np.linalg.inv(Ka_matrix) * np.subtract(x_pos, xa_pos)) #e^matrix
  denom = pi_landmarks * covariance_sqrt * exp_distance_scale
  return 1/denom

#====== init: Pre-Step 1 ======
def generateNewBot(num_landmarks, robot_loc, velocity):
  #set up loc and time vars
  num_landmarks = 1 if num_landmarks < 1 else num_landmarks
  velocity_robot = velocity
  if(robot_loc.any() == None):
    random_robot_loc = random.randint(-10, 10) #x cordinate
  else: 
    random_robot_loc = robot_loc
  first_landmark_loc = [random_robot_loc + random.randint(0, 15)]
  time_of_first_landmark = 1 #TODO: make updateable
  return first_landmark_loc

#====== Step 1 ======
def step_init(num_landmarks, first_landmark_loc):
  #Prob of landmark
  num_landmarks = 2 #temp
  x_pos = np.array([[1,1], [0,0], [0,0]]) #[x1][y][z]
  landmark_pos = np.empty([3,2])

  #add random landmark positions
  for i in range(0, num_landmarks):
    if(i==0): spec_land_pos = first_landmark_loc[0] + random.randint(0, 10) #x cord
    else: spec_land_pos += random.randint(0, 5)
    new_column = np.array([[spec_land_pos], [0], [0]])
    np.append(landmark_pos, new_column, axis=1)
  xa_pos = landmark_pos #array of mapped landmark pos
  print(xa_pos)
  print("fex", fxz_prob = fxz(2,x_pos, xa_pos))

  #probability of being landmark
  P_landmark = 1/(2 * math.pi * area) #changeable to matrix
  return print(numpy.sum(P_landmark * fxz_prob))

#====== Step k-1 ======
def step_k1(xa_pos):
  kalman_pos_arr, kalman_vel_arr = kalman_plot.kfilter(0.0,1.0, .9) #start pos, vel, acc
  displacement = kalman_pos_arr[10] - kalman_pos_arr[0] #change to time of call - time of last call
  print("before", xa_pos)
  for i in xa_pos:
    xa_pos[i] + displacement
  print("after", xa_pos)
  
#step init
landmark = generateNewBot(2,0,1)
step_init(2, landmark)
