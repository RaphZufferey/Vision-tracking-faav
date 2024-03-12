import cv2
import pandas as pd
import numpy as np
from tkinter import filedialog
import tkinter as tk
import os
from tkinter import messagebox

class DataFramePlotter:
	def __init__(self):
		self.cap = None  # Video capture object
		self.tracker = None
		self.df = pd.DataFrame(columns=['frame_num', 'x_pos_px', 'y_pos_px', 'distance_px'])
		self.output_path = None

	def choose_file(self):
		root = tk.Tk()
		root.withdraw()  # Hide the main window

		self.output_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mkv")])
		if self.output_path:
			self.track_video()

	def track_video(self):
		self.cap = cv2.VideoCapture(self.output_path)
		ret, frame = self.cap.read()
		frame_height, frame_width, _ = frame.shape
		half_frame_height, half_frame_width = int(frame_height / 2), int(frame_width / 2)
		confirmation = False
		while not confirmation:
			bbox = cv2.selectROI('Tracking', frame, False)
			confirmation = messagebox.askyesno("Bounding Box Confirmation", "Do you want to use this bounding box?")

		self.tracker = cv2.TrackerCSRT_create()
		self.tracker.init(frame, bbox)

		while True:
			ret, frame = self.cap.read()
			if not ret:
				break
			success, bbox = self.tracker.update(frame)

			if success:
				x, y, w, h = [int(i) for i in bbox]

				center_x = x + w / 2
				center_y = -(y + h / 2)  # Invert y so that y is up and x is right

				if len(self.df) == 0:
					x_init = center_x
					y_init = center_y

				X_m = (center_x - x_init)
				Y_m = (center_y - y_init)
				D_m = np.sqrt((center_x - x_init) ** 2 + (center_y - y_init) ** 2)

				self.df.loc[len(self.df)] = [self.cap.get(cv2.CAP_PROP_POS_FRAMES), X_m, Y_m, D_m]

			# Display the frame with the bounding box
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			cv2.imshow('Tracking', frame)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		self.cap.release()
		cv2.destroyAllWindows()

	def stop_tracking(self):
		if self.cap is not None:
			self.cap.release()
			cv2.destroyAllWindows()

	def confirm_roi(self):
		if self.tracker is not None:
			cv2.destroyAllWindows()

	def export_to_csv(self):
		if self.output_path and not self.df.empty:
			video_dir, video_filename = os.path.split(self.output_path)
			csv_filename = os.path.splitext(video_filename)[0] + '_tracking.csv'
			csv_path = os.path.join(video_dir, csv_filename)
			
			# Ask for confirmation
			confirmation = messagebox.askyesno("Export DataFrame", "Do you want to save the DataFrame to a CSV file?")
			
			if confirmation:
				self.df.to_csv(csv_path, index=False)
				print(f"DataFrame exported to: {csv_path}")
			else:
				print("DataFrame export cancelled.")



def main():
	plotter = DataFramePlotter()
	plotter.choose_file()
	plotter.export_to_csv()


if __name__ == "__main__":
	main()
