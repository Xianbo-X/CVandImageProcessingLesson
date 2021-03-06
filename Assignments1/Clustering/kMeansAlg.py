import cv2
import numpy as np
import logging

def distance(data,center):
    return np.linalg.norm(data-center,ord=2,axis=1)

def AssignCluster(data,centroids):
    d=np.zeros((centroids.shape[0],data.shape[0]))
    for i in range(0,centroids.shape[0]):
        d[i]=distance(data,centroids[i])
    return np.argmin(d,axis=0)

def KMeansAlgForIris(featureData:np.ndarray,featurelength,totalClasses=2,maxSteps=1000,shuffle=False):
    '''
    feature Data: each row is a data point for iris it is a 4 dimensional vector for each data point.
    Total Classes: the given k
    '''
    rng = np.random.default_rng()
    centroidsIndex=rng.integers(0,featureData.shape[0],totalClasses)
    if shuffle:
        np.random.shuffle(featureData)
    centroids=featureData[centroidsIndex].copy()
    steps=0
    while(steps<=maxSteps):
        clussterAssigment=AssignCluster(featureData,centroids)
        clusters=[]
        lastCentroids=centroids.copy()
        # Update Centroids and construct the cluster
        for i in range(0,totalClasses):
            clusters.append(np.where(clussterAssigment==i)[0]) # the corresponding centroid has the smallest distance
            if len(clusters[i])==0:
                centroids[i]=featureData[rng.integers(0,featureData.shape[0],1)].copy()
                logging.debug("Empty cluster encountered")
            else:
                centroids[i]=np.mean(featureData[clusters[i]],axis=0)
                logging.debug("Update centroids %d \n"%i + str(centroids[i]))
        # if all(np.linalg.norm(lastCentroids-centroids,ord=2,axis=1)<0.001)
        steps+=1
        assert centroids.shape[1]==featureData.shape[1], str(centroids.shape[1])+"don't comply to feature dimension"+str(featureData.shape[1])
        if np.allclose(lastCentroids,centroids):
            logging.debug("Centroids converge, break,total step="+str(steps))
            break
    if (steps>maxSteps): logging.debug("Max steps exceeded:\tcurrent"+str(steps)+"\t Maximum step: "+str(maxSteps))
    return centroids