
import time
import requests
import csv

# API_KEY = 'AIzaSyBgpO0hfoepW0eTp2vaRnYIhosbPnKKl1E'
API_KEY = 'AIzaSyAqSX2KdlYt-PqLQEfB20q1D7sBXmPSQnU'

FILENAME = 'pocs_test_result.csv'
TIMEOUT = 0.3
input_filename = "pocs_test.csv"


def csv_read(filename):
    with open(filename, 'r', encoding="utf-8") as fp:
        reader = csv.reader(fp, delimiter=',', quotechar="'")
        data_read = [row for row in reader]
    return data_read


def address_convert(address):
    parse_pocs = []
    for poc in address:
        res = pars_file(poc)
        parse_pocs.append(res)
        print(res)
    return parse_pocs


def pars_file(one_poc):
    res = []
    # geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address=% s &region=ua&key=AIzaSyBgpO0hfoepW0eTp2vaRnYIhosbPnKKl1E" % one_poc[1]
    # geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address=% s" % one_poc[1]
    # geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(one_poc[1])
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (one_poc[1], API_KEY)
    # print(geocode_url)
    results = requests.get(geocode_url)
    results = results.json()

    if len(results['results']) == 0:
        # geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address=% s &region=ua&key=AIzaSyBgpO0hfoepW0eTp2vaRnYIhosbPnKKl1E" % \
        #               one_poc[2]
        # geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(one_poc[2])
        # print(geocode_url)
        geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (one_poc[2], API_KEY)
        results = requests.get(geocode_url)
        results = results.json()
        if len(results['results']) == 0:
            lat = None
            lon = None
            found_address = one_poc[1]
        else:
            answer = results['results'][0]
            lat = answer.get('geometry').get('location').get('lat')
            lon = answer.get('geometry').get('location').get('lng')
            found_address = one_poc[2]
    else:
        answer = results['results'][0]
        lat = answer.get('geometry').get('location').get('lat')
        lon = answer.get('geometry').get('location').get('lng')
        found_address = one_poc[1]

    res.append(one_poc[0])
    res.append(lat)
    res.append(lon)
    res.append(found_address)

    time.sleep(TIMEOUT)

    return res


def write_file(text):
    with open(FILENAME, "w", newline="", encoding="utf-8", ) as file:
        writer = csv.writer(file)
        writer.writerows([['id', 'lat', 'lon', 'address'], ])
        writer.writerows(text)
    return None


my_file = csv_read(input_filename)

write_file(address_convert(my_file[1:]))
