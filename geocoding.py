import classes
from tqdm import tqdm
import time
import requests
import csv
import openpyxl

API_KEY = 'AIzaSyBiO44jrglBDqWVQLrdPCedfqtax4HrwjQ'
FILENAME = r'C:\Users\36004642\PycharmProjects\batch_geocode\pocs_address_result.xlsx'
TIMEOUT = 0.3
# INPUT_FILENAME = "pocs_address.csv"
INPUT_FILENAME = r'C:\Users\36004642\PycharmProjects\batch_geocode\pocs_address.xlsx'


def xls_read(filename):
    employees_sheet = classes.ExcelWorkbook(filename=filename)
    res = employees_sheet.read()
    return res


def address_convert(address):
    parse_pocs = []
    len_rows = len(address)

    for i in tqdm(range(len_rows), colour='green'):  # цикл который рисует прогресбар
        poc = address[i]
        res = pars_file(poc)
        parse_pocs.append(res)
    return parse_pocs


def pars_file(one_poc):
    res = []
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={adr}&region=ua&language=uk&key={apy}".format(
        adr=one_poc[1], apy=API_KEY)
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
        found_address = answer.get('formatted_address')

    res.append(one_poc[0])
    res.append(lat)
    res.append(lon)
    res.append(found_address)

    time.sleep(TIMEOUT)
    return res


def write_xls(text, file):
    """
    Записуємо результат у файл
    """
    my_file = classes.ExcelWorkbook(filename=file)
    wb = my_file.create()
    title = 'test'
    column_sheet = ['id', 'lat', 'lon', 'address']
    rows = text
    if rows == "Error: unable to fetch data" or len(rows) == 0:  # Если ошибка или пусто
        return None
    else:
        my_sheet = classes.ExcelSheet(all_rows=rows, columns=column_sheet, num=[1, ])
        my_ws = my_sheet.sheet_active(wb, title=title)
        my_sheet.write(ws=my_ws)
        wb.save(filename=file)
        return None


if __name__ == '__main__':
    my_file = xls_read(INPUT_FILENAME)
    my_text = address_convert(my_file[1:])
    write_xls(text=my_text, file=FILENAME)
