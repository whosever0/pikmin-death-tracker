import dolphin_memory_engine as dme
import time
import twitchfunctions as tf
import asyncio

async def kill_chatter(deaths):
    await tf.kill_chatters(deaths)
    return



async def main():
    # Initialize twitch API 
    await tf.init()
    # Initialize connection to running Dolphin process
    dme.hook()

    # Read a 32-bit integer from a specific hex address
    red_address = 0x803D1ED4
    yellow_address = 0x803D1ED8
    blue_address = 0x803D1ED0
    total = 0
    prev_total = 0
    while True: 
        #TODO: This is only for GameCube Pikmin, Wii versions probably have different addresses.
        red_total = dme.read_word(red_address);
        blue_total = dme.read_word(yellow_address);
        yellow_total = dme.read_word(blue_address);
        print(f"Value at {hex(red_address)}: {(red_total)}")
        print(f"Value at {hex(yellow_address)}: {(yellow_total)}")
        print(f"Value at {hex(blue_address)}: {(blue_total)}")
        total = red_total + yellow_total + blue_total
        if total < prev_total:
           await kill_chatter(prev_total - total)
        prev_total = total
        time.sleep(5)

# Write a new value to that address
# dme.write_word(address, 100)

asyncio.run(main())