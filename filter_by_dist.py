import csv

input_filename = 'sort_distance_after_match.csv'
output_filename = 'filter_by_dist.csv'


def csv_read(filename):
    with open(filename, 'r', encoding="utf-8") as fp:
        reader = csv.reader(fp, delimiter=',', quotechar="'")
        data_read = [row for row in reader]
    return data_read


def comparisons(pocs):
    result = []
    result.append(pocs[1])
    for poc in pocs:
        # if len(result) == 0:
        #     result.append(poc)
        #     continue
        for res in result:
            if poc[0] == res[0]:
                if poc[2] < res[2]:
                    result.remove()
                    result.append(poc)
        result.append(poc)



    return res



def write_file(text):
    with open(output_filename, "w", newline="", encoding="utf-8", ) as file:
        writer = csv.writer(file)
        writer.writerows([['id', 'Ol_id_inbev', 'distance'], ])
        writer.writerows(text)
    return None


all_pocs = csv_read(input_filename)
comparison = comparisons(all_pocs)
write_file(comparison)