#Kalman Filter Basics: https://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/#mjx-eqn-kalpredictfull
#Edits by Alex Fay 7/21/2020, Original KF: https://github.com/cbecker/kalman_python_cpp/blob/master/python/kf.py
import numpy as np

# offsets of each variable in the state vector
X0 = 0
V0 = 1
NUMVARS = V0 + 1

class KF:
    def __init__(self, initial_x: float, 
                       initial_v: float,
                       accel_variance: float) -> None:

        #initialize Bell Curve start Positions
        self._x = np.zeros(NUMVARS)
        self._x[X0] = initial_x
        self._x[V0] = initial_v
        self._accel_variance = accel_variance
        self._P = np.eye(NUMVARS) #init P = I

    def predict(self, dt: float) -> None:
        # (1) x = F x , F is a change in x matrix
        # (2) P = F P Ft + G Gt a , P is cerntainty matrix
        
        #Define F matrix [delta X]
        F = np.eye(NUMVARS) #num or rows and cols
        F[X0, V0] = dt
        new_x = F.dot(self._x)

        #Define G matrix [uncertantiy]
        G = np.zeros((2, 1))
        G[X0] = 0.5 * dt**2 #dependent on change in a (1/2a*t^2)
        G[V0] = dt #dependent on t
        new_P = F.dot(self._P).dot(F.T) + G.dot(G.T) * self._accel_variance

        #init uncertaty and position matrix
        self._P = new_P
        self._x = new_x

    def update(self, meas_value: float, meas_variance: float):

        #init matrix H for S eqn
        H = np.zeros((1, NUMVARS)) 
        H[0, X0] = 1

        #init all matricies
        z = np.array([meas_value]) #mean vector
        R = np.array([meas_variance]) #mean variance
        y = z - H.dot(self._x)  # y = z - H x #innovation - difference between measurement & observed
        S = H.dot(self._P).dot(H.T) + R  # S = H P Ht + R #innovation covariance
        K = self._P.dot(H.T).dot(np.linalg.inv(S)) # K = P Ht S^-1 # common gain
        
        #Update pos and uncertantity
        new_x = self._x + K.dot(y)  # x = x + K y
        new_P = (np.eye(2) - K.dot(H)).dot(self._P)  # P = (I - K H) * P
        self._P = new_P
        self._x = new_x

    @property
    def cov(self) -> np.array:
        return self._P

    @property
    def mean(self) -> np.array:
        return self._x

    @property
    def pos(self) -> float:
        return self._x[X0]

    @property
    def vel(self) -> float:
        return self._x[V0]
