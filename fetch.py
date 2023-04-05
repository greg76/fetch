import urllib.request
import tempfile
import hashlib
import datetime
import os
from sys import version_info


__tmp_dir = f"{tempfile.gettempdir()}/fetchpy-cache"
expiry_seconds: int = 600
user_agent = f"python{version_info.major}.{version_info.minor} urllib"


def get(url: str, headers: dict = None) -> str:
    if headers:
        request = urllib.request.Request(url, headers=headers)
    else:
        request = urllib.request.Request(url)
    request.add_header("User-Agent", user_agent)
    response = urllib.request.urlopen(request)
    charset = response.info().get_param('charset')
    content = response.read().decode(charset or 'utf-8')
    return content


def save(filepath: str, content: str):
    if not os.path.isdir(__tmp_dir):
        os.makedirs(__tmp_dir)

    with open(filepath, 'w') as f:
        f.write(content)


def load(filepath: str) -> str|None:
    if os.path.isfile(filepath):
        modified = max(os.path.getctime(filepath), os.path.getmtime(filepath))
        now = datetime.datetime.now().timestamp()
        if now - modified < expiry_seconds:
            with open(filepath, 'r') as f:
                return f.read()
    return None


def path(url: str) -> str:
    seed = url
    hash = hashlib.md5(seed.encode())
    path = f"{__tmp_dir}/{hash.hexdigest()}"
    return path


def fetch(url: str, headers: dict = None) -> str:
    filepath = path(url)
    content = load(filepath)
    if not content:
        content = get(url, headers=headers)
        save(filepath, content)
    return content


def cache_usage() -> int:
    file_sizes = (
        os.path.getsize(f"{__tmp_dir}/{filename}")
        for filename in os.listdir(__tmp_dir)
        if os.path.isfile(f"{__tmp_dir}/{filename}")
    )

    return sum(file_sizes)

if __name__ == '__main__':

    print(f"current case size: {cache_usage()} bytes")
    print(f"user agent: {user_agent}")