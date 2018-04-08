import csv

input_filename = 'sort_distance_after_match.csv'
output_filename = 'filter_by_dist.csv'


def csv_read(filename):
    with open(filename, 'r', encoding="utf-8") as fp:
        reader = csv.reader(fp, delimiter=',', quotechar="'")
        data_read = [row for row in reader]
    return data_read

all_pocs = csv_read(input_filename)

resutl = []
for poc in all_pocs[1:]:

    res = poc
    curent_poc = poc[0]
    dist = poc[2]
    for poc2 in all_pocs[1:]:
        if poc2[0] == curent_poc and poc[2] < dist:
            res = poc2
