from pprint import pprint
import json
import os 

from streamfile import WebNavigator

def collect_urls():
    # url = "https://xadrezverbal.com/xadrez-verbal-podcast-2/"
    base_url = "https://xadrezverbal.com/category/audio/page"
    fronteiras_regex = '.*\d{1,4}/\d{1,2}/\d{1,2}/fronteiras-invisiveis-do-futebol-\d{1,3}'
    xv_regex = '.*\d{1,4}/\d{1,2}/\d{1,2}/xadrez-verbal-podcast-\d{1,3}'

    web = WebNavigator()
    out= []
    for i in range(1,100):
        url = f"{base_url}/{i}"
        print(f"{i} : {url}")
        web.start_session(url)
        out.extend(web.find_links_by_regex(
            regex='.*\d{1,4}/\d{1,2}/\d{1,2}/fronteiras-invisiveis-do-futebol-\d{1,3}'))
        web.driver.implicitly_wait(2)
        print(len(out))

    web.teardown()
    pprint(set(out))
    
    data_path = os.path.dirname(os.path.abspath(__file__))
    save = {"fronteiras_invisiveis": list(set(out))}
    with open(f'{data_path}/data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data.update({'fronteiras_invisiveis': list(set(out))})
    
    with open(f'{data_path}/data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
def download_ep():
    data_path = os.path.dirname(os.path.abspath(__file__))
    with open(f'{data_path}/data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    web = WebNavigator()
    out = []
    for i, item in enumerate(data["xadrez_verbal"]):
        print(i, item)
        web.start_session(item)
        out.extend(web.find_links_by_regex(
            regex='.*mp3.*'))
        print(len(out))
        web.driver.implicitly_wait(2)

    pprint(set(out))
    web.teardown()

    with open(f'{data_path}/episodes_xadrezverbal.json', 'w', encoding='utf-8') as f:
        json.dump(list(set(out)), f, ensure_ascii=False, indent=4)


if __name__=="__main__":
#    collect_urls()
    download_ep()