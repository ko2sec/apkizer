# apkizer

**apkizer** collects all available versions of an Android application from apkpure.com

# Purpose

Sometimes mobile applications can be useful to dig into more endpoints, credentials, sensitive data, etc.. of a target. Older versions of a mobile application can be surprisingly more generous of these kind of data. Apkizer can be combined with [apktool](https://ibotpeaches.github.io/Apktool/) for decompiling and static analysis purposes.


# Installation

Install python3 or above to run apkizer.

```
git clone https://github.com/ko2sec/apkizer.git

pip3 install -r requirements.txt
```

# Usage

`python3 apkizer.py -p com.twitter.android `

Use this command to get all available versions of Twitter android application under com.twitter.android directory.


# Known Issues

- apkpure.com is behind Cloudflare to protect website for some kind of attacks. I used [Cloudscraper](https://github.com/VeNoMouS/cloudscraper) which is a library to bypass Cloudflare's I'm Under Attack Mode (IUAM). Sometimes it cannot bypass Cloudflare properly and fails to fetch web page, so I designed it to try multiple times until it can bypass.

- Some APK's have varieties in terms of architecture like arm or x86, for now it downloads the first one it crawls. It may change in future releases depending on the feedback.

# Feedback

Please use [Issues](https://github.com/ko2sec/apkizer/issues) section for bugs and feature requests. If you want to contact for another subjects you can send DM [@ko2sec](https://github.com/ko2sec/apkizer/issues).