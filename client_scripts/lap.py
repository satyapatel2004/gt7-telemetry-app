import datetime 
import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from mpl_toolkits.mplot3d.art3d import Line3DCollection 
import os 

from PIL import Image 

class Lap:
    def __init__(self, lapno, rawlaptime, coordinates):
        self.lapno = lapno
        self.coordinates = coordinates
        self.images = []
        
        
        minutes = rawlaptime // 60000
        seconds = (rawlaptime % 60000) // 1000 
        mseconds = rawlaptime % 1000
        
        self.laptime = f"{minutes:02}:{seconds:02}:{mseconds:03}"
                    
    # __repr__ function for logging purposes 
    def __repr__(self):
        if not self.lapno == 0:

            return f"Lapno: {self.lapno}, Laptime: {self.laptime}, Coordinates: {self.coordinates}"
                 
        else:
            return "No Lap recorded:" 
        
    def generate_images(self, fig, plt, ax, base_filename):
        # Define angles to save the plot
        angles = [(30, 30), (0, 0), (90, 0), (0, 90), (45, 45)]
        file_paths = []

        # Loop through the angles, set the view, and save the plot
        for i, angle in enumerate(angles):
            ax.view_init(elev=angle[0], azim=angle[1])
            filename = f"{base_filename}_{i}.png"
            #plt.savefig(filename)
            #file_paths.append(os.path.abspath(filename))

        plt.close(fig)  # Close the figure to free memory

        # Return the file paths
        return file_paths
    
    def add_image(self):
        fig, plt, ax, basename = self.plot_lap(self.coordinates, f"Lap: {self.lapno}")
        image_paths = self.generate_images(fig, plt, ax, basename) 
        self.images = [Image.open(image_path) for image_path in image_paths] 
        
    def plot_lap(self, data, base_filename="lap_plot"):
        x, y, z, braking, throttle = zip(*data)

        # Convert y, braking, and throttle to numpy arrays for vectorized operations
        y = np.array(y)
        braking = np.array(braking)
        throttle = np.array(throttle)

        # Create a 3D plot
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')

        # Create a list of points and segments
        points = np.array([x, y, z]).T.reshape(-1, 1, 3)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        # Normalize throttle and braking values to the range [0, 1]
        throttle_norm = throttle / 100
        braking_norm = braking / 100

        # Calculate colors based on throttle and braking values
        colors = []
        for t, b in zip(throttle_norm, braking_norm):
            if t > 0 and b == 0:  # Only throttle
                color = (1 - t, 1, 1 - t)  # Shades of green
            elif b > 0 and t == 0:  # Only braking
                color = (1, 1 - b, 1 - b)  # Shades of red
            elif t == 0 and b == 0:  # No throttle and no braking
                color = (1, 1, 1)  # White
            else:  # Both throttle and braking
                color = (1 - t, 1 - b, 1)  # Blend of green and red
            colors.append(color)

        lc = Line3DCollection(segments, colors=colors, linewidth=2)

        ax.add_collection(lc)

        # Set labels
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_zlabel('Z-axis')

        # Set limits for better visualization
        ax.set_xlim([min(x), max(x)])
        ax.set_ylim([min(y), max(y)])
        ax.set_zlim(-200,200) 

        # Set title
        plt.title('Lap with Throttle and Braking Color Gradient')
        plt.grid(True)
        
        return fig, plt, ax, base_filename
