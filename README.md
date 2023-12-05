# NAPLAN Scraper

NAPLAN data is publicly available on [MySchool](myschool.edu.au/). Unfortunately [ACARA](https://www.acara.edu.au/), the oranisation behind MySchool won't provide all the results in a spreadsheet because:

- "ACARA’s data access protocols are intended to facilitate quality research and maximise benefits to students, schools and the Australian community, while mitigating risk of misuse of data and associated harm to schooling in Australia.” AND
- "We don’t promote the comparison of schools based on results alone and therefore don’t provide data for personal use. "

🤦🏾‍♂️

...anyway, here's a python tool to scrape NAPLAN results for a given school.

# Running It

The simplest way to get started is via [poetry](https://python-poetry.org/), simply:

```bash
pip install poetry # if not already installed
poetry install
poetry run python naplan_scrapyer.py {school id} # EG:
poetry run python naplan_scrapyer.py 45587
```

To figure out the `school-id` you can download [School Profile 2008-2022 (xlsx, 24 MB)](https://acara.edu.au/docs/default-source/default-document-library/school-profile-2008-2022.xlsx?sfvrsn=d40e4c07_0) which contains the `school-id` (ACARA SML ID) as well as other data points such as:

- Whether it is independent, public, etc
- ICSEA, an **I**ndex of **C**ommunity **S**ocio-**E**ducational **A**dvantage
- And more...

# Run via Docker

Build the docker image using:

```bash
docker build . -t naplanscraper
```

The scraper requires a `school-id` to run, ensure this is passed when running the image.

```bash
docker run naplanscraper {School ID}

# Eg:
docker run naplanscraper 45587
```

# TO-DO

- [ ] Add some tests
- [ ] Lint & type-check
- [ ] Deploy to AWS Batch
  - Write a script to iterate over each school ID, check if the results are available in S3 already & if not, submit a job to batch for the school ID
