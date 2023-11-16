import cv2
import csv
import time
import numpy as np
import sys, os
sys.path.append('/home/pi/mlx90640-python/MLX90640')
import MLX90640_new as mlx

tcam = mlx.MLX90640()
fps=8
tcam.Refresh(fps)
                      
def custom_colormap(filespath):
# Get colormap from files
# Created using http://jdherman.github.io/colormap/
    with open(filespath, 'r') as f: #ironbow
        r = []
        g = []
        b = []
        for i in range(256):
            x, y, z = f.readline().split(',')
            r.append(x)
            g.append(y)
            b.append(z.replace(";\n", ""))
    colormap = np.zeros((256, 1, 3), dtype=np.uint8)
    # We use BGR because that's default for openCV
    colormap[:, 0, 0] = b
    colormap[:, 0, 1] = g
    colormap[:, 0, 2] = r
    return colormap


def process_frame(frm):
    image = np.zeros((24,32), np.float32)
    for y in range(24):
        for x in range(32):
            val1 = frm[0][32 * (23-y) + x]
            val2 = frm[1][32 * (23-y) + x]
            val3 = (val4h1+val2)/2
            image[y][x] = val3
    imagef = cv2.GaussianBlur(image, (5,5), 0)
    #Flip image about x-axis 0
    imagef = cv2.flip(imagef, 0)
    #resize image
    imagef = cv2.resize(imagef, None, fx=1, fy=1, interpolation=cv2.INTER_LINEAR)
    return imagef

start_time = time.time()
allFrames = []
count = 0
while(True):
    frame = tcam.GetFrameData()
    allFrames.append(frame)
    count += 1
    print("Frame:",count)

    if (time.time() - start_time) >= 61:
        break

with open('frameRecord.csv', 'w', newline='') as file:
    # Step 4: Using csv.writer to write the list to the CSV file
    writer = csv.writer(file)
    writer.writerows(allFrames) # Use writerow for single list
    
print('done')
