import json
from flask import Flask
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import matplotlib
import argparse
import utils
import cv2
import requests
import os 

def centroid_histogram(clt):
	# grab the number of different clusters and create a histogram
	# based on the number of pixels assigned to each cluster
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)
	# normalize the histogram, such that it sums to one
	hist = hist.astype("float")
	hist /= hist.sum()
	# return the histogram
	return hist

def plot_colors(hist, centroids):
	# initialize the bar chart representing the relative frequency
	# of each of the colors
	bar = np.zeros((50, 300, 3), dtype = "uint8")
	startX = 0
	# loop over the percentage of each cluster and the color of
	# each cluster
	for (percent, color) in zip(hist, centroids):
		# plot the relative percentage of each cluster
		endX = startX + (percent * 300)
		cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
			color.astype("uint8").tolist(), -1)
		startX = endX
	
	# return the bar chart
	return bar

app = Flask(__name__)


        
@app.route('/')
def index():
    return json.dumps({'logo_border': Border_color,
                       'dominant_color': Dominant_color})
                       
response = requests.get("https://storage.googleapis.com/bizupimg/profile_photo/goodwell_logo.png")

file = open("sample_image.png", "wb")
file.write(response.content)
file.close()
  
imag = cv2.imread(r"C:\Users\kaush\Desktop\python\sample_image.png")
imag = cv2.cvtColor(imag, cv2.COLOR_BGR2RGB)
# show our image
#plt.figure()
#plt.axis("off")
#plt.imshow(imag)

# reshape the image to be a list of pixels
imag = imag.reshape((imag.shape[0] * imag.shape[1], 3))
# cluster the pixel intensities
clt = KMeans(n_clusters = 3)
clt.fit(imag)
# build a histogram of clusters and then create a figure
# representing the number of pixels labeled to each color

hist = centroid_histogram(clt)
bar = plot_colors(hist, clt.cluster_centers_)
colo= clt.cluster_centers_
Dominant_color= matplotlib.colors.to_hex(colo[0]/255)
Border_color = matplotlib.colors.to_hex(colo[1]/255)

print(Border_color, Dominant_color)
# show our color bart
#plt.figure()
#plt.axis("off")
#plt.imshow(bar)
#plt.show()
os.unlink(r"C:\Users\kaush\Desktop\python\sample_image.png")

app.run()

