from datetime import datetime
import bsapi


class MediaUploadResponse:
    """
    Response from BrowserStack when uploading a media file

    :param str media_url: Unique ID returned from BrowserStack to be used in tests
    :param str custom_id: Custom ID defined on upload
    :param str shareable_id: Allows members of other teams to use your media files in their tests
    """
    def __init__(self, media_url=None, custom_id=None, shareable_id=None):
        self.media_url = media_url
        self.custom_id = custom_id
        self.shareable_id = shareable_id

    @staticmethod
    def from_hash(rj):
        return MediaUploadResponse(
            media_url=rj["media_url"] if "media_url" in rj else None,
            custom_id=rj["custom_id"] if "custom_id" in rj else None,
            shareable_id=rj["shareable_id"] if "shareable_id" in rj else None
        )


class MediaFile:
    """
    BrowserStack Media file

    :param str media_name: Name of the uploaded media file
    :param str media_url: Unique ID returned from BrowserStack to use in tests
    :param str media_id: Unique BrowserStack ID
    :param datetime uploaded_at: Time the file was uploaded in utc
    :param str custom_id: Custom ID set during uploaded
    :param str shareable_id: Shareable ID allows members of other teams to use the media file in their tests
    """
    def __init__(self, media_name=None, media_url=None, media_id=None, uploaded_at=None, custom_id=None,
                 shareable_id=None):
        self.media_name = media_name
        self.media_url = media_url
        self.media_id = media_id
        self.uploaded_at = uploaded_at
        self.custom_id = custom_id
        self.shareable_id = shareable_id

    @staticmethod
    def from_hash(rj):
        uploaded_at = None
        if "uploaded_at" in rj:
            uploaded_at = datetime.strptime(rj["uploaded_at"], "%Y-%m-%d %H:%M:%S %Z")

        return MediaFile(
            media_name=rj["media_file"] if "media_file" in rj else None,
            media_url=rj["media_url"] if "media_url" in rj else None,
            media_id=rj["media_id"] if "media_id" in rj else None,
            uploaded_at=uploaded_at,
            custom_id=rj["custom_id"] if "custom_id" in rj else None,
            shareable_id=rj["shareable_id"] if "shareable_id" in rj else None
        )

    def delete(self):
        """
        Delete the media file from BrowserStack

        Example::

            media_files = MediaApi.recent_files()
            for media_file in media_files:
                media_file.delete()

        :return: True/False
        :rtype: bool
        """
        return MediaApi.delete(self.media_id)


class MediaApi(bsapi.Api):

    @staticmethod
    def upload_file(filename=None, custom_id=None):
        """
        Upload a media file to BrowserStack for use in tests

        Example::

            upload_file_response = MediaApi("MyMedia.jpg", "MyTestFile")
            print(upload_file_response.media_url)

        :param filename: File to upload
        :param custom_id: Custom ID for file
        :return: Response object from BrowserStack
        :rtype: :class:`MediaUploadResponse`
        """
        if filename is None:
            raise ValueError("Filename is required")

        url = f"{bsapi.Settings.base_url}/app-automate/upload-media"
        files = {"file": open(filename, "rb")}
        params = {}
        if custom_id is not None:
            params["custom_id"] = custom_id
        response = MediaApi.http.post(url, files=files, data=params, **bsapi.Settings.request())

        if response.status_code == 200:
            rj = response.json()
            return MediaUploadResponse.from_hash(rj)
        else:
            response.raise_for_status()

    @staticmethod
    def recent_files(custom_id=None):
        """
        Get the most recently uploaded media file from BrowserStack.  If custom_id is set it will only return items with
        that custom_id

        Example::

            media_files = MediaApi.recent_files()
            for media_file in media_files:
                print(media_file.media_name)

        :param custom_id: Custom ID set during upload
        :return: A list of media files
        :rtype: list[:class:`MediaFile`]
        """
        if custom_id is None:
            custom_id_segment = ""
        else:
            custom_id_segment = f"/{custom_id}"

        url = f"{bsapi.Settings.base_url}/app-automate/recent_media_files{custom_id_segment}"
        response = MediaApi.http.get(url, **bsapi.Settings.request())

        if response.status_code == 200:
            rj = response.json()
            return [
                MediaFile.from_hash(mf)
                for mf
                in rj
            ]
        else:
            response.raise_for_status()

    @staticmethod
    def recent_group_media():
        """
        Retrieve the list of recently uploaded media files for the entire group

        Example::

            media_files = MediaApi.recent_group_media()
            for media_file in media_files:
                print(media_file.shareable_id)

        :return: A list of media files
        :rtype: list[:class:`MediaFile`]
        """
        url = f"{bsapi.Settings.base_url}/app-automate/recent_group_media"
        response = MediaApi.http.get(url, **bsapi.Settings.request())

        if response.status_code == 200:
            rj = response.json()
            return [
                MediaFile.from_hash(mf)
                for mf
                in rj
            ]
        else:
            response.raise_for_status()

    @staticmethod
    def delete(media_id=None):
        """
        Delete the uploaded media file from BrowserStack

        :param media_id: Unique ID of the media file
        :return: True/False
        :rtype: bool
        """
        if media_id is None:
            raise ValueError("Media ID is required")

        url = f"{bsapi.Settings.base_url}/app-automate/custom_media/delete/{media_id}"
        response = MediaApi.http.delete(url, **bsapi.Settings.request())

        if response.status_code == 200:
            rj = response.json()
            return rj["success"]
        else:
            response.raise_for_status()
