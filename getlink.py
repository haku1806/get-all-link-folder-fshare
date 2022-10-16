###
# Get link fshare
# 
# Auth: haku1806
#  
###

from base64 import encode
import requests
import datetime

def is_file(data):
    if data['size'] == 0 and data['pid'] == None:
        return False
    return True

def get_link(foledr_id, folder_path = "", page = 1, per_page = 50):
    url = f"https://www.fshare.vn/api/v3/files/folder?linkcode={foledr_id}&sort=type,name&page={page}&per-page={per_page}"
    
    payload={}
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "vi-VN,vi",
        "referer": f"https://www.fshare.vn/folder/{foledr_id}",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response.json())
    data = response.json()
    print(f"Dang lay du lieu trong folder: {data['current']['name']} \t PATH: {data['current']['path']}")
    
    # Check item not exists
    if len(data['items']) != 0:
        for item in data['items']:
            if not is_file(item):
                get_link(item['linkcode'], data['current']['path'])
            else:
                out_put = f"https://www.fshare.vn/file/{item['linkcode']}|{item['name']}|{data['current']['path']}"
                print(out_put)
                with open(file_name, 'a', encoding="utf-8") as f:
                    f.write(f"{out_put}\n")
        if 'next' in data['_links']:
            print("Next")
            list_next = data['_links']['next'].split('&')
            page_next = int(list_next[-2].split('=')[1])
            per_page_next = int(list_next[-1].split('=')[1])
            get_link(foledr_id, data['current']['path'], page_next, per_page_next)
    else:
        return

if __name__ == '__main__':
    folder = input("Nhap folder can lay link: ")
    folder_id = folder.split('/')[4].split('?')[0]
    list_link = []
    print(folder_id)
    file_name = datetime.datetime.now().strftime("data\\%Y%m%d_%H%M%S.txt")
    get_link(folder_id)
    print("Done. Vui long kiem tra file " + file_name)
    