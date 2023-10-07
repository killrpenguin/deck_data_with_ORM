from driver_adapter import Driver_Adapter
import asyncio

VALID_STATUSES = [200, 301, 302, 307, 404]


async def task_coroutine(link):
    try:
        async with Driver_Adapter(link) as dp:
            await dp.get_page
            if dp.page_status_code in VALID_STATUSES:
                print(f"Response: {dp.page_status_code}\nFrom: {link}")
    except Exception as e:
        print(f"Exception: {e}")


async def main_scraper():
    with open("mxlinks", "r") as link_list:
        link_list = link_list.read().strip().split("\n")
        tasks = [asyncio.create_task(task_coroutine(link)) for link in link_list]
        for task in tasks:
            await asyncio.gather(task)
        await asyncio.sleep(0)

asyncio.run(main_scraper())