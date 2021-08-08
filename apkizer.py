# apkizer coded by ko2sec

import requests
import bs4
import argparse
from requests.models import Response
import cloudscraper
import os


def main():
    parser = argparse.ArgumentParser(description='Download all versions of an Android mobile application from apkpure.com')
    required = parser.add_argument_group('required arguments')
    required.add_argument('-p', required=True, metavar="packagename", help="example: com.twitter.android")
    args = parser.parse_args()

    scraper = cloudscraper.create_scraper(delay=10) 
    base_url = "https://apkpure.com"
    package_name = args.p
    package_url = ""
    download_version_list = []
    response = scraper.get("https://apkpure.com/tr/search?q=" + package_name).text

    soup = bs4.BeautifulSoup(response, "html.parser")
    a_elements = soup.find_all("a")

    for element in a_elements:
        #print(element.attrs["href"])
        if "href" in element.attrs and element.attrs["href"] != None and package_name in element.attrs["href"]:
            if "/" in element.attrs["href"] and element.attrs["href"].split("/")[-1] == package_name:
                package_url = element.attrs["href"]             
    
    if package_url == "":
        if "Cloudflare Ray ID" in response:
            print("Cloudflare protection could not be bypassed, trying again..")
            main()
        else:
            print("Package not found!")

        return

    """
    Here is full URL correlated with package name.
    """

    response = scraper.get(base_url + package_url + "/versions").text
    soup = bs4.BeautifulSoup(response, "html.parser")

    versions_elements_div = soup.find("ul", attrs={"class":"ver-wrap"})
    versions_elements_li = versions_elements_div.findAll("li", recursive=False)

    for list_item in versions_elements_li:
        download_version_list.append(list_item.find("a").attrs["href"])

    """
    Make a list of download pages.
    """

    def download_apk(download_page):
        soup = bs4.BeautifulSoup(download_page, "html.parser")
        download_link = soup.find("iframe", {"id": "iframe_download"}).attrs["src"]
        filename = soup.find("span", {"class": "file"}).text.rsplit(' ', 2)[0].replace(" ", "_").lower()
        print(filename + " is downloading, please wait..")
        file = scraper.get(download_link)
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, package_name)

        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
        open(os.path.join(package_name, filename), "wb").write(file.content)


    for apk_url in download_version_list:
        download_page = scraper.get(base_url + apk_url).text
        if "Download Variant XAPKS" in download_page:
            """
            There are sometimes APK variants in terms of architecture,
            we need to analyze it before getting download link.
            Getting first variant for now.
            """
            soup = bs4.BeautifulSoup(download_page, "html.parser")
            apk_url = soup.find("div", {"class": "table-cell down"}).find("a").attrs["href"]
            download_page = scraper.get(base_url + apk_url).text
        download_apk(download_page)
    print("All APK's are downloaded!")

def banner():
    print("""
    
               _     _                 
              | |   (_)                
  __ _  _ __  | | __ _  ____ ___  _ __ 
 / _` || '_ \ | |/ /| ||_  // _ \| '__|
| (_| || |_) ||   < | | / /|  __/| |   
 \__,_|| .__/ |_|\_\|_|/___|\___||_|   
       | |                             
       |_|                             
                    by ko2sec, v1.0
    """)
    main()
banner()