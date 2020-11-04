import asyncio

from items_worker import main

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))

    print(" [*] Waiting for messages...")
    loop.run_forever()
