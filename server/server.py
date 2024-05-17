import asyncio
import random
import logging
from datetime import datetime

clients = []
request_counter = 0
response_counter = 0

logging.basicConfig(filename='server/logs/server.log', level=logging.INFO, format='%(message)s', encoding='utf-8')

async def handle_client(reader, writer):
    global request_counter, response_counter
    client_id = len(clients) + 1
    clients.append(writer)
    addr = writer.get_extra_info('peername')

    print(f"Client {client_id} connected from {addr}")

    try:
        while True:
            data = await reader.readuntil(b'\n')
            request = data.decode().strip()
            now = datetime.now()
            request_date = now.strftime("%Y-%m-%d")
            request_time = now.strftime("%H:%M:%S.%f")[:-3]
            print(f"Received {request} from {addr}")

            if random.random() > 0.1:  # 90% шанс ответа
                await asyncio.sleep(random.uniform(0.1, 1.0))
                response = f"[{response_counter}/{request_counter}] PONG ({client_id})"
                response_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                writer.write((response + "\n").encode())
                await writer.drain()
                logging.info(f"{request_date};{request_time};{request};{response_time};{response}")
                response_counter += 1
            else:
                logging.info(f"{request_date};{request_time};{request};(проигнорировано);(проигнорировано)")

            request_counter += 1

    except asyncio.IncompleteReadError:
        pass
    finally:
        print(f"Client {client_id} disconnected")
        clients.remove(writer)
        writer.close()
        await writer.wait_closed()

async def keepalive():
    global response_counter
    while True:
        await asyncio.sleep(5)
        for writer in clients:
            response = f"[{response_counter}] keepalive"
            writer.write((response + "\n").encode())
            await writer.drain()
            response_counter += 1

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()
    print(f"Serving on {addr}")

    await asyncio.gather(server.serve_forever(), keepalive())

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped manually")
