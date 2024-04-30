import classes
from tqdm import tqdm
import time
import requests

API_KEY = 'AIzaSyCuh0ZoaF4m71WkmjA0ZfD7NduAuZ7W5z8'
FILENAME = r'pocs_address_result.xlsx'
INPUT_FILENAME = r'pocs_address.xlsx'
TIMEOUT = 0.3


def xls_read(filename):
    """Конвертуємо дані з екселю в словник"""
    employees_sheet = classes.ExcelWorkbook(filename=filename)
    res = employees_sheet.read()
    return res


def address_convert(address):
    """Конвертуємо адресу в координати"""
    print(address_convert.__doc__)
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
    print(geocode_url)

    if len(results['results']) == 0:
        lat = None
        lon = None
        address = one_poc[1]
        found_address = None
        text = ''
    else:
        answer = results['results'][0]
        # lat = answer.get('geometry').get('location').get('lat')
        # lon = answer.get('geometry').get('location').get('lng')
        # address = one_poc[1]
        # found_address = answer.get('formatted_address')

        # новий варіант з форматованою адресою
        address = one_poc[1]
        lat = answer.get('geometry').get('location').get('lat')
        lon = answer.get('geometry').get('location').get('lng')
        pars = {}
        text = ''
        for i in answer.get('address_components'):
            pars.update({i.get('types')[0]: i.get('long_name')})
        for key in ['locality', 'route', 'street_number']:
            if pars.get(key) == None:
                t = ''
            else:
                t = pars.get(key)
            if t == '':
                pass
            else:
                if key == 'locality':
                    text = text + t
                else:
                    text = text + ', ' + t

    res.append(one_poc[0])
    res.append(address)
    # res.append(found_address)
    res.append(text)
    res.append(lat)
    res.append(lon)
    time.sleep(TIMEOUT)
    return res


def write_xls(text, file):
    """Записуємо результат у файл"""
    my_file = classes.ExcelWorkbook(filename=file)
    wb = my_file.create()
    title = 'found_address'
    column_sheet = ['id', 'address', 'found_address', 'lat', 'lon']
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
