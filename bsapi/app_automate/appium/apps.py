from bsapi import Settings, Api


class UploadResponse:
    """
    The response from uploading an app

    :var str app_url: The url for the app to use with appium
    :var str custom_id: The custom id that was set during upload
    :var str shareable_id: The shareable id for the app
    """
    def __init__(self, app_url=None, custom_id=None, shareable_id=None):
        self.app_url = app_url
        self.custom_id = custom_id
        self.shareable_id = shareable_id


class UploadedApp:
    """
    An app that has been uploaded to BrowserStack

    :var str app_name: Filename of the app
    :var str app_version: Version of the uploaded app
    :var str app_url: The url for the app to use with appium
    :var str app_id: Unique id for the app
    :var str uploaded_at: When the app was uploaded
    :var str custom_id: Custom ID that was defined for the app
    :var str shareable_id: Shareable ID allows other users to test an app you uploaded
    """
    def __init__(self, app_name=None, app_version=None, app_url=None, app_id=None,
                 uploaded_at=None, custom_id=None, shareable_id=None):
        self.app_name = app_name
        self.app_version = app_version
        self.app_url = app_url
        self.app_id = app_id
        self.uploaded_at = uploaded_at
        self.custom_id = custom_id
        self.shareable_id = shareable_id


class AppsApi(Api):
    """
    Class for interacting with the Apps REST endpoint
    """

    @classmethod
    def upload_app(cls, file=None, url=None, custom_id=None):
        """
        Upload an application file to BrowserStack.  File or url must be set but not both.

        Example::

            uploaded_app = AppsApi.upload_app("MyApp.apk", custom_id="MyApplication")

        :param file: The file to be uploaded to Browserstack
        :type file: str
        :param url: Public url for the app to be uploaded from
        :type url: str
        :param custom_id: Custom Identifier
        :type custom_id: str
        :return: The response from the server including the app url, custom id, and shareable id
        :rtype: :class:`bsapi.app.automate.appium.apps.UploadResponse`
        :raises ValueError: file or url are required but not both
        """
        api_url = f"{Settings.base_url}/app-automate/upload"

        if file is not None and url is not None:
            raise ValueError("Must use file or url not both")
        if file is None and url is None:
            raise ValueError("Must use file or url")

        params = {}
        if url is not None:
            params["url"] = url
        if custom_id is not None:
            params["custom_id"] = custom_id
        if file is not None:
            files = {"file": open(file, "rb")}
            response = cls.http.post(api_url, files=files, data=params, **Settings.request())
        else:
            response = cls.http.post(api_url, data=params, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            return UploadResponse(
                app_url=rj["app_url"] if "app_url" in rj else None,
                custom_id=rj["custom_id"] if "custom_id" in rj else None,
                shareable_id=rj["shareable_id"] if "shareable_id" in rj else None
            )
        else:
            response.raise_for_status()

    @classmethod
    def uploaded_apps(cls, custom_id=None):
        """
        Return all of the uploaded apps for a custom id.  If no custom id is supplied all apps are returned

        Example::

            apps = AppsApi.uploaded_apps("MyApplication")

        :param custom_id: The custom id used with the app was uploaded
        :type custom_id: str
        :return: A list of uploaded apps
        :rtype: list[:class:`bsapi.app_automate.appium.apps.UploadedApp`]
        """
        api_url = f"{Settings.base_url}/app-automate/recent_apps"

        if custom_id is not None:
            api_url = f"{api_url}/{custom_id}"

        response = cls.http.get(api_url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()

            if "message" in rj:
                if rj["message"] == "No results found":
                    return []

            return [
                UploadedApp(
                    app_name=app["app_name"] if "app_name" in app else None,
                    app_version=app["app_version"] if "app_version" in app else None,
                    app_url=app["app_url"] if "app_url" in app else None,
                    app_id=app["app_id"] if "app_id" in app else None,
                    uploaded_at=app["uploaded_at"] if "uploaded_at" in app else None,
                    custom_id=app["custom_id"] if "custom_id" in app else None,
                    shareable_id=app["shareable_id"] if "shareable_id" in app else None
                )
                for app
                in rj
            ]
        else:
            response.raise_for_status()

    @classmethod
    def uploaded_apps_by_group(cls):
        """
        Get the uploaded apps for your group

        Example::

            apps = AppsApi.uploaded_apps_by_group()

        :return: Returns an list of uploaded apps
        :rtype: list[:class:`bsapi.app_automate.appium.apps.UploadedApp`]
        """
        url = f"{Settings.base_url}/app-automate/recent_group_apps"

        response = cls.http.get(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()

            if "message" in rj:
                if rj["message"] == "No results found":
                    return []

            return [
                UploadedApp(
                    app_name=app["app_name"] if "app_name" in app else None,
                    app_version=app["app_version"] if "app_version" in app else None,
                    app_url=app["app_url"] if "app_url" in app else None,
                    app_id=app["app_id"] if "app_id" in app else None,
                    uploaded_at=app["uploaded_at"] if "uploaded_at" in app else None,
                    custom_id=app["custom_id"] if "custom_id" in app else None,
                    shareable_id=app["shareable_id"] if "shareable_id" in app else None
                )
                for app
                in rj
            ]
        else:
            response.raise_for_status()

    @classmethod
    def delete_app(cls, app_id):
        """
        Delete the app from BrowserStack

        Example::

            apps = AppsApi.uploaded_apps()
            if len(apps) > 0:
                app = apps[0]
                response = AppsApi.delete_app(app.app_id)
                if response:
                    print("The app was deleted")

        :param str app_id: App ID of the uploaded app
        :return: True/False
        :rtype: bool
        """
        if app_id is None:
            raise ValueError("Must enter an app id")

        url = f"{Settings.base_url}/app-automate/app/delete/{app_id}"

        response = cls.http.delete(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            if rj["success"] is True:
                return True
            else:
                return False
        else:
            response.raise_for_status()
