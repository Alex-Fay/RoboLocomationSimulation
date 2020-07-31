#@Alex Fay 7/21/2020
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

# ====== Plot Data =======
def generate_data(nbr_iterations, nbr_elements):
    #init dot start positions and speed
    dimensions = (3,1)
    center = [0,0,0]
    gaussian_std = [1,1,1]
    start_positions = np.array([center, center])
    start_speed = np.array([[0, 2, 0], [ 0,2,0]]) #v0 vectors of xyz 

    # Computing trajectory
    data = [start_positions]
    for iteration in range(nbr_iterations):
        previous_positions = data[-1]
        new_positions = previous_positions + start_speed
        data.append(new_positions)
    return data

# === Animation ======
def animate_scatters(iteration, data, scatters):
    for i in range(data[0].shape[0]):
        scatters[i]._offsets3d = (data[iteration][i,0:1], data[iteration][i,1:2], data[iteration][i,2:])
    return scatters

def main(data, save=False):
    # -- Plot Init --
    fig = plt.figure()
    ax = p3.Axes3D(fig)
    scatters = [ ax.scatter(data[0][i,0:1], data[0][i,1:2], data[0][i,2:]) for i in range(data[0].shape[0]) ]
    iterations = len(data) # Number of iterations

    ax.set_xlim3d([-50, 50]) #Xaxis
    ax.set_xlabel('X')
    ax.set_ylim3d([-50, 50]) #YAxis
    ax.set_ylabel('Y')
    ax.set_zlim3d([-50, 50]) #ZAxis
    ax.set_zlabel('Z')
    ax.set_title('3D Robo Locomation')

    # Provide starting angle for the view.
    ax.view_init(25, 10)
    ani = animation.FuncAnimation(fig, animate_scatters, iterations, fargs=(data, scatters),
                                       interval=50, blit=False, repeat=True)

    if save:
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=30, metadata=dict(artist='Me'), bitrate=1800, extra_args=['-vcodec', 'libx264'])
        ani.save('3d-scatted-animated.mp4', writer=writer)

    plt.show()


data = generate_data(100, 2)
main(data, save=True)
