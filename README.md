# Hospital Private GPT

### Flow Diagram:
![](./Flow%20diagram.png)

### Documentation
**Firstly** We are making a flow diagram in which we decide thingss how to make,how to work and what we need.
**Secondly** prepare a file named as scrape.py in which it contain:
 (a) Imports: The code imports necessary libraries including re, json, urllib, requests, BeautifulSoup from bs4.
 (b) Global Variables: It initializes a global variable count to keep track of the number of doctors scraped.
 (c) Helper Functions:
  - writeDocData(org, docData): Writes scraped doctor data to a JSON file.
  - decode_email(encoded_email): Decodes encoded email addresses found in HTML.
  - scrapeSGR(url): Scrapes doctor data from a specific type of website.
  - scrapeBombayHptl(url): Scrapes doctor data from another type of website.
  - scrapeData(url): Chooses which scraping function to call based on the URL format.
(d) Main Function:
  - Reads a list of hospital URLs from a file.
  - Iterates over the URLs, calls the appropriate scraping function for each URL, and writes the scraped data to a JSON file.
**Thirdly**, requirement file is:
(a) beautifulsoup4==4.12.3: Used for web scraping tasks, providing tools for parsing HTML and XML documents.
(b) certifi==2024.2.2: Provides curated Root Certificates for validating SSL certificates during HTTPS requests.
(c) charset-normalizer==3.3.2: Normalizes character encodings in HTTP headers and HTML/XML documents.
(d) idna==3.6: Implements Internationalized Domain Names in Applications (IDNA) encoding and decoding algorithms.
(e) requests==2.31.0: Simplifies making HTTP requests and handling responses, including session management and authentication.
(f) soupsieve==2.5: Dependency of BeautifulSoup, provides a CSS selector library for parsing CSS selectors.
(g) urllib3==2.2.1: HTTP client library for Python, offering features like connection pooling and SSL verification.

### Usage
```py
python scrape.py # Scrape website and stores out in file in json format
```






