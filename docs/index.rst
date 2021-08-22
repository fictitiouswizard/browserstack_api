.. bsapi documentation master file, created by
   sphinx-quickstart on Thu Aug 19 14:50:39 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

BSAPI the BrowserStack REST API Client
--------------------------------------


Get the logs from a BrowserStack session

.. code-block:: python

   from appium import webdriver

   username = os.getenv("browserstack_username")
   key = os.getenv("browserstack_key")

   desired_caps = {
       "build": "Python Android",
       "device": "Samsung Galaxy S8 Plus",
       "app": "<your app url>"
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


Upload an application to BrowserStack

.. code-block:: python

   app = AppsApi.upload_app("MyApp.apk")


Get the badge key for a project

.. code-block:: python

   projects = ProjectsApi.recent_projects()
   project = [p for p in projects if p.name == "My Project"][0]
   badge_key = ProjectsApi.get_badge_key(project.project_id)
   badge_markdown = f"[![BrowserStack Status](https://app-automate.browserstack.com/badge.svg?badge_key=<badge_key>)](https://app-automate.browserstack.com/public-build/{badge_key}?redirect=true)"



.. toctree::
   :maxdepth: 2
   :caption: Content:

   app_automate/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
