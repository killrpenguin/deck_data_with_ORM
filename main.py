import asyncio
from driver_adapter import Driver_Adapter


async def task_coroutine(link: str):
    driver = await Driver_Adapter(link=link)
    return driver


async def main():
    with open("mxlinks", "r") as link_list:
        link_list = link_list.read().strip().split("\n")
        tasks = [asyncio.create_task(task_coroutine(link)) for link in link_list]
        for task in tasks:
            await task


asyncio.run(main())
