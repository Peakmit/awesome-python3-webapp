import asyncio
from models import User, Blog, Comment
import orm

loop = asyncio.get_event_loop()
async def test():
    await orm.create_pool(user='root', password='123456', db='awesome', loop=loop)

    u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')

    await u.update()

loop.run_until_complete(test())