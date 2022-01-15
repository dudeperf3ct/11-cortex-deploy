import asyncio
import pprint
import time

import aiohttp


async def main():
    endpoint = "http://a1d29dbca812e47fbaa3efb9e54e06e9-5e4a92689ebef306.elb.us-east-1.amazonaws.com/sentiment"
    async with aiohttp.ClientSession() as session:
        for _ in range(1, 10):
            async with session.post(
                endpoint, json={"input_text": "i like you"}
            ) as resp:
                results = await resp.json()
                pprint.pprint(results)


start_time = time.time()
asyncio.run(main())
print("--- %s seconds ---" % (time.time() - start_time))
