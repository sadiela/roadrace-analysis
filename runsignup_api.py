import requests
import json
import sys
from API_CONSTANTS import API_KEY, API_SECRET 

'''
Steps for Obtaining Race Result Data from the RunSignup API
1. Obtain an API key and secret from RunSignup. You can join 
   their affiliate program to obtain these credentials. (https://runsignup.com/API)
2. Get a race id using the "Races" API (https://runsignup.com/API/races/GET). You can 
   filter by location and date if you are looking for a specific race. 
3. Once you have a race id, you will need a specific event id to download any results. 
   This is because each of the race ids seem to correspond to an event that sometimes 
   happens annually. To obtain an event id, use the "Get race" API 
   (https://runsignup.com/API/race/:race_id/GET). This will return a list of events and
   you can choose the specific event you are interested in.
4. Now that you have both the race id and the event id, you have all the required 
   information needed to download results. For this, use the "Get event results" API.
   (https://runsignup.com/rest/race/:race_id/results/get-results).
'''

race_id = "77205"
event_id = "795316"
startDate = '2024-12-01'
endDate = '2024-12-15'

def get_race_ids(startDate, endDate, city, state):
    url = f"https://runsignup.com/rest/races?api_key={API_KEY}&api_secret={API_SECRET}&city={city}&state={state}&start_date={startDate}&end_date={endDate}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        race_data = response.json()["races"]
        for race in race_data:
            print(race["race"]["name"],race["race"]["race_id"])
    else:
        # Print an error message if the request failed
        print("Error:", response.status_code, response.text)

def get_event_ids(race_id):
    url = f"https://runsignup.com/Rest/race/{race_id}?api_key={API_KEY}&api_secret={API_SECRET}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        event_data = response.json()["race"]["events"]
        for event in event_data:
            print(event["event_id"], event["name"], event["start_time"])
    else:
        # Print an error message if the request failed
        print("Error:", response.status_code, response.text)

def get_event_results(race_id, event_id):
    # unfortunately there is no way to know how many pages of results there are (that I can tell) so we will have to do a while loop
    # I want OVERALL RESULTS! Everything else I can figure out later.
    # I have no idea how standardized this format for race results is, so this function may not be very generally useful
    cur_page = 1
    url = f"https://runsignup.com/Rest/race/{race_id}/results/get-results?event_id={event_id}&api_key={API_KEY}&api_secret={API_SECRET}&format=json&page=1"
    all_results = []
    while True:
        response = requests.get(url + "&page=" + str(cur_page))
        if response.status_code == 200:
            results = response.json()["individual_results_sets"] #[0]["results"]
            if len(results) != 0:
                if len(results[0]["results"]) == 0:
                    break
                all_results.extend(results[0]["results"])
            else:
                print("No results found")
                break
            cur_page += 1
        else:
            # Print an error message if the request failed
            print("Error:", response.status_code, response.text)
            break
    print("TOTAL RESULTS", len(all_results))
    return all_results

if __name__ == "__main__":
    #get_race_ids("2024-11-01", "2025-11-15", "cambridge", "MA")
    CAMBRIDGE_HALF = "74589"
    CAMBRIDGE_2024_HALF = "799523"
    #get_event_ids(CAMBRIDGE_HALF)
    event_results = get_event_results("119025", "872447")
    

