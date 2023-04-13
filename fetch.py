import urllib.request
import tempfile
import hashlib
import datetime
import os
import base64
from sys import version_info


expiry_seconds: int = 600
cache_size_in_MB: float = 5

__tmp_dir = os.path.join(tempfile.gettempdir(), "fetchpy-cache")
__default_user_agent = f"python{version_info.major}.{version_info.minor} urllib"


def basicAuthHeader(credentials: tuple) -> tuple:
    user_name, password = credentials
    raw_token = f"{user_name}:{password}"
    base64string = base64.b64encode(raw_token.encode()).decode()
    return "Authorization", f"Basic {base64string}"


def get(url: str, headers: dict = None, auth: tuple = None) -> str:
    request = urllib.request.Request(url)
    if not headers or (headers and "User-Agent" not in headers):
        request.add_header("User-Agent", __default_user_agent)
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
    path = os.path.join(__tmp_dir, hash.hexdigest())
    return path


def fetch(url: str, headers: dict = None, auth: tuple = None) -> str:
    filepath = path(url)
    content = load(filepath)
    if not content:
        content = get(url, headers=headers, auth=auth)
        save(filepath, content)
    return content


def cache_list() -> list:
    details = [
        {
            "path":     os.path.join(__tmp_dir, filename),
            "size":     os.path.getsize(os.path.join(__tmp_dir, filename)),
            "updated":  max(
                            os.path.getctime(os.path.join(__tmp_dir, filename)),
                            os.path.getmtime(os.path.join(__tmp_dir, filename))
                        )
        }
        for filename in os.listdir(__tmp_dir)
        if os.path.isfile(os.path.join(__tmp_dir, filename))
    ]
    details.sort(key = lambda x: x["updated"])
    return details


def free_cache():
    to_be_freed = cache_usage() - cache_size_in_MB * 10**6
    if to_be_freed > 0:
        for file in cache_list():
            os.remove(file["path"])
            to_be_freed -= file["size"]
            if to_be_freed <= 0:
                break


def cache_usage() -> int:
    file_sizes = (file["size"] for file in cache_list())
    return sum(file_sizes)


if __name__ == '__main__':
    print(f'cache location: "{__tmp_dir}"')
    free_cache()
    print(f"cache size: {cache_usage():,} / {cache_size_in_MB * 10**6:,.0f} bytes")
    print(f'user agent: "{__default_user_agent}"')

