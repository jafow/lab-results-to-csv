from bs4 import BeautifulSoup
import glob
import csv
import time

def format_date (date_str):
    """ formats a string of 'Month Day Year' to a tuple of format YYYY MM DD """
    return time.strptime(date_str, '%b %d %Y')

def add_column(target, col_name):
    target.append(col_name)
    return target

def main ():
    """ reads a directory of html files and scrape lab results data from each file """
    res = dict()
    res['columns'] = list()

    html_files = glob.glob('./assets/*.html')

    for file in html_files:
        f = open(file, 'r')
        input = f.read()

        soup = BeautifulSoup(input, 'html.parser')

        """ data for 'All results' output are kept under the first <section> tag
        in a unordered list """
        nodes = [c for c in soup.section.ul.children]

        # get the name of current test TYPE;
        # these are written as fieldnames/columns on the CSV file
        measurement_key = (soup.section.dt.h3.text).upper()
        add_column(res['columns'], measurement_key)

        for node in nodes:
            if len(list(node)) > 1:
                date_key = node.find_all('span', class_='date')[0].text
                level = node.div.span.text

                test_data = {measurement_key: level}

                if res.get(date_key) is not None:
                    # we have records at this date so extend the dict
                    res[date_key].update(test_data)
                else:
                    res[date_key] = test_data

    return res

def make_csv(data):
    """ write a csv file from a dictionary of {'level': [list of entries]} """
    with open('./assets/levels-entries.csv', 'w', newline='') as csvfile:
        fieldnames = ['date'] + sorted(data['columns'])
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for key in data:
            if key is not 'columns':
                date = {'date': key}
                # assign all key & values onto date dict
                row =  {**date, **data[key]}
                writer.writerow(row)

    return csvfile

make_csv(main())
