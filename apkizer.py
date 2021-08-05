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
    required.add_argument('-p', required=True, metavar="packagename", help="eg. com.google.android.googlequicksearchbox")
    args = parser.parse_args()

    scraper = cloudscraper.create_scraper(delay=10) 
    base_url = "https://apkpure.com"
    package_name = args.p
    package_url = ""
    download_list = []
    response = scraper.get("https://apkpure.com/tr/search?q=" + package_name).text

    soup = bs4.BeautifulSoup(response, "html.parser")
    a_elements = soup.find_all("a")

    for element in a_elements:
        #print(element.attrs["href"])
        if "href" in element.attrs and element.attrs["href"] != None and package_name in element.attrs["href"]:
            if "/" in element.attrs["href"] and element.attrs["href"].split("/")[-1] == package_name:
                package_url = element.attrs["href"]             
    
    if package_url == "":
        print("package not found!")
        print(response)
        return

    """
    Here is full URL correlated with package name.
    """

    response = scraper.get(base_url + package_url + "/versions").text
    soup = bs4.BeautifulSoup(response, "html.parser")

    versions_elements_div = soup.find("ul", attrs={"class":"ver-wrap"})
    versions_elements_li = versions_elements_div.findAll("li", recursive=False)

    for list_item in versions_elements_li:
        download_list.append(list_item.find("a").attrs["href"])
    """
    Make a list of download URLs.
    """

    for apk_url in download_list:
        download_page = scraper.get(base_url + apk_url).text
        soup = bs4.BeautifulSoup(download_page, "html.parser")
        download_link = soup.find("iframe", {"id": "iframe_download"}).attrs["src"]
        filename = soup.find("span", {"class": "file"}).text.rsplit(' ', 2)[0].replace(" ", "_").lower()
        print(filename + " is downloading, please wait..")
        file = scraper.get(download_link)
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, package_name)

        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
        open(package_name + "/" + filename, "wb").write(file.content)

main()