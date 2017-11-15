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
        # open the current file
        f = open(file, 'r')
        input = f.read()

        # read into soup
        soup = BeautifulSoup(input, 'html.parser')

        """data for 'All results' output are kept under the first <section> tag
        in a unordered list"""
        d = [c for c in soup.section.ul.children]

        levels = [
                {
                    'level': node.div.span.text,
                    'date': format_date(node.find_all('span', class_='date')[0].text)
                    }
                for node in d
                if len(list(node)) > 1
                ]

        res[measurement_key] = levels

    return res

# csv fields: date, measurement_key, level
def make_csv(data):
    """ write a csv file from a dictionary of {'level': [list of entries]} """
    with open('./assets/levels-entries.csv', 'w', newline='') as csvfile:
        fieldnames = ['date', 'test', 'level']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for key in data:
            for xs in data[key]:
                writer.writerow({'date': xs['date'], 'test': key, 'level': xs['level']})

make_csv(main())
