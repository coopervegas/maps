

# async def get_url_data(url: str) -> tuple[str, str, list[dict]]:
# 	print(f"\n[INFO] Launching browser and navigating to: {url}")
# 	async with async_playwright() as p:
# 		browser = await p.chromium.launch(headless=False)
# 		context = await browser.new_context(
# 			geolocation={"latitude": 30.2672, "longitude": -97.7431},
# 			permissions=["geolocation"]
# 		)
# 		page = await context.new_page()
# 		await page.goto(url, wait_until='load', timeout=60000)

# 		print("[INFO] Page loaded, handling popups...")
# 		await dismiss_popups(page)
# 		print("[INFO] Finished handling popups")

# 		# Scroll to bottom to ensure all locations load
# 		for _ in range(10):
# 			await page.keyboard.press("End")
# 			await page.wait_for_timeout(1000)
# 		await page.wait_for_timeout(2000)

# 		title = await page.title()
# 		print(f"[INFO] Page title: {title}")

# 		# Pull all visible text
# 		raw_text = await page.evaluate("document.body.innerText")
# 		lines = raw_text.splitlines()

# 		results = []
# 		pending_address = None

# 		for line in lines:
# 			line = line.strip()

# 			if addrPat.match(line):
# 				pending_address = line
# 			elif phonePat.match(line) and pending_address:
# 				results.append({"address": pending_address, "phone": line})
# 				pending_address = None

# 		await browser.close()
# 		print(f"[INFO] Scraping complete. Found {len(results)} address/phone pairs.")
# 		return title, raw_text, results


# async def get_url_data(url: str) -> tuple[str, str, list[dict]]:
# 	print(f"\n[INFO] Launching browser and navigating to: {url}")
# 	async with async_playwright() as p:
# 		browser = await p.chromium.launch(headless=False)
# 		context = await browser.new_context(
# 			geolocation={"latitude": 30.2672, "longitude": -97.7431},
# 			permissions=["geolocation"]
# 		)
# 		page = await context.new_page()
# 		await page.goto(url, wait_until='load', timeout=60000)

# 		print("[INFO] Page loaded, handling popups...")
# 		await dismiss_popups(page)

# 		# Scroll the location container directly via JS
# 		# Scroll the widget containing locations
# 		widget = await page.locator('.locations-wrapper')
# 		for _ in range(15):
# 			await widget.evaluate("el => el.scrollBy(0, el.scrollHeight)")
# 			await page.wait_for_timeout(1000)



# 		results = []
# 		pending_address = None

# 		for line in lines:
# 			line = line.strip()
# 			if addrPat.match(line):
# 				pending_address = line
# 			elif phonePat.match(line) and pending_address:
# 				results.append({"address": pending_address, "phone": line})
# 				pending_address = None

# 		await browser.close()
# 		return title, raw_text, results


# async def get_url_data(url: str) -> tuple[str, str, list[dict]]:
# 	print(f"\n[INFO] Launching browser and navigating to: {url}")
# 	async with async_playwright() as p:
# 		browser = await p.chromium.launch(headless=False)
# 		context = await browser.new_context(
# 			geolocation={"latitude": 30.2672, "longitude": -97.7431},
# 			permissions=["geolocation"]
# 		)
# 		page = await context.new_page()
# 		await page.goto(url, wait_until='load', timeout=60000)

# 		print("[INFO] Page loaded, handling popups...")
# 		await dismiss_popups(page)
# 		print("[INFO] Finished handling popups")

# 		# Scroll to bottom of the widget to load all entries
# 		widget = page.locator('.locations-wrapper')
# 		for _ in range(30):
# 			await widget.evaluate("el => el.scrollBy(0, el.scrollHeight)")
# 			await page.wait_for_timeout(500)

# 		title = await page.title()
# 		print(f"[INFO] Page title: {title}")

# 		# Pull all visible text
# 		raw_text = await page.evaluate("document.body.innerText")
# 		lines = raw_text.splitlines()

# 		results = []
# 		pending_address = None

# 		for line in lines:
# 			line = line.strip()

# 			if addrPat.match(line):
# 				pending_address = line
# 			elif phonePat.match(line) and pending_address:
# 				results.append({"address": pending_address, "phone": line})
# 				pending_address = None

# 		await browser.close()
# 		print(f"[INFO] Scraping complete. Found {len(results)} address/phone pairs.")
# 		return title, raw_text, results


