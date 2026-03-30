from core.session_manager import SessionManager
import asyncio
from core.config import Config


async def main():
    session = SessionManager()
    
    config = Config()
    auth = config.auth()
    

    context = await session.get_browser_context()
    page = await context.new_page()

    await page.goto(auth["origin_url"])
    # await page.click("text=Generate Report")
    await page.wait_for_event("close")

    await session.close()




if __name__ == "__main__":
    asyncio.run(main())
