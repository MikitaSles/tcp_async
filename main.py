import subprocess
import sys
import time
import os

def create_log_files():
    os.makedirs('client/logs', exist_ok=True)
    os.makedirs('server/logs', exist_ok=True)
    open('client/logs/client1.log', 'w').close()
    open('client/logs/client2.log', 'w').close()
    open('server/logs/server.log', 'w').close()

def start_server():
    return subprocess.Popen([sys.executable, 'server/server.py'])

def start_client(client_id):
    return subprocess.Popen([sys.executable, 'client/client.py', str(client_id)])

if __name__ == '__main__':
    create_log_files()

    server_process = start_server()
    client1_process = start_client(1)
    client2_process = start_client(2)

    try:
        time.sleep(300)
    finally:
        server_process.terminate()
        client1_process.terminate()
        client2_process.terminate()
