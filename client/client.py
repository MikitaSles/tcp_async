import asyncio
import random
import logging
from datetime import datetime


async def send_ping(writer, client_id):
    request_counter = 0
    while True:
        await asyncio.sleep(random.uniform(0.3, 3.0))
        request = f"[{request_counter}] PING"
        now = datetime.now()
        request_date = now.strftime("%Y-%m-%d")
        request_time = now.strftime("%H:%M:%S.%f")[:-3]
        writer.write((request + '\n').encode())
        await writer.drain()
        log_message = f"{request_date};{request_time};{request};"
        logging.info(log_message)
        print(f"Client {client_id} sent: {request}")
        request_counter += 1


async def handle_responses(reader, client_id):
    while True:
        try:
            data = await reader.readuntil(b'\n')
            response = data.decode().strip()
            now = datetime.now()
            response_date = now.strftime("%Y-%m-%d")
            response_time = now.strftime("%H:%M:%S.%f")[:-3]
            if "keepalive" in response:
                log_message = f"{response_date};;{response_time};{response}"
            else:
                log_message = f";{response_time};{response}"
            logging.info(log_message)
            print(f"Client {client_id} received: {response}")
        except asyncio.IncompleteReadError:
            break


async def main(client_id, log_filename):
    logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(message)s')

    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    print(f"Client {client_id} connected to the server")

    await asyncio.gather(send_ping(writer, client_id), handle_responses(reader, client_id))


if __name__ == '__main__':
    import sys

    client_id = int(sys.argv[1])
    log_filename = f'client/logs/client{client_id}.log'
    try:
        asyncio.run(main(client_id, log_filename))
    except KeyboardInterrupt:
        print(f"Client {client_id} stopped manually")
