import sys
import requests
import json
from datetime import datetime


def scrape():
    base_url = "https://investor.cpr.ca/key-metrics/default.aspx"

    # Maintain a session for cookies etc
    s = requests.Session()

    # Call base URL with session (& get back updated session)
    log_this(f"GETting base URL {base_url}")
    (get_success, get_message, s, get_response) = get(s, base_url)

    if not get_success:
        log_this(f"ERROR: {get_message}")
        sys.exit(0)

    # We can ignore the response and call our first POST request
    year_url = "https://investor.cpr.ca/Services/ContentAssetService.svc/GetContentAssetYearList"
    year_payload = {
        "serviceDto": {
            "ViewType": "2",
            "ViewDate": "",
            "RevisionNumber": "1",
            "LanguageId": "1",
            "Signature": "",
            "TagList": ["time"],
        },
        "assetType": "Weekly Metrics - Download",
    }

    log_this(f"POSTing to {year_url} with payload")
    (year_success, year_message, s, year_response) = post(s, year_url, year_payload)

    if not year_success:
        log_this(f"ERROR: {year_message}")
        sys.exit(0)

    year_object = json.loads(year_response.text)
    start_year = year_object["GetContentAssetYearListResult"][0]
    log_this(f"Preparing to call data beginning {start_year}")

    # Now we have everything we need to get the file link!
    button_url = (
        "https://investor.cpr.ca/Services/ContentAssetService.svc/GetContentAssetList"
    )
    # Change the true to True in this. Python and JSON do it differently.
    button_payload = {
        "serviceDto": {
            "ViewType": "2",
            "ViewDate": "",
            "RevisionNumber": "1",
            "LanguageId": "1",
            "Signature": "",
            "ItemCount": 1,
            "StartIndex": 0,
            "TagList": ["railcar"],
            "IncludeTags": True,
        },
        "assetType": "Weekly Metrics - Download",
        "year": start_year,
    }
    # Hilariously, when we conver button_payload to JSON, the True will become true again.

    log_this(f"POSTing to {button_url} with payload")
    (button_success, button_message, s, button_response) = post(
        s, button_url, button_payload
    )

    if not button_success:
        log_this(f"ERROR: {button_message}")
        sys.exit(0)

    button_object = json.loads(button_response.text)
    file_url = button_object["GetContentAssetListResult"][0]["FilePath"]

    log_this(f"Found file: {file_url}")

    # Decoding the JSON took out all the escape characters, so the URL is good to go.
    log_this(f"GETting file URL {file_url}")
    (get_success, get_message, s, get_response) = get(s, file_url)

    if not get_success:
        log_this(f"ERROR: {get_message}")
        sys.exit(0)

    # At last, we have a file we can save out.
    now_ts = datetime.now().strftime("%Y%m%d%H%M%S")
    output_filename = f"Canadian_Pacific_RTMs_and_Carloads_{now_ts}.XLSX"

    # Use write-binary mode to ensure a good save
    (save_success, save_message) = save_file(output_filename, get_response.content)

    if not save_success:
        log_this(f"ERROR: {save_message}")
        sys.exit(0)

    log_this("Script completed successfully. Nice.")


def log_this(message):
    # Set up logging if you want
    # Add a debug mode if you want
    # I'm happy to just print messages for now
    print(message)


def get(s, url):
    # Get URL using the passed session
    try:
        response = s.get(url)
    except Exception as e:
        return False, e, s, None
    else:
        return True, "Nice", s, response


def post(s, url, payload):
    # Convert the payload to JSON for the post request
    try:
        response = s.post(url, data=json.dumps(payload))
    except Exception as e:
        return False, e, s, None
    else:
        return True, "Nice", s, response


def save_file(output_filename, output_content):
    try:
        with open(output_filename, "wb") as file:
            file.write(output_content)
    except Exception as e:
        return False, e
    else:
        return True, "Nice"


if __name__ == "__main__":
    scrape()
