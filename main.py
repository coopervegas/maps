# main.py

import asyncio, re, os
from playwright.async_api import async_playwright, Page
import json, glob, requests, time
from datetime import datetime
from dotenv import load_dotenv
from typing import List

from utils import create_fname, write_json


# Regex patterns
addrPat = re.compile(r'^.+?,\s*.+?,\s*TX,\s*\d{5}(?:,\s*US)?$')
phonePat = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')

#######################################################################
#######################################################################

def parse_POIs(text: str) -> list[dict]:

	lines = [line.strip() for line in text.splitlines() if line.strip()]
	results = []

	i = 0
	while i < len(lines):
		if re.match(r'^\d+\s*Mr Gatti\'s|GattiTown', lines[i]):
			name = lines[i].lstrip("0123456789. ").strip()
			addr = ""
			phone = ""
			j = i + 1

			while j < len(lines):
				if re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', lines[j]):
					phone = lines[j]
					break
				elif re.search(r'\d{5}', lines[j]):
					addr = lines[j]
				j += 1

			if name and addr and phone:
				results.append({
					"name": name,
					"address": addr,
					"phone": phone
				})
			i = j + 1
		else:
			i += 1

	return results


async def getPOIs(url: str, searchTerms: List[str], geocodes: list, limit: int = None) -> list[dict]:


	all_results = []

	async with async_playwright() as p:
		browser = await p.chromium.launch(headless=True)

		# count = how many iterations do we want to do, for testing
		count = 0 
		for entry in geocodes:
			state = entry["state"]
			for city in entry["cities"]:
				if limit is not None and count >= limit:
					return all_results		
				count += 1		

				city_name = city["city"]
				lat = city["lat"]
				lng = city["lng"]

				print(f"[INFO] Faking location: {city_name}, {state} ({lat}, {lng})")

				context = await browser.new_context(
					geolocation={"latitude": lat, "longitude": lng},
					permissions=["geolocation"]
				)
				page = await context.new_page()
				await page.goto(url, wait_until="load")
				await asyncio.sleep(2)

				# Scroll to load locations
				for _ in range(3):
					await page.evaluate("""
						const el = document.querySelector("#storelocator-leftcolumn");
						if (el) el.scrollTo(0, el.scrollHeight);
					""")
					await asyncio.sleep(0.5)

				# Extract innerText
				el = await page.query_selector("#storelocator-leftcolumn")
				text = await page.evaluate("(el => el ? el.innerText : '')", el)

				parsed = parse_POIs(text)

				for item in parsed:
					all_results.append({
						"name": item.get("name", ""),
						"address": item.get("address", ""),
						"phone": item.get("phone", ""),
						"city": city_name,
						"state": state
					})


				for item in parsed:
					print("--------")
					for k, v in item.items():
						print(f"{k}: {v}")



				await context.close()

		await browser.close()

	return all_results



#######################################################################
#######################################################################

# Clear screen on Windows
os.system('cls')

# Get my API KEY
# not using it right now
load_dotenv()
APIKEY = os.getenv("GOOGLE_API_KEY")

# Load geocodes.json
with open("geocodes.json", "r", encoding="utf-8") as f:
	geo_data = json.load(f)

# Your search terms & url
terms = ["Gatti's Pizza", "GattiTown"]
url = "https://mrgattispizza.com/locations/"

# Run the scraper (limit = how many to parse, for testing.)
results = asyncio.run(getPOIs(url, terms, geo_data, limit=2))

# output our results to a json file
# will create timestamped filename.  Example: gattis_pois_1048am_june6.json
write_json(create_fname("gattis_pois_", ".json"), results)


exit()


















states = ["Texas", "Kentucky", "Louisiana", "Indiana", "Alabama", "Tennessee", "Ohio", "Oklahoma", "Arkansas", "Missouri"]
search_terms = [f"Gatti's Pizza", f"Gattitown"]
getPOIs(APIKEY, states, search_terms)













# Find the most recent googleapi*.json file
json_files = glob.glob("googleapi*.json")
latest_file = max(json_files, key=os.path.getmtime)

with open(latest_file, "r") as f:
	locations = json.load(f)

results = []
found_count = 0
missing_count = 0

for i, loc in enumerate(locations):
	lat = loc["lat"]
	lng = loc["lng"]
	found = gmaps("gatti", 100, lat, lng, APIKEY)
	status = "found" if found else "missing"
	if found:
		found_count += 1
	else:
		missing_count += 1
	results.append({
		"index": i,
		"lat": lat,
		"lng": lng,
		"status": status
	})
	print(f"{i}:\t {lat}, {lng}, {'✅' if found else '❌'} {status}")

# Write output file
timestamp = datetime.now().strftime("%d%m%y_%H%M")
out_file = f"googlemaps_{timestamp}.json"
with open(out_file, "w") as f:
	json.dump(results, f, indent=2)

# Summary
total = found_count + missing_count
print("\nSummary:")
print(f"✅ Found:   {found_count}")
print(f"❌ Missing: {missing_count}")
print(f"📦 Total:   {total}")



print("==============")
print("END OF PROGRAM")
print("==============")