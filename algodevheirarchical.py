import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram
from skimage import io, color, segmentation

image = io.imread('path/to/your/image.jpg')
gray_image = color.rgb2gray(image)
segments = segmentation.slic(image, n_segments=300, compactness=10, sigma=1)
X = np.column_stack([gray_image.flatten(), segments.flatten()])

model = AgglomerativeClustering(n_clusters=None, distance_threshold=0)
model.fit(X)
labels = model.labels_

def plot_dendrogram(model, **kwargs):
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                      counts]).astype(float)

    dendrogram(linkage_matrix, **kwargs)

plt.figure(figsize=(12, 6))
plt.title('Hierarchical Clustering Dendrogram')
plot_dendrogram(model, truncate_mode='level', p=3)
plt.xlabel("Number of points in node (or index of point if no parenthesis).")
plt.show()
