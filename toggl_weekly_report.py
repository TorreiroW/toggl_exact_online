import os
import requests
import json
import argparse
from datetime import datetime, timedelta

# Function to read the Toggl API key from a file


def read_api_key(api_key_file):
    with open(api_key_file, 'r') as file:
        api_key = file.read().strip()
    return api_key

# Function to get the time entries for a specific week


def get_weekly_report(api_key, week_number, year, workspace_id):
    start_date = datetime.strptime(f'{year}-W{week_number}-1', "%Y-W%U-%w")
    end_date = start_date + timedelta(days=6)

    headers = {
        'Authorization': f'Basic {api_key}',
    }

    params = {
        'user_agent': 'TogglWeekReportDownloader',
        'workspace_id': workspace_id,
        'since': start_date.strftime('%Y-%m-%dT%H:%M:%S%z'),
        'until': end_date.strftime('%Y-%m-%dT%H:%M:%S%z'),
    }

    response = requests.get(
        'https://api.track.toggl.com/reports/api/v2/details', headers=headers, params=params)

    if response.status_code == 200:
        report_data = response.json()
        return report_data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Download Toggl detailed report for a specific week')
    parser.add_argument('-w', '--week-number', type=int,
                        required=True, help='Week number (e.g., 1-52)')
    parser.add_argument('-y', '--year', type=int, required=True, help='Year')
    parser.add_argument('-k', '--api-key-file',
                        default='toggl_api.dat', help='Toggl API key file')
    parser.add_argument('-i', '--workspace-id', type=int,
                        required=True, help='Toggl workspace ID')

    args = parser.parse_args()

    week_number = args.week_number
    year = args.year
    api_key_file = args.api_key_file
    workspace_id = args.workspace_id

    if not os.path.isfile(api_key_file):
        print(f"API key file '{api_key_file}' not found.")
        exit(1)

    api_key = read_api_key(api_key_file)

    report_data = get_weekly_report(api_key, week_number, year, workspace_id)

    if report_data:
        # You can now process and use the report data as needed
        # For example, you can save it to a JSON file or perform data analysis.
        with open(f'weekly_report_w{week_number}_y{year}.json', 'w') as report_file:
            json.dump(report_data, report_file, indent=4)
        print(
            f"Report data saved to weekly_report_w{week_number}_y{year}.json")
