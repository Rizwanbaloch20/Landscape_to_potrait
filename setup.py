import subprocess
import sys

def install_requirements():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy"])

install_requirements()
