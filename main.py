from driver_adapter import Driver_Adapter
import asyncio
import traceback

VALID_STATUSES = [200, 301, 302, 307, 404]


async def Create_Adapter(link) -> object:
    adapter = Driver_Adapter(link=link)
    await adapter.get_page()
    return adapter


async def task_coroutine(link):
    try:
        async with Driver_Adapter(link) as dp:
            await Create_Adapter(link=link)
            if dp.page_status_code in VALID_STATUSES:
                print(f"Response: {dp.page_status_code}\nFrom: {link}")
    except Exception as e:
        print(f"Exception: {e}")
        print(f"{traceback.format_exc()}")


async def main_scraper():
    with open("mxlinks", "r") as link_list:
        link_list = link_list.read().strip().split("\n")
        tasks = [asyncio.create_task(task_coroutine(link)) for link in link_list]
        for task in tasks:
            await asyncio.gather(task)
        await asyncio.sleep(0)

asyncio.run(main_scraper())