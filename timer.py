import tkinter as tk
from tkinter import ttk, messagebox
import time
from threading import Thread
import winsound  # For Windows sound alerts

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Timer")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'))
        
        # Variables
        self.running = False
        self.remaining_time = 0
        self.timer_thread = None
        self.alarm_sound = True
        
        # Main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        ttk.Label(self.main_frame, text="Advanced Timer", style='Header.TLabel').pack(pady=10)
        
        # Timer display
        self.time_display = tk.Label(self.main_frame, text="00:00:00", 
                                   font=('Arial', 48), bg='black', fg='white')
        self.time_display.pack(pady=20)
        
        # Input frame
        input_frame = ttk.Frame(self.main_frame)
        input_frame.pack(pady=10)
        
        # Time input
        ttk.Label(input_frame, text="Hours:").grid(row=0, column=0, padx=5, pady=5)
        self.hours_entry = ttk.Spinbox(input_frame, from_=0, to=23, width=5)
        self.hours_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Minutes:").grid(row=1, column=0, padx=5, pady=5)
        self.minutes_entry = ttk.Spinbox(input_frame, from_=0, to=59, width=5)
        self.minutes_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Seconds:").grid(row=2, column=0, padx=5, pady=5)
        self.seconds_entry = ttk.Spinbox(input_frame, from_=0, to=59, width=5)
        self.seconds_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Alarm sound toggle
        self.sound_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(input_frame, text="Enable Alarm Sound", 
                       variable=self.sound_var).grid(row=3, column=0, columnspan=2, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=10)
        
        # Control buttons
        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.pause_button = ttk.Button(button_frame, text="Pause", command=self.pause_timer, state=tk.DISABLED)
        self.pause_button.grid(row=0, column=1, padx=5)
        
        self.reset_button = ttk.Button(button_frame, text="Reset", command=self.reset_timer)
        self.reset_button.grid(row=0, column=2, padx=5)
        
        # Preset buttons frame
        preset_frame = ttk.Frame(self.main_frame)
        preset_frame.pack(pady=10)
        
        ttk.Label(preset_frame, text="Quick Presets:").pack()
        
        # Preset buttons
        presets = [("1 min", 0, 1, 0), 
                  ("5 min", 0, 5, 0), 
                  ("10 min", 0, 10, 0),
                  ("15 min", 0, 15, 0),
                  ("30 min", 0, 30, 0)]
        
        for i, (text, h, m, s) in enumerate(presets):
            btn = ttk.Button(preset_frame, text=text, 
                           command=lambda h=h, m=m, s=s: self.set_preset(h, m, s))
            btn.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self.main_frame, textvariable=self.status_var).pack(pady=10)
    
    def set_preset(self, hours, minutes, seconds):
        self.hours_entry.delete(0, tk.END)
        self.hours_entry.insert(0, str(hours))
        self.minutes_entry.delete(0, tk.END)
        self.minutes_entry.insert(0, str(minutes))
        self.seconds_entry.delete(0, tk.END)
        self.seconds_entry.insert(0, str(seconds))
        self.update_display(hours * 3600 + minutes * 60 + seconds)
    
    def update_display(self, total_seconds):
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        self.time_display.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
    
    def start_timer(self):
        if self.running:
            return
            
        try:
            hours = int(self.hours_entry.get())
            minutes = int(self.minutes_entry.get())
            seconds = int(self.seconds_entry.get())
            self.remaining_time = hours * 3600 + minutes * 60 + seconds
            
            if self.remaining_time <= 0:
                messagebox.showwarning("Warning", "Please enter a valid time greater than 0")
                return
                
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.status_var.set("Timer running...")
            
            self.timer_thread = Thread(target=self.run_timer, daemon=True)
            self.timer_thread.start()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
    
    def run_timer(self):
        while self.remaining_time > 0 and self.running:
            self.update_display(self.remaining_time)
            time.sleep(1)
            self.remaining_time -= 1
            
        if self.remaining_time <= 0:
            self.root.after(0, self.timer_complete)
    
    def timer_complete(self):
        self.running = False
        self.update_display(0)
        self.status_var.set("Timer completed!")
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        
        if self.sound_var.get():
            for _ in range(3):  # Beep 3 times
                winsound.Beep(1000, 500)  # Frequency 1000Hz, duration 500ms
                time.sleep(0.3)
    
    def pause_timer(self):
        self.running = False
        self.pause_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)
        self.status_var.set("Timer paused")
    
    def reset_timer(self):
        self.running = False
        self.remaining_time = 0
        self.update_display(0)
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.status_var.set("Ready")
        
        # Reset input fields
        self.hours_entry.delete(0, tk.END)
        self.hours_entry.insert(0, "0")
        self.minutes_entry.delete(0, tk.END)
        self.minutes_entry.insert(0, "0")
        self.seconds_entry.delete(0, tk.END)
        self.seconds_entry.insert(0, "0")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
