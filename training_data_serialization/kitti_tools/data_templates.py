"""
One raw data includes
    - PointClouds
    - RGB (H x W x C)
    - Ground Truth Transform (Extrinsic Calibration Matrix)
    - Camera Matrix-s (P, R, ...)
One training data includes
    - X
        - PointClouds
        - RGB (H x W x C)
        - Initial Transform (Generated by injecting random transform in Ground Truth Transform in raw data)
        - Initial Depth Map (Projecting PointClouds into RGB and count points to construct pixel)
    - y
        - Ground Truth Transform (Re-calculated with the random transform)
        - Classifier Label
        - Regressor Label
"""
import cv2
import numpy as np
from copy import deepcopy


class RawData(object):
    def __init__(self):
        self.pts_fp = None
        self.rgb_fp = None
        self.transform_mat = None
        self.cam_mat_P = None
        self.cam_mat_R = None
        self.id = None

        # Below data could be loaded in run-time by calling load function to save resources
        self.pts_data = None
        self.rgb_data = None

    def load(self):
        self.pts_data = np.fromfile(self.pts_fp, dtype=np.float32).reshape((-1, 4))[:, :4]
        self.rgb_data = cv2.imread(self.rgb_fp)

    def inspect(self):
        print("-----------------------------Inspecting---------------------------")
        print("self.pts_fp: {}".format(self.pts_fp))
        print("self.rgb_fp: {}".format(self.rgb_fp))
        print("[Shape = {}]     self.transform_mat: {}".format(self.transform_mat.shape, self.transform_mat))
        print("[Shape = {}]     self.cam_mat_P: {}".format(self.cam_mat_P.shape, self.cam_mat_P))
        print("[Shape = {}]     self.cam_mat_R: {}".format(self.cam_mat_R.shape, self.cam_mat_R))
        print("------------------------------------------------------------------")


class TrainingData(object):

    def __init__(self, raw_data=None):
        # deepcopy here is necessary so that when loading the raw data the memory does not leak
        self.raw_data = deepcopy(raw_data)
        self.raw_data.load()
        self.pts_data = self.raw_data.pts_data
        self.rgb_data = self.raw_data.rgb_data
        self._set_Xs()
        self._set_Ys()

    def _set_Xs(self):
        # For VAE
        self.x_dm_ft_resized = None
        self.x_cam_resized = None

        # For RGGNet
        self.x_dm = None
        self.x_cam = None
        self.x_R_rects = None
        self.x_P_rects = None

    def _set_Ys(self):
        self.y_se3param = None
        self.y_dm = None

    def inspect(self):
        print("-----------------------------Inspecting---------------------------")
        print("self.raw_data.pts_fp: {}".format(self.raw_data.pts_fp))
        print("self.raw_data.rgb_fp: {}".format(self.raw_data.rgb_fp))
        print("[Shape = {}]     self.pts_data".format(self.pts_data.shape))
        print("[Shape = {}]     self.rgb_data".format(self.rgb_data.shape))
        print("------------------------------------------------------------------")
