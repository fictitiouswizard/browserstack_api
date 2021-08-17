import requests

from browserstack_api import Settings


class UploadResponse:
    def __init__(self, app_url=None, custom_id=None, shareable_id=None):
        self.app_url = app_url
        self.custom_id = custom_id
        self.shareable_id = shareable_id


class UploadedApp:
    def __init__(self, app_name=None, app_version=None, app_url=None, app_id=None,
                 uploaded_at=None, custom_id=None, shareable_id=None):
        self.app_name = app_name
        self.app_version = app_version
        self.app_url = app_url
        self.app_id = app_id
        self.uploaded_at = uploaded_at
        self.custom_id = custom_id
        self.shareable_id = shareable_id


class AppsApi:

    @staticmethod
    def upload_app(file=None, url=None, custom_id=None):
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
            response = requests.post(api_url, files=files, data=params, **Settings.request())
        else:
            response = requests.post(api_url, data=params, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            return UploadResponse(rj["app_url"], rj["custom_id"], rj["shareable_id"])
        else:
            raise Exception("Invalid Status Code")

    @staticmethod
    def uploaded_apps(custom_id=None):
        api_url = f"{Settings.base_url}/app-automate/recent_apps"

        if custom_id is not None:
            api_url = f"{api_url}/{custom_id}"

        response = requests.get(api_url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            return [
                UploadedApp(
                    app_name=app["app_name"],
                    app_version=app["app_version"],
                    app_url=app["app_url"],
                    app_id=app["app_id"],
                    uploaded_at=app["uploaded_at"],
                    custom_id=app["custom_id"],
                    shareable_id=app["shareable_id"]
                )
                for app
                in rj.json()
            ]
        else:
            raise Exception("Invalid Status Code")

    @staticmethod
    def uploaded_apps_by_group():
        url = f"{Settings.base_url}/app-automate/recent_group_apps"

        response = requests.get(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            return [
                UploadedApp(
                    app_name=app["app_name"],
                    app_version=app["app_version"],
                    app_url=app["app_url"],
                    app_id=app["app_id"],
                    uploaded_at=app["uploaded_at"],
                    custom_id=app["custom_id"],
                    shareable_id=app["shareable_id"]
                )
                for app
                in rj.json()
            ]
        else:
            raise Exception("Invalid Status Code")

    @staticmethod
    def delete_app(app_id):
        if app_id is None:
            raise ValueError("Must enter an app id")

        url = f"{Settings.base_url}/app-automate/app/delete/{app_id}"

        response = requests.delete(url, **Settings.request())

        if response.status_code == 200:
            rj = response.json()
            if rj["success"] is True:
                return True
            else:
                return False
        else:
            raise Exception("Invalid Status Code")
