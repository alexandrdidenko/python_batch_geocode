import csv
import math
import time


# pi - число pi, rad - радиус сферы (Земли)
rad = 6372795
input_filename_effes = 'pocs_test_result.csv'
input_filename_inbev = 'UA_pocs_SW_test.csv'
output_filename = 'pocs_matching_test.csv'
distance_limit = 50
TIMEOUT = 0


def csv_read(filename):
    with open(filename, 'r', encoding="utf-8") as fp:
        reader = csv.reader(fp, delimiter=',', quotechar="'")
        data_read = [row for row in reader]
    return data_read


def dist(p1, p2):
    # координаты двух точек
    llat1 = float(p1[1])
    llong1 = float(p1[2])

    llat2 = float(p2[1])
    llong2 = float(p2[2])

    # в радианах
    lat1 = llat1 * math.pi / 180.
    lat2 = llat2 * math.pi / 180.
    long1 = llong1 * math.pi / 180.
    long2 = llong2 * math.pi / 180.

    # косинусы и синусы широт и разницы долгот
    cl1 = math.cos(lat1)
    cl2 = math.cos(lat2)
    sl1 = math.sin(lat1)
    sl2 = math.sin(lat2)
    delta = long2 - long1
    cdelta = math.cos(delta)
    sdelta = math.sin(delta)

    # вычисления длины большого круга
    y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
    x = sl1 * sl2 + cl1 * cl2 * cdelta
    ad = math.atan2(y, x)
    dist = ad * rad
    return dist


def match(all_inbev, all_effes):
    result = []
    count = 0
    for effes in all_effes:
        res = []
        for inbev in all_inbev:
            try:
                distance = dist(inbev, effes)
            except ValueError:
                continue
            if distance <= distance_limit:
                res.append(effes[0])
                res.append(inbev[0])
                result.append(res)
                print('итерация - {} совпадений - {}'.format(count, len(result)))

            time.sleep(TIMEOUT)

        count += 1
    return result


def write_file(text):
    with open('pocs_matching_test.csv', "w", newline="", encoding="utf-8", ) as file:
        writer = csv.writer(file)
        # writer.writerows([['id', 'Ol_id_inbev'], ])
        writer.writerows(text)
    return None


all_inbev = csv_read(input_filename_inbev)[1:]
all_effes = csv_read(input_filename_effes)[1:]
# after_mach = match(all_inbev, all_effes)
write_file(match(all_inbev, all_effes))
