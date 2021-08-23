'''
Takes the ppm image output from VMD and converts them to PNGs.
These can then be merged in blender to create a movie of the trajectory.
'''
import os

directory = './'
# Loop through all images in the current directory
count = 0
for filename in sorted(os.listdir(directory)):
    file = os.path.join(directory, filename)
    
    # Checking if it is a file
    if os.path.isfile(file):
        os.system('pnmtopng {} > {}.png'.format(file, count))
        count += 1