from urllib.parse import urlparse
from threading import Thread
import http.client as httplib
import sys
from queue import Queue
from fake_useragent import UserAgent

concurrent = 50
q = Queue(concurrent * 2)

def menu():
    print("""                                    ██████                                  
                                   ███░░███                                 
 ████████  █████ ████             ░███ ░░░  █████ ████  █████████  █████████
░░███░░███░░███ ░███  ██████████ ███████   ░░███ ░███  ░█░░░░███  ░█░░░░███ 
 ░███ ░███ ░███ ░███ ░░░░░░░░░░ ░░░███░     ░███ ░███  ░   ███░   ░   ███░  
 ░███ ░███ ░███ ░███              ░███      ░███ ░███    ███░   █   ███░   █
 ░███████  ░░███████              █████     ░░████████  █████████  █████████
 ░███░░░    ░░░░░███             ░░░░░       ░░░░░░░░  ░░░░░░░░░  ░░░░░░░░░ 
 ░███       ███ ░███                                                        
 █████     ░░██████                                                         
░░░░░       ░░░░░░                                                          """)
    print("[*] Py-fuzz starting...")
    print("[i] Please, give me some informations.")
    menu.url = str(input("[url] > "))
    menu.wordlist_path = str(input("[wordlist] > "))
    print("[i] Everything i'll find will be shown here.")

def url_test():
    if(menu.url.startswith('http://') or menu.url.startswith('https://')):
        pass
    else:
        menu.url = 'http://' + menu.url
    if(menu.url.endswith('/')):
        pass
    else:
        menu.url = menu.url + '/'

def ua_gen():
    ua = UserAgent()
    return ua.random

def doWork():
    while True:
        url = menu.url + q.get()
        status, url = getStatus(url)
        print_found(status, url)
        q.task_done()

def getStatus(ourl):
    try:
        url = urlparse(ourl)
        conn = httplib.HTTPConnection(url.netloc)   
        conn.request("HEAD", url.path)
        res = conn.getresponse()
        return res.status, ourl
    except:
        return "[DEBUG] error, following url doesn't seems to work. might want to check out.\n", ourl

def print_found(status, url):
    if(status == 200 or status == 301):
        url = url + " "*(40 - len(url))
        print(f"""+----------------------------------------+--------+
|{url}|  {status}   |
""")

def fuzz():
    print("""+========================================+========+
|                   URL                  | Status |
""")
    ua = ua_gen()
    for i in range(concurrent):
        t = Thread(target=doWork)
        t.daemon = True
        t.start()
    try:
        for url in open(menu.wordlist_path):
            q.put(url.strip())
        q.join()
    except KeyboardInterrupt:
        sys.exit(1)

def main():
    menu()
    url_test()
    fuzz()

if __name__ == '__main__':
    main()
