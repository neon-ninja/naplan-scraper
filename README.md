# NAPLAN Scraper

NAPLAN data is publicly available on [MySchool](https://myschool.edu.au/). Unfortunately [ACARA](https://www.acara.edu.au/), the oranisation behind MySchool won't provide all the results in a spreadsheet because:

- "ACARA’s data access protocols are intended to facilitate quality research and maximise benefits to students, schools and the Australian community, while mitigating risk of misuse of data and associated harm to schooling in Australia.” AND
- "We don’t promote the comparison of schools based on results alone and therefore don’t provide data for personal use. "

🤦🏾‍♂️

...anyway, here's a python tool to scrape NAPLAN results.

# Running It

You'll almost certainly get blocked running this. ATM it's setup to randomly rotate through a list of proxies. Ensure you have a file called `proxy_list.txt` in your root folder.

The simplest way to get started is via [poetry](https://python-poetry.org/), simply:

```bash
pip install poetry # if not already installed
poetry install
poetry run python scraper/generate_school_ids.py
poetry run python scrape_all.py
```

# TO-DO

- [ ] Get it to run without getting stuck on Catpchas or IP blocks
