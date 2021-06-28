#!/usr/bin/env python

import os
import sys
import yaml
import enquiries
import requests
import jmespath
import datetime
from tabulate import tabulate
from argparse import ArgumentParser

global_arguments = None

def init_arguments():
    parser = ArgumentParser(prog=os.path.basename(__file__))
    parser.add_argument('--area', help="grandcanyonlodges, glaciernationalparklodges, grandcanyongrandhotel, yellowstonenationalparklodges, zionlodge");
    parser.add_argument('--start-date', help='Start Date (MM/DD/YYYY)')
    parser.add_argument('--end-date', help='End Date (MM/DD/YYYY)')
    parser.add_argument('--adults', help='Number of Adults (1~8)')
    parser.add_argument('--children', help='Number of Children (0~7)')
    return parser.parse_args()

def get_areas():
    with open('config.yml', 'r') as s:
        return yaml.safe_load(s)['areas']

def select_area():
    areas = get_areas()
    codes = jmespath.search('[*].code', areas)

    if global_arguments.area in codes:
        index = codes.index(global_arguments.area)
        return areas[index]

    options = jmespath.search('[*].title', areas)
    choice = enquiries.choose('Area: ', options)
    index = options.index(choice)
    return areas[index]

def get_information(area):
    url = f'https://webapi.xanterra.net/v1/api/property/information/{area["code"]}'
    return requests.get(url).json()

def get_hotels(area):
    url = f'https://webapi.xanterra.net/v1/api/property/hotels/{area["code"]}'
    return requests.get(url).json()

def select_date():
    def days_between(d1, d2):
        d1 = datetime.datetime.strptime(d1, "%m/%d/%Y")
        d2 = datetime.datetime.strptime(d2, "%m/%d/%Y")
        return abs((d2 - d1).days)

    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%m/%d/%Y")
    start_date = global_arguments.start_date or input(f'Enter start date [{tomorrow}]: ') or tomorrow

    next_week = (datetime.datetime.strptime(start_date, "%m/%d/%Y") +datetime.timedelta(days=7)).strftime("%m/%d/%Y")
    end_date = global_arguments.end_date or input(f'Enter end date [{next_week}]: ') or next_week

    return start_date, days_between(start_date, end_date)

def select_people():
    if global_arguments.adults is not None:
        adults = global_arguments.adults
    else:
        adults = global_arguments.adults or input('Enter number of adults (1~8)[1]: ') or 1
    if global_arguments.children is not None:
        children = global_arguments.children
    else:
        children = input('Enter number of children (0~7)[0]: ') or 0
    return int(adults), int(children)

def get_availability(area, date, nights):
    url = f'https://webapi.xanterra.net/v1/api/availability/hotels/{area["code"]}'
    params = {'date': date, 'limit': nights}
    return requests.get(url, params).json()

def get_flexsearch_url(area, date, nights, adults, children):
    dateFrom = datetime.datetime.strptime(date, "%m/%d/%Y").strftime("%m-%d-%Y")
    url = f'https://secure.{area["code"]}.com/booking/lodging-flex-search'
    params = {
        'dateFrom': dateFrom,
        'adults': adults,
        'children': children,
        'nights': nights,
        'destination': 'ALL'
    }
    return requests.Request('GET', url, params=params).prepare().url

def parse_availability(area, availability, adults, children):
    messages = []
    result_table = ''

    # code and title
    hotels = get_hotels(area)
    code_title_table = []
    code_title_map = {}
    for code, data in hotels.items():
        code_title_table.append([code, data['title']])
        code_title_map[code] = data['title']
    result_table += "\n" + tabulate(code_title_table, headers=["Code", "Hotel Title"], tablefmt="github") + "\n"

    # hotel available
    date_table = []
    hotel_header = []
    people = adults + children
    for date, data in availability['availability'].items():
        if not hotel_header:
            hotel_header = data.keys()

        date_data = [date]
        for code, hotel in data.items():
            available_people = 0
            for idx, perGuests in hotel["perGuests"].items():
                available_people += perGuests['a']
            if available_people >= (adults + children):
                date_data.append('O')
                messages.append(f"[{date}] {code_title_map[code]}")
            else:
                date_data.append('X')
        date_table.append(date_data)
    result_table += "\n" + tabulate(date_table, headers=hotel_header, tablefmt="github") + "\n"

    return messages, result_table


def main():
    global global_arguments
    global_arguments = init_arguments()

    # Step 1: Area, [Arrival Date, Departure Date]
    area = select_area()

    # Step 2: pick date
    date, nights = select_date()

    # Step 3: Number of people
    adults, children = select_people()

    # Step 4: Parse availability
    availability = get_availability(area, date, nights)
    messages, result_table = parse_availability(area, availability, adults, children)

    # Step 5: Check availability and notify
    if messages:
        # TODO: Push Notification
        print()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!! Found the available date !!")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(result_table)
        print("\nList: ")
        for message in messages:
            print(message)
        print("\nFlexible Date URL: " + get_flexsearch_url(area, date, nights, adults, children))

if __name__ == "__main__":
    main()