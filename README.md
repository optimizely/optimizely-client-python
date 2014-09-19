Optimizely Python Client
=================

Optimizely's Python client library is an interface to its [REST API](http://developers.optimizely.com/rest/).


Usage
-----

Set your API key and you're ready to go!
```python
   >>> import optimizely
   >>> optimizely.api_key = 'abcdefghijklmnopqrstuvwxyz:123456'
   >>> optimizely.Project.all()
   [
      {
        "code_revision": 8,
        "installation_verified": true,
        "project_name": "My new project",
        "ip_filter": null,
        "ip_anonymization": false,
        "created": "2014-04-14T23:09:03.429630Z",
        "library": "jquery-1.6.4-trim",
        "last_modified": "2014-05-21T23:03:06.968520Z",
        "project_status": "Active",
        "include_jquery": true,
        "js_file_size": 46176,
        "id": 819000157,
        "code_last_modified": "2014-05-21T23:03:04.918880Z",
        "account_id": 555650815
      },
      {
        "code_revision": 12,
        "installation_verified": null,
        "project_name": "My even newer project name",
        "ip_filter": "1.2.3.4",
        "ip_anonymization": false,
        "created": "2014-04-16T21:33:34.408430Z",
        "library": "jquery-1.6.4-trim",
        "last_modified": "2014-06-10T22:12:21.707170Z",
        "project_status": "Active",
        "include_jquery": false,
        "js_file_size": 23693,
        "id": 859720118,
        "code_last_modified": "2014-06-10T22:12:20.615820Z",
        "account_id": 555650815
      }
    ]
```