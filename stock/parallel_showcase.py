from threading import Thread
import datetime
import asyncio
import aiohttp


async def long_running_task(id):
    ''' Asynchronous request to a given url '''
    print(f"Fetching stock {id}...")
    # simulate call to external API
    await asyncio.sleep(5)
    print(f"Fetching stock {id} done!")
    
    return {id: f"Stock {id}"}, 200

async def fetch_all():
    ''' Fetch all stock summaries '''
    tasks = []
    for id in [1, 2, -3, -4, 5]:
        tasks.append(long_running_task(id))
    
    return await asyncio.gather(*tasks)

start_time = datetime.datetime.now()
    
results = asyncio.run(fetch_all())
print(results)


end_time = datetime.datetime.now()

print(f"Time taken: {end_time - start_time}")