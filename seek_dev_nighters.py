import pytz
import requests
import datetime


def load_attempts():
    page = 1
    url = "https://devman.org/api/challenges/solution_attempts/"
    while True:
        response = requests.get(url, params={"page": page})
        attempts_data = response.json()
        for attempt in attempts_data["records"]:
            yield {
                'username': attempt["username"],
                'timestamp': attempt["timestamp"],
                'timezone': attempt["timezone"],
            }
        page += 1
        if page > attempts_data["number_of_pages"]:
            break


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
    attempts_data = load_attempts()
    midnighters = get_midnighters(attempts_data)
    print("Midnighters:")
    for username in midnighters:
        print(username)
