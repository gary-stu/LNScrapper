# LNScrapper

This scrapper uses both requests to query existing APIs and Selenium to scrape webpages not using APIs.
Selenium is set-up to use Firefox specifically.

## Installation
### Setting up the project

Note: These setup steps are designed for windows, but you should be able to do the same on Linux and Mac by adapting the commands

1. If not done already, install Firefox: [https://www.mozilla.org/fr/firefox/new/](https://www.mozilla.org/fr/firefox/new/)

2. Optional: create a virtual env if you don't want to install libraries directly onto your system
```bash
python -m venv {venv_name}
.\{venv_name}\Scripts\Activate.ps1
```

3. install the project requirements:
````bash
pip install -r requirements.txt
````

### Setting up firefox

1. Optional: For ease of use, command options have been added to LNScrapper.py that requires the Firefox folder to be added to the PATH

2. Create a new Firefox Profile named `firefox.selenium` in the profiles folder:
```bash
.\LNScrapper.py --new-profile
```

3. Pass the anti-bot challenges for the websites that requires it:
```bash
.\LNScrapper.py --challenge
```

## Running the project

1. Optional: You may need to pass the challenges before running the script, else sources requiring challenges will be skipped
```
.\LNScrapper.py --challenge
```

2. Run the script (in verbose mode if you want)
```bash
.\LNScrapper.py [-v] 
```
