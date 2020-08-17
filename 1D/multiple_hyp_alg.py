# @Alex Fay 7/29/2020
#Algorithm from Paper: https://www-users.cs.umn.edu/~stergios/papers/icra00_hypotheses.pdf
import numpy as np
import math
import cmath
import random 
from scipy import linalg
#import kalman_plot

#====== Helper Functions ======
landmark_pos = np.array([[0],[0],[5]])
area = 25 # surface area
first_landmark_loc = np.array([[3],[0],[3]])
x_pos = np.array([[1,5], [0,0], [5,30]]) #temp [x1, x2][y1, y2][z]
xa_pos = np.array([[7], [0], [-15]]) #[x1][y][z]
Ka_values = dict()
fxz_values = []

def Ka(x_pos, xa_pos): #Ka = E[(x-xa)(x-xa)^T]
  for i in range(0, x_pos.shape[1]): #each possible pos get seperate matrix
    exp_x = math.pow(x_pos[0][i] - xa_pos[0], 2)
    exp_y = math.pow(x_pos[1][i] - xa_pos[1], 2)
    exp_phi = math.pow(x_pos[2][i] - xa_pos[1],2)
    Ka_matrix = np.array([[exp_x, 0, 0], [0 ,exp_y, 0], [0,0, exp_phi]])
    Ka_values[i] = Ka_matrix
  return Ka_values #dict stores each pos as matrix

def sub_singular_matrix(x_pos, xa_pos): #duplicates col needed to subtract matrix
  new_xa = xa_pos 
  for i in range(1, x_pos.shape[1]):
    new_xa = np.append(new_xa, xa_pos, axis = -1)
  return new_xa

def fxz(num_landmarks, x_pos, xa_pos):
  Ka_ret = Ka(x_pos, xa_pos)
  for i in range(0, len(Ka_ret)):
    covariance_sqrt = cmath.sqrt(np.linalg.det(Ka_ret.get(i))) #current error since Ka is not square
    pi_landmarks = ((2*math.pi)**(num_landmarks/2))
    new_xa = sub_singular_matrix(x_pos, xa_pos)
    Ka_inv = np.linalg.inv(Ka_ret.get(i)) # 3 by 3 matrix
    displacement_transpose = np.transpose(np.subtract(x_pos, new_xa))
    displacement_diff = np.subtract(x_pos, new_xa)
    exp_result = displacement_transpose.dot(Ka_inv)
    exp_distance_scale = exp_result.dot(displacement_diff) * -.5
    denom = pi_landmarks * covariance_sqrt * exp_distance_scale
    fxz_result = 1/denom
    fxz_values.append(fxz_result)
  return fxz_values

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
  x_pos = np.array([[1,1], [2,1], [5,10]]) #[x1, x2...][y][z]
  landmark_pos = np.empty([3,1])

  #add random landmark positions
  xa_pos = np.random.rand(3, num_landmarks) * 10
  fxz_prob = fxz(2,x_pos, xa_pos)

  #probability of being landmark
  P_landmark = 1/(2 * math.pi * area) #changeable to matrix
  prob_of_landmark = []
  for i in range(0, len(fxz_prob)):
    prob_of_landmark.append(np.sum(P_landmark * fxz_prob[i]))
  return print(prob_of_landmark)
#====== Step k-1 ======
def step_k1(xa_pos):
  kalman_pos_arr, kalman_vel_arr = kalman_plot.kfilter(0.0,1.0, .9) #start pos, vel, acc
  displacement = kalman_pos_arr[10] - kalman_pos_arr[0] #change to time of call - time of last call
  print("before", xa_pos)
  for i in xa_pos:
    xa_pos[i] + displacement
  print("after", xa_pos)
  
#Main
step_init(1, first_landmark_loc)
