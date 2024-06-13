from .debrisdetector import DerbrisDetector
import torch
import numpy as np

import os
from os import listdir
from os.path import isfile, join


class Yolo5TorchHub(DerbrisDetector):
    _description="""
    Official YOLOv5 implementation based on Pytorch and torch Hub.\n
    """

    def __init__(self, model_file="yolov5s", use_accel=True, model_type="yolov5s") -> None:
        super().__init__(None)
        self.net = torch.hub.load("ultralytics/yolov5", model_type)
        self.net.conf = 0.25  # NMS confidence threshold
        self.net.iou = 0.45  # NMS IoU threshold
        self.net.agnostic = False  # NMS class-agnostic
        self.net.multi_label = False  # NMS multiple labels per box
        self.net.classes = None  # (optional list) filter by class, i.e. = [0, 15, 16] for COCO persons, cats and dogs
        self.net.max_det = 1000  # maximum number of detections per image
        #self.net.amp = True  # Automatic Mixed Precision (AMP) inference

        if use_accel:
            self.net.cuda()
            self.net.amp = True  # Automatic Mixed Precision (AMP) inference
        else:
            self.net.cpu()

        self.img_width = 1280
        self.img_height = 640

        self.list_classes=[]
        for clsnr in range(max(list(self.net.names.keys()))+1):
            self.list_classes.append(self.net.names[clsnr])
            
        self.dtype=np.float32
        



    def apply_model(self, inputs, confidence_threshold=0.2, class_threshold=0.25):  
        self.net.conf = confidence_threshold  # NMS confidence threshold
        row, col, _ = inputs.shape
        results = self.net([inputs], size=row)

        res =  results.xyxy[0]
        result_class_ids = []
        result_confidences = []
        result_boxes = []

        for i in range(res.shape[0]):
            result_class_ids.append(int(res[i,5]))
            result_confidences.append(res[i,4])
            left = res[i,0]
            top = res[i,1]
            width = res[i,2]-res[i,0]
            height = res[i,3]-res[i,1]
            bbox = np.array([left, top, width, height])
            result_boxes.append(bbox)

        return result_class_ids, result_confidences, result_boxes
    
    def apply_model_percent(self, inputs, confidence_threshold=0.2, class_threshold=0.25):  
        self.net.conf = confidence_threshold  # NMS confidence threshold
        row, col, _ = inputs.shape
        results = self.net([inputs], size=row)

        res =  results.xyxy[0]
        result_class_ids = []
        result_confidences = []
        result_boxes = []

        for i in range(res.shape[0]):
            result_class_ids.append(int(res[i,5]))
            result_confidences.append(res[i,4])
            left = res[i,0]/self.img_width
            top = res[i,1]/self.img_height
            width = (res[i,2]-res[i,0])/self.img_width
            height = (res[i,3]-res[i,1])/self.img_height
            bbox = np.array([left, top, width, height])
            result_boxes.append(bbox)

        return result_class_ids, result_confidences, result_boxes
    
DerbrisDetector.add_model("YOLOv5_Original", Yolo5TorchHub)
