import cv2
import rosbag
from std_msgs.msg import Int32, String

bag = rosbag.Bag('data_new.bag')

for topic, msg, t in bag.read_messages(topics=['/camera/depth/color/points']):
    print(msg)
bag.close()


# TODO chessboard detection, wait until chessboard is detected
img = img
boardsize = (7,7)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
found, corners = cv2.findChessboardCorners(gray, boardsize, flags=cv2.CALIB_CB_NORMALIZE_IMAGE|cv2.CALIB_CB_ADAPTIVE_THRESH)
if(found):    
    # TODO chessboard state recognition
    z = corners.reshape((49,2))
    board_center = z[24]
# TODO 