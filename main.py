# main.py

import asyncio, re, os
from playwright.async_api import async_playwright, Page

# Regex patterns
addrPat = re.compile(r'^.+?,\s*.+?,\s*TX,\s*\d{5}(?:,\s*US)?$')
phonePat = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')

#######################################################################



#######################################################################
async def dismiss_popups(page: Page):
	# Handle cookie banner
	try:
		await page.locator("button:has-text('Accept')").click(timeout=3000)
		await page.wait_for_load_state('load')
		await page.wait_for_timeout(2000)
	except:
		pass

	# Handle location popup variations
	try:
		await page.locator("button:has-text('Allow This Time')").click(timeout=3000)
		await page.wait_for_timeout(2000)
	except:
		try:
			await page.locator("button:has-text('Allow')").click(timeout=3000)
			await page.wait_for_timeout(1000)
		except:
			try:
				await page.locator("button:has-text('Use My Location')").click(timeout=3000)
				await page.wait_for_timeout(1000)
			except:
				pass


#######################################################################
async def get_url_data(url: str) -> list[dict]:
	print(f"\n[INFO] Launching browser and navigating to: {url}")
	async with async_playwright() as p:
		context = await p.chromium.launch_persistent_context(
			"playwright_profile",
			headless=False,
			viewport={"width": 1600, "height": 1200},
			user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
		)
		page = context.pages[0] if context.pages else await context.new_page()
		await page.goto(url, wait_until='load', timeout=60000)

		print("[INFO] Page loaded, handling popups...")
		await dismiss_popups(page)
		print("[INFO] Finished handling popups")


		raw_text = await page.evaluate("document.body.innerText")
		lines = raw_text.splitlines()

		results = []
		pending_address = None

		for line in lines:
			line = line.strip()
			if addrPat.match(line):
				pending_address = line
			elif phonePat.match(line) and pending_address:
				results.append({"address": pending_address, "phone": line})
				pending_address = None

		await context.close()
		print(f"[INFO] Scraping complete. Found {len(results)} address/phone pairs.")
		return results

#######################################################################
def main():
	os.system('cls')  # Clear screen on Windows
	url = "https://mrgattispizza.com/locations/"
	results = asyncio.run(get_url_data(url))

	print(f"\n{url}")
	print("Locations:")

	def prt_location(street, city, state, phone, w1, w2, w3, w4):
		def fmt(s, w): return s.strip()[:w].ljust(w)
		print(fmt(street, w1) + ' ' +	fmt(city, w2) + ' ' +	fmt(state, w3) + ' ' +	fmt(phone, w4))		


	for i, entry in enumerate(results):
		addr = re.sub(r'\b(Suite|STE|#)\s*\w+\b', '', entry['address'], flags=re.IGNORECASE)
		addr = re.sub(r'\(.*?\)', '', addr)
		addr_parts = [part.strip() for part in addr.split(',') if part.strip()]

		street = addr_parts[0] if len(addr_parts) > 0 else ''
		city = addr_parts[1] if len(addr_parts) > 1 else ''
		state = addr_parts[2].split()[0] if len(addr_parts) > 2 else ''
		phone = entry['phone'].strip()

		prt_location(street, city, state, phone, 25, 15, 2, 15)
	print(f"\nTotal locations: {len(results)}\n")


#######################################################################
if __name__ == "__main__":
	main()
