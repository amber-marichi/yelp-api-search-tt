# Yelp Api search script
Simple example script to search for business by category and location using free Yelp API. Requests are done with Python "requests" library, output is stored in .csv file form.

On how to register and get API key please refer to https://docs.developer.yelp.com/docs/fusion-authentication


### To run locally
!! Python3.8+ with pip should be installed and ready.

Download using GitHUB
```sh
git clone https://github.com/amber-marichi/yelp-api-search-tt.git
cd yelp-api-search-tt
```

1. Create and activate venv:
```sh
python -m venv venv
```

2. Activate environment:

On Mac and Linux:
```sh
source venv/bin/activate
```
On Windows
```sh
venv/Scripts/activate
```

3. Get requests library:

```sh
pip install requests
```

4. Fill search fields and start the app:

```sh
python app.py
```

### Getting results
For example following fields values
```sh
search_address = "Coal Harbor"
search_category = "eyelash"
```
will result in getting such .csv file:
```sh
coal_harbor_eyelash.csv
```
![Screenshot at 2023-07-27 11-39-33](https://github.com/amber-marichi/yelp-api-search-tt/assets/72259870/957e0ed0-a82b-49e4-bc5c-16284832e3d7)
