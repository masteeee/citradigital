import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from sklearn.cluster import KMeans
from PIL import Image, ImageTk

class ColorMoodAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Program Mood Warna")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize variables
        self.current_image = None
        self.current_image_path = None
        self.photo = None
        
        # Define color moods
        self.color_moods = {
            'Bahagia': {'colors': [(255, 255, 0), (255, 165, 0), (255, 192, 203), (255, 215, 0), (255, 239, 213)]},
            'Sedih': {'colors': [(0, 0, 139), (25, 25, 112), (47, 79, 79)]},
            'Marah': {'colors': [(255, 0, 0), (139, 0, 0), (178, 34, 34)]},
            'Tenang': {'colors': [(173, 216, 230), (135, 206, 235), (176, 224, 230)]},
            'Natural': {'colors': [(34, 139, 34), (0, 128, 0), (144, 238, 144)]},
            'Elegant': {'colors': [(0, 0, 0), (169, 169, 169), (192, 192, 192)]},
            'Vintage': {'colors': [(160, 82, 45), (139, 69, 19), (205, 133, 63)]},
            'Modern': {'colors': [(105, 105, 105), (128, 128, 128), (211, 211, 211)]},
            'Dreamy': {'colors': [(230, 230, 250), (221, 160, 221), (218, 112, 214)]},
            'Warm': {'colors': [(205, 92, 92), (240, 128, 128), (250, 128, 114)]},
            'Cool': {'colors': [(0, 139, 139), (0, 128, 128), (72, 209, 204)]}
        }
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title Frame
        title_frame = tk.Frame(self.root, bg='#e0e0e0', relief='raised', borderwidth=1)
        title_frame.pack(fill='x', padx=20, pady=10)
        
        title_label = tk.Label(title_frame, text="Program Mood Warna", 
                             font=('Arial', 16, 'bold'), bg='#e0e0e0')
        title_label.pack(pady=10)
        
        # Members Frame
        members_frame = tk.Frame(title_frame, bg='#e0e0e0')
        members_frame.pack(pady=5)
        
        members_title = tk.Label(members_frame, text="Anggota Kelompok 4:", 
                               font=('Arial', 12, 'bold'), bg='#e0e0e0')
        members_title.pack(anchor='w')
        
        # Member list in columns
        members = [
            "1. Mulya Adi Saputra (221011401587)", "3. Muhammad Ario Ardhi (221011403129)", "5. Anisa Karenina (221011400758)",
            "2. Muhammad Fakhri Azmar (221011402596)", "4. Abimanyu Fakhrudin Qois (221011403114)", "6. Indika Saputra (221011402182)"
        ]
        
        member_frame = tk.Frame(members_frame, bg='#e0e0e0')
        member_frame.pack()
        
        for i, member in enumerate(members):
            row = i // 3
            col = i % 3
            tk.Label(member_frame, text=member, bg='#e0e0e0', 
                    font=('Arial', 11)).grid(row=row, column=col, padx=20, pady=2)
        
        # Main content frame
        content_frame = tk.Frame(self.root)
        content_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Left side - Image
        left_frame = tk.Frame(content_frame)
        left_frame.pack(side='left', expand=True, fill='both')
        
        image_label = tk.Label(left_frame, text="Gambar", font=('Arial', 12, 'bold'))
        image_label.pack(pady=5)
        
        self.image_frame = tk.Frame(left_frame, width=500, height=400)
        self.image_frame.pack(expand=True)
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(expand=True)
        
        # Right side - Histogram
        right_frame = tk.Frame(content_frame)
        right_frame.pack(side='right', expand=True, fill='both')
        
        histogram_label = tk.Label(right_frame, text="Histogram", font=('Arial', 12, 'bold'))
        histogram_label.pack(pady=5)
        
        # Create matplotlib figure for histogram
        self.fig = Figure(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(expand=True, fill='both')
        
        # Buttons frame at bottom
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # Create rounded buttons
        self.open_button = tk.Button(button_frame, text="Buka Gambar", 
                                   command=self.open_image, 
                                   relief='raised',
                                   font=('Arial', 10),
                                   bg='#e0e0e0',
                                   padx=20, pady=10)
        self.open_button.pack(side=tk.LEFT, padx=20)
        
        self.histogram_button = tk.Button(button_frame, text="Tampilkan Histogram",
                                        command=self.show_histogram,
                                        relief='raised',
                                        font=('Arial', 10),
                                        bg='#e0e0e0',
                                        padx=20, pady=10)
        self.histogram_button.pack(side=tk.LEFT, padx=20)
        
    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.webp")]
        )
        if file_path:
            self.current_image_path = file_path
            self.current_image = cv2.imread(file_path)
            self.display_image(file_path)
            
    def display_image(self, file_path):
        # Open and resize image for display
        pil_image = Image.open(file_path)
        
        # Calculate new size while maintaining aspect ratio
        display_size = (500, 400)
        pil_image.thumbnail(display_size, Image.Resampling.LANCZOS)
        
        # Convert to PhotoImage and store it
        self.photo = ImageTk.PhotoImage(pil_image)
        
        # Update label with new image
        self.image_label.configure(image=self.photo)
        self.image_label.image = self.photo
            
    def analyze_mood(self):
        if self.current_image is None:
            messagebox.showerror("Error", "Please open an image first")
            return None
            
        # Resize image for clustering
        rgb_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
        reshaped_image = rgb_image.reshape(-1, 3)
        
        # Use KMeans clustering to find dominant colors
        kmeans = KMeans(n_clusters=5, random_state=0).fit(reshaped_image)
        dominant_colors = kmeans.cluster_centers_
        
        min_distance = float('inf')
        closest_mood = None
        
        for mood, properties in self.color_moods.items():
            for color in properties['colors']:
                for dominant_color in dominant_colors:
                    distance = np.sqrt(np.sum((np.array(color) - dominant_color) ** 2))
                    if distance < min_distance:
                        min_distance = distance
                        closest_mood = mood
                        
        return closest_mood
            
    def show_histogram(self):
        if self.current_image is None:
            messagebox.showerror("Error", "Please open an image first")
            return
            
        self.fig.clear()
        
        b, g, r = cv2.split(self.current_image)
        
        ax = self.fig.add_subplot(111)
        ax.hist(b.ravel(), 256, [0, 256], color='blue', alpha=0.5, label='Biru')
        ax.hist(g.ravel(), 256, [0, 256], color='green', alpha=0.5, label='Hijau')
        ax.hist(r.ravel(), 256, [0, 256], color='red', alpha=0.5, label='Merah')
        
        mood = self.analyze_mood()
        
        ax.set_xlabel('Intensitas Piksel')
        ax.set_ylabel('Frekuensi')
        ax.set_title(f'Histogram Warna - Mood: {mood}')
        ax.legend()
        
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = ColorMoodAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
