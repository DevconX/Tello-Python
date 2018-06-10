import socket
import threading
import time
import pickle
import cv2
from Detection.MtcnnDetector import MtcnnDetector
from Detection.detector import Detector
from Detection.fcn_detector import FcnDetector
from train_models.mtcnn_model import P_Net, R_Net, O_Net
import visualization_utils

thresh = [0.7, 0.1, 0.1]
min_face_size = 24
stride = 2
slide_window = True
shuffle = False
detectors = [None, None, None]
prefix = ['data/MTCNN_model/PNet_landmark/PNet', 'data/MTCNN_model/RNet_landmark/RNet', 'data/MTCNN_model/ONet_landmark/ONet']
epoch = [18, 14, 16]
model_path = ['%s-%s' % (x, y) for x, y in zip(prefix, epoch)]
PNet = FcnDetector(P_Net, model_path[0])
detectors[0] = PNet
RNet = Detector(R_Net, 24, 1, model_path[1])
detectors[1] = RNet
ONet = Detector(O_Net, 48, 1, model_path[2])
detectors[2] = ONet
mtcnn_detector = MtcnnDetector(detectors=detectors, min_face_size=min_face_size,stride=stride, threshold=thresh, slide_window=slide_window)

header = b'\x00\x00\x00\x01gM@(\x95\xa0<\x05\xb9\x00\x00\x00\x01h\xee8\x80'
h264 = []

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock_video = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock_video.bind(('192.168.10.3', 6038))

def receive_video():
    global h264
    while True:
        data, addr = sock_video.recvfrom(2048)
        if len(data[2:]) not in [8,13]:
            h264.append(data[2:])

def run_cam():
    global h264
    while True:
        k = sum([int(len(i) < 1000) for i in h264])
        temp = []
        for i in reversed(range(len(h264))):
            if len(h264[i]) < 1000:
                count, temp = 0, [h264[i]]
                for n in reversed(range(len(h264[:i]))):
                    if len(h264[n]) < 1000:
                        count += 1
                    if count == 3:
                        break
                    temp.append(h264[n])
            break
        if k > 2:
            with open('temp.h264','wb') as fopen:
                fopen.write(header+b''.join(temp[::-1]))
            h264.clear()
            cap = cv2.VideoCapture('temp.h264')
            while True:
                try:
                    ret, img = cap.read()
                    boxes_c,_ = mtcnn_detector.detect(img)
                    for u in range(boxes_c.shape[0]):
                        bbox = boxes_c[u, :4]
                        visualization_utils.draw_bounding_box_on_image_array(img,int(bbox[1]),int(bbox[0]),
                                                                             int(bbox[3]),
                                                                             int(bbox[2]),
                                                                             'YellowGreen',display_str_list=['face'],
                                                                             use_normalized_coordinates=False)
                    cv2.imshow('cam',img)
                    if cv2.waitKey(30) & 0xFF == ord('q'):
                        break
                except:
                    break

receive_thread = threading.Thread(target=receive_video)
receive_thread.daemon=True
receive_thread.start()
receive_cam_thread = threading.Thread(target=run_cam)
receive_cam_thread.daemon = True
receive_cam_thread.start()

command = bytearray.fromhex('9617')
sock.sendto(b'conn_req:'+bytes(command), ('192.168.10.1',8889))
sock.sendto(bytes(bytearray.fromhex('cc58007c60250000006c95')), ('192.168.10.1',8889))
sock.sendto(bytes(bytearray.fromhex('cc600027682000000004fd9b')), ('192.168.10.1',8889))
try:
    while True:
        time.sleep(0.1)
        sock.sendto(bytes(bytearray.fromhex('cc58007c60250000006c95')), ('192.168.10.1',8889))
except KeyboardInterrupt:
    pass
