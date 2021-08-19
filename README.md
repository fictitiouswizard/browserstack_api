# baspi
#### The BrowserStack Rest Api Client

Provides wrapper classes for the BrowserStack rest api

## App Automate
___
### Appium
___
### Apps
Upload an app to App Automate for Appium
    
```python
from bsapi.app_automate.appium import AppsApi
    
app = AppsApi.upload_app("MyApp.apk", custome_id="MyApp")
```

Retrieve a list of uploaded apps

```python
from bsapi.app_automate.appium import AppsApi

apps = AppsApi.uploaded_apps()
```


Retrieve the apps uploaded by your group

```python
from bsapi.app_automate.appium import AppsApi

apps = AppsApi.uploaded_apps_by_group()
```

Delete an App

```python
from bsapi.app_automate.appium import AppsApi

apps = AppsApi.uploaded_apps()
app = next(filter(lambda a: a.app_name == "MyApp.apk", apps), None)
response = AppsApi.delete_app(apps[0].app_id)
```

### Projects
Get recent Projects

```python
from bsapi.app_automate.appium import ProjectsApi

projects = ProjectsApi.recent_projects()
```

Get the details for a project

```python
from bsapi.app_automate.appium import ProjectsApi

projects = ProjectsApi.recent_projects()
project = ProjectsApi.details(projects[0].project_id)
```

Update the name of a project
```python
from bsapi.app_automate.appium import ProjectsApi

projects = ProjectsApi.recent_projects()
project_id = [p.project_id for p in projects if p.name == "My Project"][0]
project = ProjectsApi.update_project_name(project_id, "The New Project Name")
```

Retrieve the Badge Key for your project
```python
from bsapi.app_automate.appium import ProjectsApi

projects = ProjectsApi.recent_projects()
project_id = [p.project_id for p in projects if p.name == "My Project"][0]
```

Delete a project

You can not delete a project that have builds associated with it.  They must be removed first.
```python
from bsapi.app_automate.appium import ProjectsApi, BuildsApi

projects = ProjectsApi.recent_projects()
for project in projects:
    if project.builds is None:
        continue

    for build in project.builds:
        BuildsApi.delete(build.hashed_id)
    response = ProjectsApi.delete(project.project_id)
```

### Builds
Get recent builds

```python
from bsapi.app_automate.appium import BuildsApi

builds = BuildsApi.recent_builds()
```

Get the sessions associated with a build

```python
from bsapi.app_automate.appium import BuildsApi

builds = BuildsApi.recent_builds()
sessions = BuildsApi.details(builds[0].hashed_id)
```
    

Delete a build

```python
from bsapi.app_automate.appium import BuildsApi

builds = BuildsApi.recent_builds()
for build in builds:
    response = BuildsApi.delete(build.hashed_id)
```    
    

### Devices
Get a list of supported devices

```python
from bsapi.app_automate.appium import DevicesApi

devices = DevicesApi.get_device_list()
``` 

### Plans
Get information about your App Automate Plan

```python
from bsapi.app_automate.appium import PlansApi

plan = PlansApi.details()
```
    