import tkinter as tk
import time
import pygame
import random

# Initialize pygame for playing sound
pygame.init()
pygame.mixer.init()

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer App")

        self.time_left = 0
        self.timer_running = False
        self.flashes_remaining = 0
        self.shots = 0  # Initialize the shots count

        # Timer label
        self.label = tk.Label(root, text="00:00:00", font=("Helvetica", 48), bg='white')
        self.label.pack()

        # Shots label
        self.shots_label = tk.Label(root, text=f"SHOTS TAKEN: {self.shots}", font=("Helvetica", 24))
        self.shots_label.pack()

        self.start_60_button = tk.Button(root, text="Power Hour", command=lambda: self.start_timer(60))
        self.start_60_button.pack()

        self.start_100_button = tk.Button(root, text="Start 100 Minute Timer", command=lambda: self.start_timer(100))
        self.start_100_button.pack()

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_timer)
        self.pause_button.pack()

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer)
        self.reset_button.pack()
        
        # Forward and Backward buttons
        self.forward_button = tk.Button(root, text="Backward (+1 min)", command=self.increment_timer)
        self.forward_button.pack()

        self.backward_button = tk.Button(root, text="Forward (-1 min)", command=self.decrement_timer)
        self.backward_button.pack()
        
        # Audio file paths
        self.first_shot_audio = r'C:\Users\biswa\Documents\total.mp3'
        self.last_shot_audio = r'C:\Users\biswa\Documents\total.mp3'
        self.random_audio_files = [
            r'C:\Users\biswa\Documents\Recording.mp3',
            r'C:\Users\biswa\Documents\shots.mp3',
            r'C:\Users\biswa\Documents\neverbackdown.mp3',
            r'C:\Users\biswa\Documents\MLGAirHornSound.mp3',
            # Add more if needed
        ]

    def increment_timer(self):
        if self.timer_running:
            self.time_left += 60  # Add 60 seconds
            mins, secs = divmod(self.time_left, 60)
            time_format = '{:02d}:{:02d}:{:02d}'.format(mins // 60, mins % 60, secs)
            self.label.config(text=time_format)

    def decrement_timer(self):
        if self.timer_running and self.time_left >= 60:
            self.time_left -= 60  # Subtract 60 seconds
            mins, secs = divmod(self.time_left, 60)
            time_format = '{:02d}:{:02d}:{:02d}'.format(mins // 60, mins % 60, secs)
            self.label.config(text=time_format)
            
    def start_timer(self, minutes):
        self.reset_timer()  # Reset the timer before starting
        self.max_time = minutes * 60  # Set the maximum time in seconds
        self.total_shots = minutes  # Total shots based on the timer duration
        self.time_left = self.max_time
        self.timer_running = True
        self.play_sound()  # Play sound at the beginning
        self.flashes_remaining = 3  # Initialize flash count
        self.flash_label()  # Start flashing at the beginning
        self.shots += 1  # Count the first shot
        self.shots_label.config(text=f"SHOTS TAKEN: {self.shots}")  # Update the shots label
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0 and self.timer_running:
            mins, secs = divmod(self.time_left, 60)
            time_format = '{:02d}:{:02d}:{:02d}'.format(mins // 60, mins % 60, secs)
            self.label.config(text=time_format)
            self.time_left -= 1
            if self.time_left % 60 == 0:  # Every 60 seconds
                self.play_sound()
                self.flashes_remaining = 3
                self.flash_label()
                self.shots += 1  # Increment the shots count
                self.shots_label.config(text=f"SHOTS TAKEN: {self.shots}")  # Update the shots label
            self.root.after(1000, self.update_timer)
        else:
            self.timer_running = False
            self.label.config(bg="white")

    def flash_label(self):
        if self.flashes_remaining > 0:
            current_color = self.label.cget("bg")
            next_color = "red" if current_color == "white" else "white"
            self.label.config(bg=next_color)
            self.flashes_remaining -= 1 if next_color == "white" else 0
            self.root.after(500, self.flash_label)
        else:
            self.label.config(bg="white")  # Explicitly reset to white after the flashes

    def pause_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.pause_button.config(text="Unpause")
        else:
            self.timer_running = True
            self.pause_button.config(text="Pause")
            self.update_timer()  # Restart the timer updating

    def reset_timer(self):
        self.timer_running = False
        self.time_left = 0
        self.flashes_remaining = 0
        self.shots = 0  # Reset the shots count
        self.label.config(text="00:00:00", bg='white')
        self.shots_label.config(text=f"SHOTS TAKEN: {self.shots}")  # Reset the shots label
        self.pause_button.config(text="Pause")  # Reset the pause button text


    def play_sound(self):
        try:
            # Debug print to check the current shot count and total shots
            print(f"Playing sound for shot number: {self.shots}, Total shots: {self.total_shots}")

            if self.shots == 0:
                # Play the first shot audio
                audio_file = self.first_shot_audio
            elif self.shots == self.total_shots:
                # Play the last shot audio
                audio_file = self.last_shot_audio
            else:
                # Play a random audio file
                audio_file = random.choice(self.random_audio_files)

            pygame.mixer.music.stop()  # Stop any currently playing music
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"Error playing sound from {audio_file}. File may be missing or incorrect format.")
            print(e)  # This will print the actual pygame error message



root = tk.Tk()
app = TimerApp(root)
root.mainloop()
