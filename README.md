# fetch.py
just an other simple urllib wrapper for api requests. handy when you want to quickly iterate over consuming REST apis, but you don't always want to wait for longer then usual response times. quickly see your changes with some recent responses from a local file cache. (cache being located in the temp folder of the OS)

it does:
* binary to text decoding
* caching to system temp folder (under `fetchpy-cache` sub-folder)
* no external dependencies, standard library only
* default user agent is set to: "python3.x urllib"

## api
```
expiry_seconds: int (default: 600)

def fetch(url, headers: dict|None, auth: dict|None) -> str
    headers: key, value pairs that you would like to add to http request headers
    auth: (user_name, password) tuple for basic auth
```

## how to install
```
pip install git+https://github.com/greg76/fetch.git
```
