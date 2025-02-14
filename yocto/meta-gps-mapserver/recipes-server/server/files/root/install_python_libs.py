import subprocess
import sys

def check_and_install(package):
    try:
        __import__(package)
        print(f"{package} is already installed.")
    except ImportError:
        print(f"{package} not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

packages = ['pyserial', 'requests', 'flask']

for package in packages:
    check_and_install(package)

