import numpy as np
from sklearn.cluster import DBSCAN


def cluster_faces(embeddings, eps=0.35):
    """Cluster L2-normalized face embeddings using cosine distance.

    eps is intentionally configurable because the appropriate threshold must be
    validated against the target image collection.
    """
    if not embeddings:
        return np.array([], dtype=int)

    matrix = np.asarray(embeddings, dtype=np.float32)
    return DBSCAN(
        eps=eps,
        min_samples=1,
        metric='cosine'
    ).fit_predict(matrix)
