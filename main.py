import os
import time
import pickle
import matplotlib.pyplot as plt
from array import array
import threading
import time
from pynput import keyboard
import os
import pygame


#@title Define class and run CLI
FPS = 30 #@param {type:"integer"}
class FrameRecorder:
    def __init__(self):
        self._recordings = []
        self.locked = False

    @property
    def recordings(self):
        return self._recordings


    @recordings.setter
    def recordings(self, value):
        self._recordings = value

    def load_audio(self, file_path):
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)


    def record(self, duration):
        if self.locked:
            return
        
        # play audio on record, if an audio file exists
        file_path = "D:\\Users\\geosp\\Documents\\Code\\PY\\Projects\\AnimationTools\\MOTD.mp3"
        audio_exists = False
        if os.path.exists(file_path):
            print("Will play audio file when recording.")
            audio_exists = True
            self.load_audio(file_path)
        else:
            print("No audio file found, will nt play audio when recording.")

        keyframes = []

        # Define the callback function for capturing keyframes
        def on_press(key):
            keyframes.append(time.time())

        input("Press Enter to start recording...")
        start_time = time.time()
        if audio_exists:
            pygame.mixer.music.play()
        end_time = start_time + duration

        # Start capturing keyframes
        with keyboard.Listener(on_press=on_press) as listener:
            while time.time() < end_time:
                time.sleep(0.01)

        if audio_exists:
            pygame.mixer.music.stop()
        
        # Calculate relative timestamps
        keyframes = [ts - start_time for ts in keyframes]
        self.recordings.append(keyframes)

        input("Recording completed. Press enter to clear input/continue.")
        if (len(keyframes) < 20):
            print("Recorded timestamps:")
            for i, timestamp in enumerate(keyframes):
                print(f"[i{i + 1}: {timestamp:.2f}s], ", end="")
            print()

    def graph(self):
      print(f"Graphing recordings in {FPS} FPS")
      num_recordings = len(self.recordings)

      plt.figure()

      for i, keyframes in enumerate(self.recordings):
          frame_nums = [int(timestamp * FPS) for timestamp in keyframes]

          if num_recordings > 1:
            y_values = [i * (2 / (num_recordings - 1)) - 1 for _ in frame_nums]
          else:
            y_values = [0] * len(frame_nums)
          plt.plot(frame_nums, y_values, marker='o', label=f"Recording {i + 1}")

          for frame_num, y_value, timestamp in zip(frame_nums, y_values, keyframes):
              plt.annotate(frame_num, (frame_num, y_value), xytext=(5, -10), textcoords='offset points')

      plt.xlabel("Frame number")
      plt.ylabel("Recording")
      plt.title("Recordings Graph")
      plt.legend()
      plt.ion()
      plt.show()


    def print(self):
        print(f"[{FPS} FPS]")
        frame_spacing = 1 / FPS
        for i, keyframes in enumerate(self.recordings):
            print(f"Recording {i + 1}:")
            for frame_num, timestamp in enumerate(keyframes):
                frame_time = frame_num * frame_spacing
                print(f"Keyframe {frame_num + 1} (frame {int(timestamp * FPS)}): {timestamp} (Time: {frame_time:.2f}s)")
            print()


    def convert(self):
        lock = input(f"[{FPS} FPS] You are about to lock the FPS falue. Are you sure? (y), n: ")
        if ('n' in lock):
            return

        if not self.recordings:
            print("No recordings available.")
            return

        converted_string = ""
        lockedRecordings = []
        # for each recording
        for i, keyframes in enumerate(self.recordings):
            # construct the converted string for that specific recording
            converted_string += f"\nRecording {i+1}:\n"
            frame_nums = [int(timestamp * float(FPS)) for timestamp in keyframes]
            converted_string += ", ".join([f"{frame_num}:(0)" for frame_num in frame_nums])
            # append converted string to list
            lockedRecordings.append(converted_string)
        if (len(converted_string) > 200):
            # if the converted strng is beefy then save to a txt file
            filename = str(time.time()).replace('.', "")
            filename =  f"[{filename}]Convert.txt"
            print(f"Converted string very long, saving to file: {filename}")
            with open(os.path.join(os.getcwd(), filename), 'w') as fp:
                fp.write(converted_string)
        else:
            print(converted_string)
        
        
    def save(self, filepath):
        with open(filepath, "wb") as file:
            pickle.dump(self.recordings, file)

        print(f"Recordings saved to {filepath}")

    def load(self, filepath):
        with open(filepath, "rb") as file:
            self.recordings = pickle.load(file) 

    def remove_recording(self):
          if not self.recordings:
              print("No recordings available.")
              return

          print("Select a recording to remove:")
          for i, keyframes in enumerate(self.recordings):
              print(f"Recording {i + 1}")

          while True:
              choice = input("Enter the recording number to remove or 'q' to cancel: ")
              if choice == 'q':
                  return

              try:
                  recording_idx = int(choice) - 1
                  if 0 <= recording_idx < len(self.recordings):
                      removed_recording = self.recordings.pop(recording_idx)
                      print(f"Recording {recording_idx + 1} removed.")
                      break
                  else:
                      print("Invalid recording number. Please try again.")
              except ValueError:
                  print("Invalid input. Please try again.")


    def __str__(self):
        num_recordings = len(self.recordings)
        recording_info = [f"Recording {i + 1}: {len(keyframes)} keyframes" for i, keyframes in enumerate(self.recordings)]
        return f"FrameRecorder with {num_recordings} recordings\n" + "\n".join(recording_info)


    def cli(self):
        while True:
            choice = input("Enter 'r' to record, 'g' to graph, 'c' to convert, 'rm' to remove, or 'q' to quit: ")
            if choice == 'r':
                # Get the recording duration from the user
                duration = int(input("Enter the recording duration in seconds: "))
                self.record(duration)
            elif choice == 'g':
                self.graph()
            elif choice == 's':
                # Get the filepath from the user
                filepath = input("Enter the filepath to save the recordings: ")
                self.save(filepath)
            elif choice == 'l':
                # Get the filepath from the user
                filepath = input("Enter the filepath to load the recordings: ")
                self.load(filepath)
            elif choice == 'c':
                self.convert()
            elif choice == 'rm':
              self.remove_recording()
            elif choice == 'q':
                break
            else:
                print("Invalid choice. Please try again.")



recorder = FrameRecorder()
recorder.cli()



