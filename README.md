# Bayesian estimation and Kalman filtering: Mobile Robot Localization

Applying 3D locomotion to the infamous kid napped robot problem - a robot lands in an unknown area with unknown identifies and limited field of view. It needs to identify landmarks and figure out where it is with confidence. Here I map the confidence (error) with predicted location and actual location in 3 dimensions. We will be using a new algorithm from the paper attached below to minimize error over time.

This is a multi step process, the first step is to create a 1D error and scale up to 3D and add acceleration.

See https://www-users.cs.umn.edu/~stergios/papers/icra00_hypotheses.pdf for details
