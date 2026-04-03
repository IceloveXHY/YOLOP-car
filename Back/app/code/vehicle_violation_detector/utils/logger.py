import os
import csv
import cv2

class ViolationLogger:
    def __init__(self, csv_path, img_dir):
        self.img_dir = img_dir

        os.makedirs(self.img_dir, exist_ok=True)

        self.csv_file = open(csv_path, "w", newline="")
        self.writer = csv.writer(self.csv_file)
        self.writer.writerow(["Vehicle_ID", "Frame", "Time(s)", "Saved_Image"])

    def log_violation(self, frame, vid, frame_idx, box, time_in_roi):
        img_crop = frame[box[1]:box[3], box[0]:box[2]]
        img_name = f"{self.img_dir}/vid{vid}_frame{frame_idx}.jpg"
        cv2.imwrite(img_name, img_crop)
        self.writer.writerow([vid, frame_idx, f"{time_in_roi:.1f}", img_name])

    def close(self):
        self.csv_file.close()
