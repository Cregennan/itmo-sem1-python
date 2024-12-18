import os.path
import sys
import asyncio
import aiohttp
import aiofiles
import uuid

async def downloadPromise(session: aiohttp.ClientSession):
    use_proxy = False # ЗАМЕНИТЬ НА СВОИ ДАННЫЕ ЕСЛИ НЕОБХОДИМО
    proxy_url = 'http://localhost:2081'

    random_id = uuid.uuid4()
    image_path = f'https://picsum.photos/seed/{random_id}/400/300'

    async with session.get(url=image_path, proxy=(proxy_url if use_proxy else None)) as response:
        if response.status == 200:
            raw_path = os.path.join('artifacts', 'task5_1', f'{random_id}.jpg')
            save_path = os.path.abspath(raw_path)
            print(f'File saved to {save_path}')
            async with aiofiles.open(save_path, mode='wb+') as file:
                await file.write(await response.read())
        else:
            print(f'Download error: {response.status}')

async def download(count: int):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[downloadPromise(session) for _ in range(count)])


async def main():
    if len(sys.argv) < 2:
        raise ValueError('There\'s no count argument')
    count = int(sys.argv[1])
    if count <= 0:
        raise ValueError('Count argument should be greater than 0')
    await download(count)

if __name__ == '__main__':
    asyncio.run(main())