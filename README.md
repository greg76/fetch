# fetch.py
just an other simple urllib wrapper for doing api requests. handy when you want to quickly iterate over consuming REST apis, but you don't always want to wait for longer then usual response times, you would only want to quickly see your changes with some recent responses.

it does:
* binary to text decoding
* caching to system temp folder (under `fetchpy-cache` sub-folder)
* no external dependencies, standard library only

## api
```
expiry_seconds: int (default: 600)

def fetch(url, headers: dict|None) -> str
```

## how to install
```
pip install git+https://github.com/greg76/fetch.git
```
