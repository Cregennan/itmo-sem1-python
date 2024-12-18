import asyncio
import itertools
import os
import re
import uuid
import aiofiles
import aiocsv

from playwright.async_api import Browser, async_playwright, Playwright, ElementHandle, ViewportSize
from urllib.parse import urlparse


DataRow = dict[str, int|str]

def construct_link(page_url: str, link: str):
    parse_result = urlparse(page_url)
    if link.startswith('/'):
        link = link[1:]
    return f'{parse_result.scheme}://{parse_result.netloc}/{link}'

async def parse_yandex(browser: Browser, count: int) -> list[DataRow]:
    page = await browser.new_page()
    await page.goto('https://realty.yandex.ru/')
    await page.is_visible('[data-test="IndexPageSnippetsTitle"] a')
    raw_link = await (await page.query_selector_all('[data-test="IndexPageSnippetsTitle"] a'))[1].get_attribute('href')
    link = construct_link(page.url, raw_link)
    await page.goto(link)
    items = await page.query_selector_all('[data-test="OffersSerpItem"]')

    async def parse_each(elements: list[ElementHandle]) -> list[DataRow]:
        result = []
        for element in elements:
            url_raw = await (await element.query_selector('.OffersSerpItem__titleLink')).get_attribute('href')
            uid = int(re.sub('[^0-9,]','', url_raw))
            name_raw = await (await element.query_selector('.OffersSerpItem__titleLink span span')).inner_html()
            name_parts = name_raw.split('·')
            area_raw = re.sub('[^0-9,]', '', name_parts[0])
            area_raw = area_raw.replace(',', '.')
            area = float(area_raw)
            name = re.sub('[^0-9,]', '', name_parts[0]).strip()
            location = await (await element.query_selector('.OffersSerpItem__location a')).inner_text()
            price_raw = await (await element.query_selector('.OffersSerpItem__price')).inner_text()
            price_raw = re.sub('[^0-9,.]','', price_raw)
            price_raw = price_raw.replace(',', '.')
            price = float(price_raw)
            result.append({
                'location': location,
                'uid': uid,
                'area': area,
                'name': name,
                'price': price,
                'source': 'yandex'
            })
        return result
    return await parse_each(items)


async def parse_avito(browser: Browser, count: int) -> list[DataRow]:
    return []


async def parse_cian(playwright: Playwright, browser: Browser, count: int) -> list[DataRow]:
    device = playwright.devices['iPhone 13']
    context = await browser.new_context(**device)
    page = await context.new_page()
    #await page.set_viewport_size(ViewportSize(width=400, height=600))
    await page.goto('https://www.cian.ru/kupit-kvartiru/')
    await page.is_visible('[data-name="CardContainer"]')
    await page.is_visible('[data-name="СloseBtn"]')
    await page.click('[data-name="СloseBtn"]')
    items = await page.query_selector_all('[data-name="CardContainer"]')
    async def foreach(elements: list[ElementHandle]) -> list[DataRow]:
        result = []
        for element in elements:
            price_raw = await (await element.query_selector('[data-testid="Price"]')).inner_text()
            if price_raw.strip() == '':
                continue
            price_raw = re.sub('[^0-9,]', '', price_raw)
            price = float(price_raw.replace(',', '.'))
            location = await (await element.query_selector('[data-name="Address"]')).inner_text()
            name_raw = await element.query_selector('[data-name="Features"]')
            name_parts = (await name_raw.inner_text()).split('•')
            name = name_parts[0].strip()
            area = float(re.sub('[^0-9,]', '', price_raw).replace(',', '.'))
            link_raw = await name_raw.get_attribute('href')
            link = construct_link(page.url, link_raw)
            uid = int(re.sub('[^0-9]', '', link))
            result.append({
                'location': location,
                'uid': uid,
                'area': area,
                'name': name,
                'price': price,
                'source': 'cian'
            })
        return result

    return await foreach(items)


async def begin(pw: Playwright, count: int) -> list[DataRow]:
    chromium = pw.chromium
    browser = await chromium.launch(headless=False)

    yandex = parse_yandex(browser, count)
    avito = parse_avito(browser, count)
    cian = parse_cian(pw, browser, count)
    results_raw = await asyncio.gather(*[yandex, avito, cian])
    return list(itertools.chain.from_iterable(results_raw))


async def main():
    async with async_playwright() as pw:
        result = await begin(pw, 10)
        filename = f'{uuid.uuid4()}.csv'
        filepath = os.path.join('artifacts', 'task5_2', filename)
        async with aiofiles.open(filepath, 'w+') as file:
            writer = aiocsv.AsyncDictWriter(file, ['location','uid','area','name', 'price','source'], delimiter=',')
            await writer.writeheader()
            await writer.writerows(result)


if __name__ == '__main__':
    asyncio.run(main())





