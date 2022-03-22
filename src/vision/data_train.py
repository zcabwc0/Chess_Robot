import os
import numpy as np
import cv2
from sklearn.decomposition import PCA
from sklearn.svm import SVC
import pickle

color_labels = ['black','empty','white']

def load_data(label, path):
    labels = []
    images = []
    data_path = os.path.join(path,label)
    if(label == 'empty'):
        index = 0
    if(label == 'black'):
        index = 1
    if(label == 'white'):
        index = 2
    for dirs in os.listdir(data_path):
        img_path = os.path.join(data_path, dirs)
        images.append(np.asarray(cv2.imread(img_path)).flatten())
        labels.append(index)
    return labels, np.array(images)

def data_shuffle(dataset, labels):
    indices = np.arange(len(labels))
    np.random.shuffle(indices)
    dataset = dataset[indices]
    labels = labels[indices]
    return dataset, labels

def main():
    data_path = "./data/squares/color"
    dataset = np.ndarray([0,10800])
    data_labels = []
    for label in color_labels:
        labels, images = load_data(label,data_path)
        dataset = np.concatenate((dataset,images))
        data_labels += labels
    dataset, data_labels = data_shuffle(dataset,np.array(data_labels))
    train_size = int(len(data_labels) * 0.9)
    d_train = dataset[:train_size]
    d_val = dataset[train_size:]    
    y_train = data_labels[:train_size]
    y_val = data_labels[train_size:]
    pca = PCA(n_components=16, whiten=True)
    pca.fit(d_train)
    train_pca = pca.transform(d_train)
    val_pca = pca.transform(d_val)
    svc = SVC()
    svc.fit(train_pca, y_train)
    pred = svc.predict(val_pca)
    a = np.sum(pred == y_val) / float(y_val.shape[0])
    print("Accuracy: " + str(a))

    with open(os.path.join(data_path,"color_detection.pca"), 'wb') as file:
        pickle.dump(pca, file)
    with open(os.path.join(data_path,"color_detection.svc"), 'wb') as file:
        pickle.dump(svc, file)

main()
