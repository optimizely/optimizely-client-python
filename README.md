Optimizely Python Client
=================

Optimizely's Python client library is an interface to its [REST API](http://developers.optimizely.com/rest/).


Usage
-----

Set your API key and you're ready to go!
```python
   >>> import optimizely
   >>> client = optimizely.Client('abcdefghijklmnopqrstuvwxyz:123456')
   
   >>> projects = client.Projects.get()
   >>> projects
   # [<optimizely.resource.Project object at 0x000000000>, <optimizely.resource.Project object at 0x000000010>]
   
   >>> my_project = projects[0]
   >>> my_project.project_name
   # 'My Project'
   
   >>> my_project.project_name = 'My Project (Updated)'
   >>> my_project.save()
   
```
