import os

import boto3
import requests
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += "HIGH:!DH:!aNULL"

try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += (
        "HIGH:!DH:!aNULL"
    )
except AttributeError:
    # no pyopenssl support used / needed / available
    pass

AWS_KEY = os.environ.get("AWS_KEY", "")
AWS_SECRET = os.environ.get("AWS_SECRET", "")
SPACE_NAME = os.environ.get("SPACE_NAME", "")
SPACE_ENDPOINT = os.environ.get("SPACE_ENDPOINT", "")
SPACE_REGION = os.environ.get("SPACE_REGION", "")


def download_ehentai_images(link, name, start_index):
    session = boto3.session.Session()
    client = session.client(
        "s3",
        region_name=SPACE_REGION,
        endpoint_url=SPACE_ENDPOINT,
        aws_access_key_id=AWS_KEY,
        aws_secret_access_key=AWS_SECRET,
    )

    folder = f"ehen/{name}"

    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/53.0.2785.143 Safari/537.36"
    }

    cookies = {
        "igneous": "df5b575f2",
        "ipb_member_id": "4144232",
        "ipb_pass_hash": "100f840c16e5cc30e4c2f45f4a88aacd",
        "sk": "62s68l4isdarb58lnmd5asj9kq07",
        "yay": "louder",
    }
    request_params = {"headers": headers, "cookies": cookies, "verify": False}

    res = requests.get(link, **request_params)

    soup = BeautifulSoup(res.content, "html.parser")

    pages = soup.find("table", {"class": "ptt"})
    tds = pages.find_all("td")
    page_length = len(tds) - 2
    main = soup.find("div", {"id": "gdt"})
    imgs = main.find_all("a")
    alist = []
    index = 1

    for a in imgs:
        if start_index and (index <= int(start_index)):
            start_index = int(start_index)
            index += 1
            continue
        res = requests.get(a["href"], **request_params)
        file = BeautifulSoup(res.content, "html.parser")
        imgs = file.find("div", {"id": "i3"})
        img = imgs.find("img")
        alist.append(img["src"])
        r = requests.get(img["src"], **request_params)
        if r.status_code == 200:
            file_name = str(index) + ".jpg"
            client.put_object(
                Bucket=SPACE_NAME,
                Key=f"{folder}/{file_name}",
                Body=r.content,
                ACL="private",
            )

        index += 1

    if page_length > 1:
        current_page = 1
        while current_page < page_length:
            res = requests.get(link + "?p=" + str(current_page), **request_params)
            soup = BeautifulSoup(res.content, "html.parser")
            main = soup.find("div", {"id": "gdt"})
            imgs = main.find_all("a")
            for a in imgs:
                if (start_index) and (index <= start_index):
                    index += 1
                    continue
                res = requests.get(a["href"], **request_params)
                file = BeautifulSoup(res.content, "html.parser")
                imgs = file.find("div", {"id": "i3"})
                img = imgs.find("img")
                alist.append(img["src"])
                r = requests.get(img["src"], **request_params)
                if r.status_code == 200:
                    file_name = str(index) + ".jpg"
                    client.put_object(
                        Bucket=SPACE_NAME,
                        Key=f"{folder}/{file_name}",
                        Body=r.content,
                        ACL="private",
                    )
                index += 1
            current_page += 1

    return True
