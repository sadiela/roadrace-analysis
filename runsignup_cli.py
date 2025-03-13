from runsignup_api import *

if __name__ == "__main__":
    state = input("What State? ")
    city = input("What City? ")
    print(state)
    s_date = input("Start Date (YYYY-MM-DD)? ")
    e_date = input("End Date (YYYY-MM-DD)? ")

    get_race_ids(s_date, e_date, city, state)