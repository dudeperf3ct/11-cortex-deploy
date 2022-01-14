import asyncio
import pprint
import time

import aiohttp


async def main():
    endpoint = "<endpoint>?input_text=ilikeyou"
    async with aiohttp.ClientSession() as session:
        for i in range(1, 10):
            async with session.post(endpoint) as resp:
                results = await resp.json()
                pprint.pprint(results)


start_time = time.time()
asyncio.run(main())
print("--- %s seconds ---" % (time.time() - start_time))
