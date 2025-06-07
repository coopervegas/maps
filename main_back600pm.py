# main.py

import asyncio, re, os
from playwright.async_api import async_playwright, Page
import json
from datetime import datetime
import requests
import time

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

		await dismiss_popups(page)

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
def fetch_gattis_locations(apiKey: str, region: str = "Texas") -> list:
	"""
	Fetches all Gatti's Pizza locations in the specified region using Google Places API.
	
	Args:
		apiKey (str): Your Google Places API key.
		region (str): Geographic area to search in (default is 'Texas').

	Returns:
		list: List of dicts with name, address, and location coordinates.
	"""
	query = f"Gatti's Pizza in {region}"
	url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={apiKey}"

	results = []
	resp = requests.get(url)
	data = resp.json()
	results.extend(data.get("results", []))

	while "next_page_token" in data:
		time.sleep(2)  # Required delay
		next_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken={data['next_page_token']}&key={apiKey}"
		resp = requests.get(next_url)
		data = resp.json()
		results.extend(data.get("results", []))

	# Extract relevant info
	locations = []
	for place in results:
		locations.append({
			"name": place.get("name"),
			"address": place.get("formatted_address"),
			"lat": place.get("geometry", {}).get("location", {}).get("lat"),
			"lng": place.get("geometry", {}).get("location", {}).get("lng")
		})
	
	return locations



#######################################################################
def main():
	os.system('cls')  # Clear screen on Windows



	apiKey = "AIzaSyD19HD2hVPe7UnqvErvBtidEwv9f3l3vb0"
	#locations = fetch_gattis_locations(apiKey)

	states = ["Texas", "Kentucky", "Louisiana", "Indiana", "Alabama", "Tennessee", "Ohio", "Oklahoma", "Arkansas", "Missouri"]
	locations = []
	for st in states:
		locs = fetch_gattis_locations(apiKey, region=st)
		locations.extend(locs)

	# Generate filename
	ts = datetime.now().strftime("%d%m%y_%H%M")
	fname = f"googleapi{ts}.json"

	# Save to JSON file
	with open(fname, "w", encoding="utf-8") as f:
		json.dump(locations, f, indent=2)

	print(f"Saved {len(locations)} locations to {fname}")

	for loc in locations:
		name = loc["name"]
		addr = loc["address"].split(", United States")[0]  # Clean off the ending
		print(f"{name} — {addr}")
	print(f"\nTotal locations: {len(locations)}\n")




	exit










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
