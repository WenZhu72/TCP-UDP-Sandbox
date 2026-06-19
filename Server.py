import asyncio

HOST = "127.0.0.1"
PORT = 5000

async def handle_client(reader, writer):
    address = writer.get_extra_info("peername")
    print(f"[Connected] {address}")

    try:
        while True:
            data = await reader.readline()

            if not data:
                print(f"[Disconnected] {address}")
                break

            message = data.decode().strip()
            print(f"[Client {address}] {message}")

            if message.upper() == "PING":
                writer.write(b"PONG\n")
            else:
                writer.write(f"Server recieved: {message}\n".encode())

            await writer.drain()

    except ConnectionResetError:
        print(f"[RESET] {address}")

    finally:
        writer.close()
        await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)

    print(f"[SERVER STARTED] Listening on {HOST}:{PORT}")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())


