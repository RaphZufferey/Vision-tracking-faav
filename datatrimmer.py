import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

class DataFramePlotter:
	def __init__(self, root):
		self.root = root
		self.dataframe = None
		self.fig, self.ax = plt.subplots()
		self.canvas = None
		self.trim_button = None
		self.start_slider = None
		self.end_slider = None
		self.file_button = None  # Initialize file_button widget
		self.file_path = None 
		
		self.create_gui()

	def create_gui(self):
		self.root.title("CSV data trimmer")

		if self.dataframe is not None:
			
			if self.file_button:  # Check if file_button exists
				self.file_button.destroy()  # Remove file_button
			self.plot_dataframe()
			slider_frame = ttk.Frame(self.root)
			slider_frame.pack(padx=10, pady=10)

			ttk.Label(slider_frame, text="Start Index:").pack(side="left")
			self.start_slider = ttk.Scale(slider_frame, from_=0, to=len(self.dataframe), orient="horizontal", length=self.root.winfo_screenwidth()*0.3, command=self.update_plot)
			self.start_slider.pack(side="left", padx=5)

			ttk.Label(slider_frame, text="End Index:").pack(side="left")
			self.end_slider = ttk.Scale(slider_frame, from_=0, to=len(self.dataframe), orient="horizontal", length=self.root.winfo_screenwidth()*0.3, command=self.update_plot)
			self.end_slider.set(len(self.dataframe))  # Set the initial position to the end
			self.end_slider.pack(side="left", padx=5)

			self.trim_button = ttk.Button(self.root, text="Trim Data", command=self.trim_data)
			self.trim_button.pack(pady=5)
		else:
			self.file_button = ttk.Button(self.root, text="Choose File",command=self.choose_file )
			self.file_button.pack(pady=50, padx= 150)
		
	def plot_dataframe(self):
		screen_width = self.root.winfo_screenwidth()
		screen_height = self.root.winfo_screenheight()

		# Set the size as a percentage of the screen resolution
		width_percentage = 0.8  # Adjust as needed
		height_percentage = 0.6  # Adjust as needed

		width = int(screen_width * width_percentage)
		height = int(screen_height * height_percentage)

		self.fig.set_size_inches(width / 100, height / 100)
		self.ax.clear()
		self.dataframe.plot(ax=self.ax)
		self.ax.set_title("DataFrame Plot")
		self.ax.set_xlabel("X")
		self.ax.set_ylabel("Y")

		if self.canvas:
			self.canvas.get_tk_widget().destroy()

		self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
		self.canvas.get_tk_widget().pack()

	def update_plot(self, _):
		start_index = int(self.start_slider.get())
		end_index = int(self.end_slider.get())
		
		if start_index >= end_index:
			return
		
		self.ax.clear()
		self.dataframe[start_index:end_index].plot(ax=self.ax)
		self.ax.set_title("DataFrame Plot")
		self.ax.set_xlabel("X")
		self.ax.set_ylabel("Y")
		self.canvas.draw()

	def trim_data(self):
		start_index = int(self.start_slider.get())
		end_index = int(self.end_slider.get())
		
		if start_index >= end_index:
			return
		
		self.dataframe = self.dataframe[start_index:end_index]
		self.plot_dataframe()

		# Save cropped data to a CSV file
		# self.file_path = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
		
		if self.file_path:
			file_parts = self.file_path.rsplit('.', 1)
			trimmed_file_path = f"{file_parts[0]}_trim.{file_parts[1]}"
			self.dataframe.to_csv(trimmed_file_path, index=False)
			print(f"Trimmed data saved to: {trimmed_file_path}")
			self.root.destroy()
			quit()

	def choose_file(self):
		self.file_path = tk.filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
		if self.file_path:
			self.dataframe = pd.read_csv(self.file_path)
			self.create_gui()  # Re-create the GUI with the new DataFrame


def main():
	# Load your DataFrame here
	# data = {
	# 	"X": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
	# 	"Y": [2, 4, 1, 7, 5, 8, 3, 6, 9, 2]
	# }
	# df = pd.DataFrame(data)

	
	root = tk.Tk()
	app = DataFramePlotter(root)
	root.mainloop()

if __name__ == "__main__":
	main()
