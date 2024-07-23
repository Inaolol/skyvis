import numpy as np
import cv2

class PositionEstimator:
    def __init__(self):
        self.K = np.array([[1413.3, 0, 950.0639],
                           [0, 1418.8, 543.3796],
                           [0, 0, 1]])
        self.D = np.array([-0.0091, 0.0666, 0, 0, 0])
        self.focal_length_x = 1413.3
        self.focal_length_y = 1418.8
        self.position = np.array([0, 0], dtype=np.float32)
        self.prev_gray = None
        self.trajectories = []
        self.frame_idx = 0
        self.initial_position_set = False

        self.lk_params = dict(winSize=(15, 15),
                              maxLevel=2,
                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        self.feature_params = dict(maxCorners=20,
                                   qualityLevel=0.3,
                                   minDistance=10,
                                   blockSize=7)

    def set_initial_position(self, x, y):
        if not self.initial_position_set:
            self.position = np.array([x, y], dtype=np.float32)
            self.initial_position_set = True

    def estimate_position(self, frame):
        frame_undistorted = cv2.undistort(frame, self.K, self.D)
        frame_gray = cv2.cvtColor(frame_undistorted, cv2.COLOR_BGR2GRAY)

        if self.prev_gray is None:
            self.prev_gray = frame_gray
            return self.position

        if len(self.trajectories) > 0:
            p0 = np.float32([trajectory[-1] for trajectory in self.trajectories]).reshape(-1, 1, 2)
            p1, _st, _err = cv2.calcOpticalFlowPyrLK(self.prev_gray, frame_gray, p0, None, **self.lk_params)
            p0r, _st, _err = cv2.calcOpticalFlowPyrLK(frame_gray, self.prev_gray, p1, None, **self.lk_params)
            d = abs(p0 - p0r).reshape(-1, 2).max(-1)
            good = d < 1

            new_trajectories = []

            for trajectory, (x, y), good_flag in zip(self.trajectories, p1.reshape(-1, 2), good):
                if not good_flag:
                    continue
                trajectory.append((x, y))
                if len(trajectory) > 40:  # trajectory_len
                    del trajectory[0]
                new_trajectories.append(trajectory)

            self.trajectories = new_trajectories

            if len(p0) > 0 and len(p1) > 0:
                movement_px = np.mean(p1 - p0, axis=0).flatten()
                movement_meters_x = (movement_px[0] / self.focal_length_x)
                movement_meters_y = (movement_px[1] / self.focal_length_y)
                self.position += np.array([-movement_meters_x, -movement_meters_y])

        if self.frame_idx % 5 == 0:  # detect_interval
            mask = np.zeros_like(frame_gray)
            mask[:] = 255
            for x, y in [np.int32(trajectory[-1]) for trajectory in self.trajectories]:
                cv2.circle(mask, (x, y), 5, 0, -1)
            p = cv2.goodFeaturesToTrack(frame_gray, mask=mask, **self.feature_params)
            if p is not None:
                for x, y in np.float32(p).reshape(-1, 2):
                    self.trajectories.append([(x, y)])

        self.frame_idx += 1
        self.prev_gray = frame_gray

        return self.position

    def reset(self):
        self.position = np.array([0, 0], dtype=np.float32)
        self.prev_gray = None
        self.trajectories = []
        self.frame_idx = 0
        self.initial_position_set = False