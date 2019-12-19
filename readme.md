

Deploying
=========

This app is running under python3. Some lib are needed:

* python3 (Python 3.6.9)
* django (django 2.0)
* djangorestframework (3.10)
* aapt (Android Asset Packaging Tool, v0.2-27.0.1)



The database engine is sqlite3. You have to create the db.sqlite3 file in famoco/ directory. Once done, execute the migration script to create the app models with
```
$ python manage.py migrate
```
Then create a superuser with
```
$ python manage.py createsuperuser
```

Finally, you can launch the application with
```
$ python manage.py runserver

```

API
====
* Listing the applications
By doing a GET request on localhost:8000/api/list, the returned values will be like
```
[{
    "package_name": "ru.zdevs.zarchiver",
    "package_version_code": "9265",
    "application": "/media/a0b99974-0946-387b-bbc5-20c829d9a3b6.apk"
}, {
    "package_name": "com.whatsapp.",
    "package_version_code": "33",
    "application": "/media/v5dg7j-0946-387b-f3s-3dhfgh78hgm.apk"
}]
```

* Adding Application
By doing a POST request on localhost:8000/api/add
with header "Content-Type application/x-www-form-urlencoded" and its data
- application (required): the APK file
- description (optional): a string with the description


The returned value (if success) will be like
```
{
    "package_name": "ru.zdevs.zarchiver",
    "package_version_code": "9265",
    "application": "/media/a0b99974-0946-387b-bbc5-20c829d9a3b6.apk"
}
```