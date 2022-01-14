import asyncio
import pprint
import time

import aiohttp


async def main():
    endpoint = "http://aef8794492ec94b0bbec106d83bca5a8-fd4d5795eed99b6d.elb.us-east-1.amazonaws.com/sentiment/classify?input_text=ilikeyou"
    async with aiohttp.ClientSession() as session:
        for i in range(1, 10):
            async with session.post(endpoint) as resp:
                results = await resp.json()
                pprint.pprint(results)


start_time = time.time()
asyncio.run(main())
print("--- %s seconds ---" % (time.time() - start_time))
