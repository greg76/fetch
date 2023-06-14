import urllib.request
import tempfile
import hashlib
import datetime
import os
import base64
from sys import version_info


expiry_seconds: int = 600
cache_size_in_MB: float = 5

_tmp_dir = os.path.join(tempfile.gettempdir(), "fetchpy-cache")
_default_user_agent = f"python{version_info.major}.{version_info.minor} urllib"


def basicAuthHeader(credentials: tuple) -> tuple:
    user_name, password = credentials
    raw_token = f"{user_name}:{password}"
    base64string = base64.b64encode(raw_token.encode()).decode()
    return "Authorization", f"Basic {base64string}"


def get(url: str, headers: dict = None, auth: tuple = None) -> str:
    request = urllib.request.Request(url)
    if not headers or (headers and "User-Agent" not in headers):
        request.add_header("User-Agent", _default_user_agent)
    if headers:
        for key, value in headers.items():
            if value:
                request.add_header(key, value)
    if auth:
        request.add_header(*basicAuthHeader(auth))

    response = urllib.request.urlopen(request)
    charset = response.info().get_param('charset')
    content = response.read().decode(charset or 'utf-8')
    return content


def save(filepath: str, content: str):
    if not os.path.isdir(_tmp_dir):
        os.makedirs(_tmp_dir)

    with open(filepath, 'w') as f:
        f.write(content)


def load(filepath: str) -> str | None:
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
    path = os.path.join(_tmp_dir, hash.hexdigest())
    return path


def fetch(url: str, headers: dict = None, auth: tuple = None) -> str:
    filepath = path(url)
    content = load(filepath)
    if not content:
        content = get(url, headers=headers, auth=auth)
        save(filepath, content)
    return content


class Cache:
    def __init__(self):
        self.refresh_details()

    def refresh_details(self) -> list:
        global _tmp_dir

        self.details = [
            {
                "path":     os.path.join(_tmp_dir, filename),
                "size":     os.path.getsize(os.path.join(_tmp_dir, filename)),
                "updated":  max(
                    os.path.getctime(os.path.join(_tmp_dir, filename)),
                    os.path.getmtime(os.path.join(_tmp_dir, filename))
                )
            }
            for filename in os.listdir(_tmp_dir)
            if os.path.isfile(os.path.join(_tmp_dir, filename))
        ]
        self.details.sort(key=lambda x: x["updated"])
        self.size = sum(file["size"] for file in self.details)

    def free(self):
        to_be_freed = self.size - cache_size_in_MB * 10**6
        if to_be_freed > 0:
            for file in self.details:
                os.remove(file["path"])
                to_be_freed -= file["size"]
                if to_be_freed <= 0:
                    break


cache = Cache()

if __name__ == '__main__':
    print(f'cache location: "{_tmp_dir}"')
    cache.free()
    print(
        f"cache size: {cache.size:,} / {cache_size_in_MB * 10**6:,.0f} bytes, {len(cache.details)} files")
    print(f'user agent: "{_default_user_agent}"')
