import pytz
import requests
import datetime


def get_number_of_pages():
    url = "https://devman.org/api/challenges/solution_attempts/"
    response = requests.get(url)
    if response.ok:
        return response.json()["number_of_pages"]


def load_attempts(pages):
    page = 1
    pages = 1
    url = "https://devman.org/api/challenges/solution_attempts/"
    while page <= pages:
        response = requests.get(url, params={"page": page})
        attempts_data = response.json()["records"]
        pages = response.json()["number_of_pages"]
        for attempt in attempts_data:
            yield {
                'username': attempt["username"],
                'timestamp': attempt["timestamp"],
                'timezone': attempt["timezone"],
            }
        page += 1


def get_midnighters(attempts_data):
    midnighters = set()
    midnight_time = 0
    morning_time = 5
    for attempt in attempts_data:
        attempt_time = convert_to_hours(
            attempt["timestamp"],
            attempt["timezone"]
        )

        if midnight_time <= attempt_time <= morning_time:
            midnighters.add(attempt["username"])
    return midnighters


def convert_to_hours(timestamp, user_timezone):
    return datetime.datetime.fromtimestamp(
        timestamp,
        tz=pytz.timezone(user_timezone)
    ).hour


if __name__ == "__main__":
    number_of_pages = get_number_of_pages()
    attempts_data = load_attempts(number_of_pages)
    midnighters = get_midnighters(attempts_data)
    print("Midnighters:")
    for username in midnighters:
        print(username)
