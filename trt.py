import sys
sys.path.append('../')
from utils.utils import preproc, vis
from utils.utils import BaseEngine
import numpy as np
import cv2
import time
import os


class Predictor(BaseEngine):
    def __init__(self, engine_path , imgsz=(640,640)):
        super(Predictor, self).__init__(engine_path)
        self.imgsz = imgsz
        self.n_classes = 80
        self.class_names = [ 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
         'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
         'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
         'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
         'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
         'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
         'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
         'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
         'hair drier', 'toothbrush' ]
    def inference(self, frame):
        #origin_img = cv2.imread(img_path)
        origin_img = frame
        mean = None
        std = None
        img, ratio = preproc(origin_img, self.imgsz, mean, std)
        t1 = time.time()
        data = self.infer(img,half=False)
        print(1 / (time.time() - t1))
        predictions = np.reshape(data, (1, -1, int(5+self.n_classes)))[0]
        dets = self.postprocess(predictions,ratio)
        # import pdb
        # pdb.set_trace()
        if dets is not None:
            final_boxes, final_scores, final_cls_inds = dets[:,
                                                             :4], dets[:, 4], dets[:, 5]
            origin_img = vis(origin_img, final_boxes, final_scores, final_cls_inds,
                             conf=0.5, class_names=self.class_names)
        return origin_img

        # cv2.imwrite("%s_yolov6.jpg" % os.path.splitext(
        #     os.path.split(img_path)[-1])[0], origin_img)


if __name__ == '__main__':
    pred = Predictor(engine_path='model.engine')
    #img_path = '../imgs/3.jpg'
    cap = cv2.VideoCapture(0)
    while 1 :
        _,frame = cap.read()
        frame = pred.inference(frame)
        cv2.imshow("frame",frame)
        ch = cv2.waitKey(1)
        if ch == ord("q") : break
