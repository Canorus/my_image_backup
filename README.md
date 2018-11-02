# Back up your purchased history

eee|bay deletes images from their server after 60 days from the day of purchase. This code saves images from the server with source code of listing under the name of the item.

## Requirement

- python 3
- selenium python package
- bs4 python package
- [chromedriver](http://chromedriver.chromium.org/downloads), included is version 2.35.528157 

## Others

You'll need to adjust the code to your environment. i.e. your account, password, location of chrome driver, location to save resources.

**FYI, this code saves your credential data in unencrypted way. So if you think this might be dangerous, I'm sorry. You'll have to find other way.**

Use it with cron, or launchd to run regularly.

This code is subject to changes on server. I can't guarantee this code will make it to run forever.
