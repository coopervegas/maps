# main.py

import asyncio
import re
from playwright.async_api import async_playwright, Page

# Regex patterns
addrPat = re.compile(r'[\w\d\s.#\-]+,\s*[\w\s]+,\s*TX,\s*\d{5}')
phonePat = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')

async def dismiss_popups(page: Page):
	# Handle cookie banner
	try:
		await page.locator("button:has-text('Accept')").click(timeout=3000)
		await page.wait_for_load_state('load')
		await page.wait_for_timeout(2000)
	except:
		pass

	# Handle location popup
	try:
		await page.locator("button:has-text('Allow')").click(timeout=3000)
		await page.wait_for_timeout(1000)
	except:
		try:
			await page.locator("button:has-text('Use My Location')").click(timeout=3000)
			await page.wait_for_timeout(1000)
		except:
			pass


async def get_url_data(url: str) -> tuple[str, str, list[str]]:
	print(f"\n[INFO] Launching browser and navigating to: {url}")
	async with async_playwright() as p:
		browser = await p.chromium.launch(headless=False)
		context = await browser.new_context(
			geolocation={"latitude": 30.2672, "longitude": -97.7431},
			permissions=["geolocation"]
		)
		page = await context.new_page()
		await page.goto(url, wait_until='load', timeout=60000)

		print("[INFO] Page loaded, handling popups...")
		await dismiss_popups(page)
		print("[INFO] Finished handling popups")

		title = await page.title()
		print(f"[INFO] Page title: {title}")

		# Pull full page text
		raw_text = await page.evaluate("document.body.innerText")
		lines = raw_text.splitlines()

		# Ordered address extraction
		addresses = []
		seen = set()
		for line in lines:
			line = line.strip()
			if addrPat.match(line) and line not in seen:
				seen.add(line)
				addresses.append(line)

		await browser.close()
		print(f"[INFO] Scraping complete. Found {len(addresses)} addresses.")
		return title, raw_text, addresses




def main():
	url = "https://mrgattispizza.com/locations/"
	title, rawText, addresses = asyncio.run(get_url_data(url))

	phones = set(phonePat.findall(rawText))

	print("Title:", title)
	print("\nPhone Numbers:")
	for p in phones:
		print("-", p)

	print("\nAddresses:")
	for a in addresses:
		print("-", a)

if __name__ == "__main__":
	main()
