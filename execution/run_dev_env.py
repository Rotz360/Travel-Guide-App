"""
Script to start the development environment (Backend + Frontend).
"""
import os
import subprocess
import sys
import time
import socket
from concurrent.futures import ThreadPoolExecutor

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def run_backend():
    print("Starting Backend...")
    os.chdir('backend')
    # Using python main.py as per instructions
    subprocess.run([sys.executable, "main.py"], check=True)

def run_frontend():
    print("Starting Frontend...")
    os.chdir('frontend')
    subprocess.run(["npm", "run", "dev"], check=True, shell=True)

def main():
    # 1. Check Ports
    if is_port_in_use(8001) or is_port_in_use(3000):
        print("Error: Ports 8001 or 3000 are already in use.")
        return 1

    # 2. Start Servers in Parallel
    print("Starting Development Environment...")
    
    # Note: In a real script we'd want to manage these subprocesses better (e.g. killing them on exit).
    # For this simple implementation, we rely on the user to kill the terminal.
    # However, since this blocks, we can't easily run both in this simple script without threading.
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(run_backend)
        executor.submit(run_frontend)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping environment...")
