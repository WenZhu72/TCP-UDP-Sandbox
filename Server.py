import asyncio

HOST = "127.0.0.1"
PORT = 5000

clients = {}

async def broadcast(message, sender_writer):
    for client_writer in list(clients.keys()):
        if client_writer != sender_writer:
            client_writer.write(message.encode())
            await client_writer.drain()

async def handle_client(reader, writer):
    address = writer.get_extra_info("peername")

    writer.write(b"Enter your username: ")
    await writer.drain()

    username_data = await reader.readline()
    username = username_data.decode().strip()

    clients[writer] = username
    print(f"[Connected] {username} from {address}")

    try:
        while True:
            data = await reader.readline()

            if not data:
                break

            message = data.decode().strip()
            print(f"[{username}] {message}")

            if message.lower() == "quit":
                break

            if message.upper() == "PING":
                writer.write(b"Pong\n")
                await writer.drain()
            else:
                await broadcast(f"[{username}] {message}\n", writer)

    finally:
        print(f"[DISCONNECTED] {address}")
        clients.pop(writer, None)
        writer.close()
        await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    print(f"[SERVER] Running on {HOST}:{PORT}")

    async with server:
        await server.serve_forever()

asyncio.run(main())

