Optimizely Python Client
=================

Optimizely's Python client library is an interface to its [REST API](http://developers.optimizely.com/rest/).


Usage
-----

Set your API key and you're ready to go!
```python
   >>> import optimizely
   >>> optimizely.api_key = 'abcdefghijklmnopqrstuvwxyz:123456'
   >>> projects = optimizely.Project.list()
   >>> projects
   [<Project object with ID: 12345>]
   
   >>> my_project = projects[0]
   >>> my_project.project_name
   u'My Project'
   
   >>> my_project = optimizely.Project.update(12345, {'project_name': 'My Project (Updated)'})
   >>> my_project.project_name
   u'My Project (Updated)'
   
```