import subprocess
import time

if __name__ == '__main__':

    server_process = subprocess.Popen(['python', 'server/server.py'])
    time.sleep(1)


    client1_process = subprocess.Popen(['python', 'client/client.py', '1'])
    client2_process = subprocess.Popen(['python', 'client/client.py', '2'])

    try:

        time.sleep(300)
    except KeyboardInterrupt:
        print("Terminating processes manually")
    finally:
        server_process.terminate()
        client1_process.terminate()
        client2_process.terminate()
