# lab-results-to-csv

A scraper script for writing the interesting parts of many bloodtest results from html to a CSV file.

## example
Running:

```bash
python3 main.py
```

will read the [example file](./assets/example.html) and write a CSV file
called `level-entries.csv` to the `assets` folder that looks like this:

```bash
cat assets/level-entries.csv

date,test,level
"Jan 01, 2017",example, 4.9 g/dL
```

## License 
MIT
