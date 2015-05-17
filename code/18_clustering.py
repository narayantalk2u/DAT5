'''
CLUSTER ANALYSIS
How do we implement a k-means clustering algorithm?

scikit-learn KMeans documentation for reference:
http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
'''

# Imports
from sklearn.cluster import KMeans # K means model
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Set random seed for reproducibility 
np.random.seed(0)

# Read in data
data = pd.read_csv('student_data.csv') # All values range from 0 to 1
data.head() # Look at data
data.describe() # Get summary of data

# Clean up the data
manual_labels = data.manual_label # Store labels
data.drop('manual_label', axis=1, inplace=True) # Drop labels from dataframe
data.head() # Confirm it was dropped

# Run KMeans
est = KMeans(n_clusters=4, init='random') # Instatiate estimator
est.fit(data) # Fit your data
y_kmeans = est.predict(data) # Make cluster "predictions"

# We can get the coordiantes for the center of each cluster
centers = est.cluster_centers_



'''
VISUALIZING THE CLUSTERS
'''

# We can create a nice plot to visualize this upon two of the dimensions
colors = np.array(['red', 'green', 'blue', 'yellow', 'orange'])

plt.figure()
plt.scatter(data.iloc[:, 2], data.iloc[:, 3], c=colors[y_kmeans], s=50)
plt.xlabel('Study Time')
plt.ylabel('Exam Performance')
plt.scatter(centers[:, 2], centers[:, 3], linewidths=3,
            marker='+', s=300)
plt.show()

# We can generate a scatter matrix to see all of the different dimensions paired
pd.scatter_matrix(data, c=colors[y_kmeans], figsize=(15,15), s = 100)
plt.show()

'''
DETERMINING THE NUMBER OF CLUSTERS
How do you choose k? There isn't a bright line, but we can evaluate 
performance metrics such as the silhouette coefficient across values of k.

Note:  You also have to take into account practical limitations of choosing k
also.  Ten clusters may give the best value, but it might not make sense in the
context of your data.

scikit-learn Clustering metrics documentation:
http://scikit-learn.org/stable/modules/classes.html#clustering-metrics
'''

# Create a bunch of different models
k_rng = range(2,15)
k_est = [KMeans(n_clusters = k).fit(data) for k in k_rng]

# Silhouette Coefficient
# Generally want SC to be closer to 1, while also minimizing k
from sklearn import metrics
silhouette_score = [metrics.silhouette_score(data, e.labels_, metric='euclidean') for e in k_est]

# Plot the results
plt.figure(figsize=(7, 8))
plt.subplot(211)
plt.title('Silhouette coefficient for various values of k')
plt.plot(k_rng, silhouette_score, 'b*-')
plt.xlim([1,15])
plt.grid(True)
plt.ylabel('Silhouette Coefficient')