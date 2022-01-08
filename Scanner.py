#!/usr/bin/env python
from socket import*
import os
import time
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
baslangicZamani=time.time()
os.system("figlet SOFTWARE BLOGER")
print("""
Web Analiz Aracı
softwarebloger.com

[1] Hızlı tarama
[2] Detaylı tarama
[3] Sql taraması
[4] Web dosya/dizin listeleme
[5] Subdomain bulma

""")
metin="Hedef IP veya URL giriniz: "
islem=input("Yapılacak işlemi numarasını giriniz: ")
try:
    if islem == "1":
        target =input('Taranacak IP veya URL giriniz(Örnek Kullanım: xxxx.com): ')
        t_IP = gethostbyname(target)
        print ('Taranmaya başlanan IP: ', t_IP)
        for i in range(1, 500):
            s = socket(AF_INET, SOCK_STREAM)
            conn = s.connect_ex((t_IP, i))
            if(conn == 0) :
                print ('Port %d: OPEN(ACIK)' % (i,))
            s.close()
        print('Geçen Süre:', time.time() - baslangicZamani)
    elif islem=="2":
        hIP=input(metin)
        os.system("nmap -sS -sV -O "+ hIP)
    elif islem=="3":
        acikSQL= input(metin)
        os.system("sqlmap -u " + acikSQL + " --dbs --random-agent")
    elif islem == "4":
        colorama.init()
        GREEN = colorama.Fore.GREEN
        GRAY = colorama.Fore.LIGHTBLACK_EX
        RESET = colorama.Fore.RESET
        internal_urls = set()
        external_urls = set()
        def is_valid(url):
            parsed = urlparse(url)
            return bool(parsed.netloc) and bool(parsed.scheme)
        def get_all_website_links(url):
            urls = set()
            domain_name = urlparse(url).netloc
            soup = BeautifulSoup(requests.get(url).content, "html.parser")
            for a_tag in soup.findAll("a"):
                href = a_tag.attrs.get("href")
                if href == "" or href is None:
                    continue
                href = urljoin(url, href)
                parsed_href = urlparse(href)
                href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
                if not is_valid(href):
                    continue
                if href in internal_urls:
                    continue
                if domain_name not in href:
                    if href not in external_urls:
                        print(f"{GRAY}[!] External link: {href}{RESET}")
                        external_urls.add(href)
                    continue
                print(f"{GREEN}[*] Internal link: {href}{RESET}")
                urls.add(href)
                internal_urls.add(href)
            return urls
        total_urls_visited = 0
        def crawl(url, max_urls=50):
            global total_urls_visited
            total_urls_visited += 1
            links = get_all_website_links(url)
            for link in links:
                if total_urls_visited > max_urls:
                    break
                crawl(link, max_urls=max_urls)
        if __name__ == "__main__":
            print("Örnek Kullanım: https://xxx.com/")
            weblist=input(metin)
            crawl(weblist)
            print("[+] Total External links:", len(external_urls))
            print("[+] Total Internal links:", len(internal_urls))
            print("[+] Total:", len(external_urls) + len(internal_urls))
    elif islem=="5":
        domain = input("Url giriniz: ")
        file = open(input("Subdomain wordlistini giriniz(Örnek Adres:https://github.com/rbsec/dnscan): "))
        content = file.read()
        subdomains = content.splitlines()
        discovered_subdomains = []
        for subdomain in subdomains:
            url = f"http://{subdomain}.{domain}"
            try:
                requests.get(url)
            except requests.ConnectionError:
                pass
            else:
                print("[+] Alt alan adları :", url)
                discovered_subdomains.append(url)
    else:
        print("Hatalı bir giriş yaptını")
except:
    print("Hata gelişti")