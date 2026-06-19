import asyncio
from csv import writer
from email import message
from urllib import response

HOST = "127.0.0.1"
PORT = 5000

async def main():
    try:
        reader, writer = await asyncio.open_connection(HOST, PORT)
        print("[CLIENT] Connected to server")

        while True:
            message = input("> ")

            writer.write((message + "\n").encode())
            await writer.drain()

            response = await reader.readline()
            print("[SERVER]", response.decode().strip())

            if message.lower() == "quit":
                break

    except ConnectionRefusedError:
        print("[ERROR] Could not connect to server. Is my server.py running")

    finally:
        writer.close()
        await writer.wait_closed()

asyncio.run(main())