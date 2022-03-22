import cv2
from itertools import product
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import os

boardsize = (7,7)

vid = cv2.VideoCapture(0)
ret, frame = vid.read()

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
found, corners = cv2.findChessboardCorners(gray, boardsize, flags=cv2.CALIB_CB_NORMALIZE_IMAGE|cv2.CALIB_CB_ADAPTIVE_THRESH)
print(found)
z = corners.reshape((49,2))
board_center = z[24]
frame_center = frame.shape[1] / 2.0, frame.shape[0] / 2.0
cv2.imwrite("origin_camera_frame.jpg", frame)

X_train = np.array(list(product(np.linspace(-3, 3, 7), np.linspace(-3, 3, 7))))

poly = PolynomialFeatures(degree=4)
X_train = poly.fit_transform(X_train)

m_x = LinearRegression()
m_x.fit(X_train, z[:, 0])

m_y = LinearRegression()
m_y.fit(X_train, z[:, 1])

def predict(i, j):
    features = poly.fit_transform(np.array([[i, j]]))
    return m_x.predict(features), m_y.predict(features)

P = []
Q = []

P.append(predict(-4.0, -4.0))
Q.append((0.0, 0.0))

P.append(predict(-4.0, 4.0))
Q.append((0.0, 480.0))

P.append(predict(4.0, -4.0))
Q.append((480.0, 0.0))

P.append(predict(4.0, 4.0))
Q.append((480.0, 480.0))

Q = np.array(Q, np.float32)
P = np.array(P, np.float32).reshape(Q.shape)
ind = np.lexsort((P[:,1],P[:,0]))
P = P[ind]

M = cv2.getPerspectiveTransform(P, Q)
perspective_path = "./perspectiveMatrix.npy"
np.save(perspective_path, M)
frame = cv2.warpPerspective(frame, M, (480, 480))
cv2.imwrite('chessboard.jpg',frame)
while(True):
    
    cv2.imshow('frame',frame)

    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break
vid.release()

cv2.destroyAllWindows()