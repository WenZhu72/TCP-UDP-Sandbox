import asyncio


HOST = "127.0.0.1"
PORT = 5000

async def send_message(writer):
    while True:
        message = await asyncio.to_thread(input, "> ")

        writer.write((message + "\n").encode())
        await writer.drain()

        if message.lower() == "quit":
            break

async def recieve_message(reader):
    while True:
        data = await reader.readline()

        if not data:
            print("[DISCONNECTED] Server closed the connection")
            break

        print(f"\n{data.decode().strip()}")
        print("> ", end="", flush=True)

async def main():

    writer = None

    try:
        reader, writer = await asyncio.open_connection(HOST, PORT)
        print("[CONNECTED] Connected to server")

        prompt = await reader.readuntil(b": ")
        username = await asyncio.to_thread(input, prompt.decode())

        writer.write((username + "\n").encode())
        await writer.drain()

        await asyncio.gather(
            send_message(writer),
            recieve_message(reader)
            )

    except ConnectionRefusedError:
        print("[ERROR] Could not connect to server. Is Server.py running")

    finally:
        if writer is not None:
            writer.close()
            await writer.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())

