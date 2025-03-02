import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import colorchooser
from lru import LRUCache

class ColorApp:
    """ Aplicación gráfica con explicación de la caché LRU """
    def __init__(self, root, cache_size=5):
        self.root = root
        self.root.title("Pintar con LRU Cache")
        self.root.geometry("500x700")

        self.canvas = tk.Canvas(root, width=380, height=380, bg="white", relief="solid", bd=2)
        self.canvas.pack(pady=15)

        self.btn_select = ttk.Button(root, text="🎨 Elegir Color", command=self.choose_color, bootstyle=PRIMARY)
        self.btn_select.pack(pady=10)

        self.cache = LRUCache(cache_size)

        self.label_recent = ttk.Label(root, text="🎨 Colores recientes", font=("Arial", 12, "bold"))
        self.label_recent.pack(pady=5)
        self.recent_frame = ttk.Frame(root)
        self.recent_frame.pack()

        self.state_label = ttk.Label(root, text="📜 Estado de la Caché:", font=("Arial", 10, "bold"))
        self.state_label.pack(pady=5)
        self.state_text = tk.Text(root, height=5, width=50, state="disabled", wrap="word")
        self.state_text.pack(pady=5)

        self.explanation_label = ttk.Label(root, text="ℹ️ Selecciona un color para ver cómo funciona la caché.", wraplength=400, font=("Arial", 10))
        self.explanation_label.pack(pady=10)

        self.slider_frame = ttk.Frame(root)
        self.slider_frame.pack(pady=5)

        self.slider_label = ttk.Label(self.slider_frame, text="📏 Tamaño de la Caché:", font=("Arial", 12, "bold"))
        self.slider_label.pack(side="left")
        
        self.slider_value = ttk.Label(self.slider_frame, text=f"{cache_size}", font=("Arial", 12, "bold"), width=3)
        self.slider_value.pack(side="left", padx=10)
        
        self.slider = ttk.Scale(root, from_=1, to=10, orient="horizontal", length=200, command=self.update_cache_size)
        self.slider.set(cache_size)
        self.slider.pack(pady=5)

        self.update_recent_colors()

    def choose_color(self):
        color = colorchooser.askcolor(title="Selecciona un color")[1]
        if color:
            self.canvas.config(bg=color)
            self.cache.put(color, color)
            self.update_recent_colors()

            message = f"🎨 Has seleccionado {color}. Se ha movido al final de la caché."
            if len(self.cache.cache) > self.cache.capacity:
                message += f"\n❌ La caché estaba llena. Se eliminó el color menos usado."
            self.explanation_label.config(text=message)

    def update_recent_colors(self):
        for widget in self.recent_frame.winfo_children():
            widget.destroy()

        colors = self.cache.get_recent_colors()
        for color, usage_count in colors:
            frame = tk.Canvas(self.recent_frame, width=50, height=50, highlightthickness=1, highlightbackground="gray")
            frame.create_oval(5, 5, 45, 45, fill=color, outline="black")
            frame.pack(side="left", padx=5, pady=5)
            frame.bind("<Button-1>", lambda e, c=color: self.set_canvas_color(c))

        self.update_state_text()

    def set_canvas_color(self, color):
        self.canvas.config(bg=color)
        self.cache.get(color)
        self.update_recent_colors()
        self.explanation_label.config(text=f"🔄 Has reutilizado el color {color}. Se ha movido al final de la caché.")

    def update_cache_size(self, value):
        new_size = int(float(value))
        self.cache.set_capacity(new_size)
        self.update_recent_colors()
        self.slider_value.config(text=f"{new_size}")
        self.explanation_label.config(text=f"⚙️ Tamaño de la caché cambiado a {new_size}")

    def update_state_text(self):
        self.state_text.config(state="normal")
        self.state_text.delete(1.0, tk.END)

        colors = self.cache.get_recent_colors()
        for color, usage_count in colors:
            self.state_text.insert(tk.END, f"🎨 {color} - Usado {usage_count} veces\n")

        self.state_text.config(state="disabled")

if __name__ == "__main__":
    root = ttk.Window(themename="superhero") 
    app = ColorApp(root)
    root.mainloop()