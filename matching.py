import math

# pi - число pi, rad - радиус сферы (Земли)
rad = 6372795

active = (
    ('''"Коротенко Мелитополь";on-trade;101140000001824;2017''', 46.297906, 35.305783),
    ('''"Коротенко Мелитополь";off-trade;101140000001885;2017''', 46.297947, 35.305533),
    )

pasive = (
    ('''"Караван-Сарай Краматорск";off-trade;1010703644;2012''', 49.19101, 37.515147),
    ('''"Караван-Сарай Краматорск";off-trade;1010705815;2016''', 49.191104, 37.51574),
    ('''"Караван-Сарай Краматорск";off-trade;1010700319;2012''', 49.206317, 37.59614)
    )


def dist(p1, p2):
    # координаты двух точек
    llat1 = p1[1]
    llong1 = p1[2]

    llat2 = p2[1]
    llong2 = p2[2]

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

check = 0
count2 = 0

for first in range(len(active)):
    for second in range(len(pasive)):
        count2 = count2 + 1
        distance = dist(active[first], pasive[second])
        # print(first, second)
        if distance <= 10:
            check = check + 1
            print(count2,";",active[first][0], ";", pasive[second][0], ";", distance, ";check - ", check)
