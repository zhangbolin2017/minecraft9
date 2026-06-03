import time
import threading
import subprocess

def run_game():
    subprocess.run(["python", "source3d/main.py"])

t = threading.Thread(target=run_game)
t.daemon = True
t.start()

time.sleep(5)
with open("source3d/world_save.json", "r") as f:
    print(f.read())
