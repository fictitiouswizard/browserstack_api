# baspi
#### A BrowserStack Rest Api Client

[![Build Status](https://app.travis-ci.com/fictitiouswizard/bsapi.svg?branch=master)](https://app.travis-ci.com/fictitiouswizard/bsapi)
[![Documentation Status](https://readthedocs.org/projects/bsapi/badge/?version=latest)](https://bsapi.readthedocs.io/en/latest/?badge=latest)


Provides wrapper classes for the BrowserStack rest api



## App Automate
___
### Appium
___

Get the logs for a BrowserStack session

```python

import os
from appium import webdriver
from bsapi.app_automate.appium import Session

username = os.getenv("browserstack_username")
key = os.getenv("browserstack_key")

desired_caps = {
    "build": "Python Android",
    "device": "Samsung Galaxy S8 Plus",
    "app": "<your app url>",
    "browserstack.networkLogs": "true",
    "browserstack.deviceLogs": "true",
    "browserstack.appiumLogs": "true",
    "browserstack.video": "true"
}

url = f"https://{username}:{key}@hub-cloud.browserstack.com/wd/hub"

driver = webdriver.Remote(url, desired_caps)
session_id = driver.session_id
driver.quit()

session = Session.by_id(session_id)
session.save_session_logs("session.log")
session.save_appium_logs("appium.log")
session.save_device_logs("device.log")
session.save_network_logs("network.log")
session.save_video("session.mp4")

```

Upload an application to BrowserStack

```python

app = AppsApi.upload_app("MyApp.apk")

```

Get the badge key for a project

```python

projects = ProjectsApi.recent_projects()
project = [p for p in projects if p.name == "My Project"][0]
badge_key = ProjectsApi.get_badge_key(project.project_id)
badge_markdown = f"[![BrowserStack Status](https://app-automate.browserstack.com/badge.svg?badge_key={badge_key})](https://app-automate.browserstack.com/public-build/{badge_key}?redirect=true)"

```