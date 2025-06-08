from datetime import datetime
import json

# will create timestamped filename.  Example: gattis_pois_1048am_june6.json
def create_fname(prefix: str, suffix: str) -> str:
	ts = (
		datetime.now().strftime("%I%M%p").lower() + "_" +
		datetime.now().strftime("%B").lower() +
		str(datetime.now().day)
	)
	return f"{prefix}{ts}{suffix}"



def write_json(fname: str, data: list[dict]) -> None:
	with open(fname, "w", encoding="utf-8") as f:
		json.dump(data, f, indent=2)
	print(f"[DONE] Saved {len(data)} records to {fname}")

