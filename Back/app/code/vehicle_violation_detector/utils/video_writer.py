import cv2

class VideoWriter:
    def __init__(self, out_path, fps, frame_size):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(out_path, fourcc, fps, frame_size)

    def write(self, frame):
        self.out.write(frame)

    def release(self):
        self.out.release()
