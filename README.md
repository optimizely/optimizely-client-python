#Optimizely Python Client

##Getting Started
Optimizely's Python client library is an interface to its [REST API](http://developers.optimizely.com/rest/).

The `optimizely` Python module can be installed via `pip` using the command `pip install optimizely`.

###Authentication
The constructor takes in a API key and token type. We support two token types: `oauth` and `legacy`. OAuth refers to a token that was generated via OAuth and legacy is a standard API token, which can be generated from [optimizely.com/tokens](https://www.optimizely.com/tokens). 

`optimizely.Client(api_key, token_type)`

In the following examples, `client` refers to a `Client` object created using the code below.

```python
>>> import optimizely
>>> client = optimizely.Client('abcdefghijklmnopqrstuvwxyz:123456', 'oauth')
```

###Exceptions
If you make a call and it succeeds, data will be included in the returned object(s) (except in the case of deletions, where a `None` response indicates success).

If the call fails, we'll raise one of the following exceptions:

* `BadRequestError` can happen if your request was not sent in valid JSON. The error may reference specific fields that were invalid.

* `UnauthorizedError` if your API token was missing.

* `ForbiddenError` if you provided an API token but it was invalid or revoked, or if you don't have read/write access to the entity you're trying to view/edit.

* `NotFoundError` if the id used in the call was inaccurate or you didn't have permission to view/edit it.

* `TooManyRequestsError` if you hit a rate limit for the API. If you receive this response, we recommend waiting at least 60 seconds before re-attempting the call.

* `ServiceUnavailableError` if the API is overloaded or down for maintenance. If you receive this response, we recommend waiting at least 60 seconds before re-attempting the call.

All of these Exceptions inherit from the `OptimizelyError` class.

##Projects
A project is a collection of experiments, goals, and audiences. Each project has an associated Javascript file to include on the page.

###Read a Project
Get metadata for a single project.

See [the Optimizely REST API documentation](http://developers.optimizely.com/rest/#read-a-project) for response attribute definitions.

####Example Python
```python
>>> project = client.Projects.get(1234) # get Project by Id
>>> project.__dict__
# {
#   'id': 1234,
#   'account_id': 123456789,
#   'code_revision': 12,
#   'project_name': 'My even newer project name',
#   'project_status': 'Active',
#   'created': '2014-04-16T21:33:34.408430Z',
#   'last_modified': '2014-06-10T22:12:21.707170Z',
#   'library': 'jquery-1.6.4-trim',
#   'include_jquery': False,
#   'js_file_size': 23693,
#   'project_javascript': 'someFunction = function () {\n //Do cool reusable stuff \n}'
#   'enable_force_variation': False,
#   'exclude_disabled_experiments': False,
#   'exclude_names': None,
#   'ip_anonymization': False,
#   'ip_filter': '1.2.3.4'
# }
>>> client.Projects.get([1234, 5678])   # get multiple Projects by Id
# [<optimizely.resource.Project object at 0x000000000>, <optimizely.resource.Project object at 0x000000010>]
```

###Create a Project
Create a new project in your account. The `project_name` is required in the call. The [other editable arguments](#update-a-project) are all optional.

####Example Python
```python
>>> project = client.Projects.create({'project_name': 'My new project name'})
>>> project.__dict__
# {
#   'id': 5678,
#   'account_id': 123456789,
#   'code_revision': 0,
#   'project_name': 'My new project name',
#   'project_status': 'Active',
#   'created': '2014-04-16T21:33:34.408430Z',
#   'last_modified': '2014-06-10T22:12:21.707170Z',
#   'library': 'jquery-1.6.4-trim',
#   'include_jquery': True,
#   'js_file_size': None,
#   'project_javascript': None
#   'enable_force_variation': False,
#   'exclude_disabled_experiments': False,
#   'exclude_names': None,
#   'ip_anonymization': False,
#   'ip_filter': ''
# }
```

###Update a Project

Projects can be updated by updating the attributes of a fetched object and calling `save` or by calling `update` on a client and passing in an update dictionary and resource Id.

####Editable Fields
* `project_status`
* `project_name`
* `include_jquery`
* `project_javascript`
* `enable_force_variation`
* `exclude_disabled_experiments`
* `exclude_names`
* `ip_anonymization`
* `ip_filter`

####Example Python
```python
>>> project.project_name = 'My even newer project name'
>>> project.save()
>>> project.__dict__
# {
#   'id': 5678,
#   'account_id': 123456789,
#   'code_revision': 0,
#   'project_name': 'My even newer project name',
#   'project_status': 'Active',
#   'created': '2014-04-16T21:33:34.408430Z',
#   'last_modified': '2014-06-10T22:12:21.707170Z',
#   'library': 'jquery-1.6.4-trim',
#   'include_jquery': True,
#   'js_file_size': None,
#   'project_javascript': None
#   'enable_force_variation': False,
#   'exclude_disabled_experiments': False,
#   'exclude_names': None,
#   'ip_anonymization': False,
#   'ip_filter': ''
# }

# an equivalent call
>>> client.Projects.update(5678, {'project_name': 'My even newer project name'})
```

###Delete a Project
Deleting projects is not supported.

###List Projects in Account
Get a list of all the projects in your account, with associated metadata.

####Example Python
```python
>>> client.Projects.get()  # get all Account's Projects
# [<optimizely.resource.Project object at 0x000000000>, <optimizely.resource.Project object at 0x000000010>, <optimizely.resource.Project object at 0x000000020>]
```

##Experiments
An A/B experiment is a set of rules for matching visitors to content and recording their conversions. Experiments are the hub that connect several other models:

* **Goals** measure conversions and determine a winner.
* **Audiences** determine which visitors will see an experiment.
* **Variations** define the code that should be applied on a page to change the experience for a visitor, and the percentage of visitors who should see that code.

A multivariate experiment also has **Sections**. A section is a collection of variations that all manipulate the same feature of the page.

A multipage experiment adds **Pages**, which manipulate different URLs on your site.

###Read an Experiment
Get metadata for a single experiment.

See [the Optimizely REST API documentation](http://developers.optimizely.com/rest/#read-an-experiment) for response attribute definitions.

####Example Python
```python
>>> experiment = client.Experiments.get(15)
>>> experiment.__dict__
# {
#   'id': 15,
#   'percentage_included': 10000,
#   'display_goal_order_lst': [],
#   'is_multivariate': False,
#   'project_id': 754864960,
#   'variation_ids': [
#     800227656,
#     800227657
#   ],
#   'status': 'Not started',
#   'url_conditions': [
#     {
#       'index': 0,
#       'match_type': 'simple',
#       'created': '2014-04-12T19:10:53.806640Z',
#       'value': 'http://blog.optimizely.com/2014/04/11/10-reasons-why-your-agency-should-offer-optimization/',
#       'last_modified': '2014-04-12T19:10:53.806650Z',
#       'negate': False
#     }
#   ],
#   'description': 'Wordpress: 10 Reasons Why Your Agency Should Offer Optimization ',
#   'last_modified': '2014-04-12T19:10:53.806650Z',
#   'activation_mode': 'immediate',
#   'details': 'Experiment to test out blog post.',
#   'custom_css': '',
#   'created': '2014-04-12T19:10:53.588450Z',
#   'custom_js': '',
#   'primary_goal_id': None,
#   'experiment_type': 'ab',
#   'shareable_results_link': 'https://www.optimizely.com/results?experiment_id=791495413&token=fh3lk2hrlk',
#   'edit_url': 'http://blog.optimizely.com/2014/04/11/10-reasons-why-your-agency-should-offer-optimization/',
#   'audience_ids': []
# }
```

###Create a New Experiment
A `project_id`, `description`, and `edit_url` are required in the the call. Other editable arguments are all optional.

When you create an experiment, Optimizely will also fill in associated data by default. These defaults mimic the behavior of Optimizely's editor and include:

* Two variations in `variation_ids` named 'Default Variation #1' and 'Default Variation #2'. The default variations have 50% traffic each and no code.
* One URL targeting condition in `url_conditions`. By default, your experiment is targeted to the `edit_url` with a simple match.
* Traffic allocated to 100% in `percentage_included`. Traffic is measured in basis points. Divide by 100 to get a percentage.
* A `status` of 'Not started', meaning the experiment will not be running initially.
* Immediate `activation_mode`, rather than manual.
* The `experiment_type` will be a normal A/B test, rather than a multivariate or multipage test.

####Example Python
```python
>>> experiment = client.Experiments.create({'project_id': 1234, 'edit_url': 'https://mysite.com/products/', 'description': 'My Experiment Name'})
>>> experiment.__dict__
# {
#   'id': 15,
#   'project_id': 1234,
#   // ... (other fields omitted)
#   'percentage_included': 10000,
#   'is_multivariate': False,
#   'variation_ids': [
#     800227656,
#     800227657
#   ],
#   'status': 'Not started',
#   'url_conditions': [
#     {
#       'index': 0,
#       'match_type': 'simple',
#       'created': '2014-04-12T19:10:53.806640Z',
#       'value': 'https://mysite.com/products',
#       'last_modified': '2014-04-12T19:10:53.806650Z',
#       'negate': False
#     }
#   ],
#   'description': 'My Experiment Name',
#   'activation_mode': 'immediate',
#   'custom_css': '',
#   'custom_js': '',
#   'experiment_type': 'ab',
# }
```

###Update an Experiment
Experiments can be updated by updating the attributes of a fetched object and calling `save` or by calling `update` on a client and passing in an update dictionary and resource Id.

####Editable Fields
Experiments can be updated by updating the attributes of a fetched object and calling `save` or by calling `update` on a client and passing in an update dictionary and resource Id.

* `audience_ids` (add or remove an audience ID here to change the experiment's targeting)
* `activation_mode`
* `description`
* `edit_url`
* `status` (send 'Running' to start an experiment and 'Paused' to stop)
* `custom_css`
* `custom_js`
* `percentage_included`
* `url_conditions`

We don't currently support creating or updating multivariate or multipage tests via the API.

####Example Python
```python
>>> experiment.status = 'Running'
>>> experiment.save()
>>> experiment.__dict__
# {
#   'id': 15,
#   'project_id': 1234,
#   // ... (other fields omitted)
#   'percentage_included': 10000,
#   'is_multivariate': False,
#   'variation_ids': [
#     800227656,
#     800227657
#   ],
#   'status': 'Not started',
#   'url_conditions': [
#     {
#       'index': 0,
#       'match_type': 'simple',
#       'created': '2014-04-12T19:10:53.806640Z',
#       'value': 'https://mysite.com/products',
#       'last_modified': '2014-04-12T19:10:53.806650Z',
#       'negate': False
#     }
#   ],
#   'description': 'My Experiment Name',
#   'activation_mode': 'immediate',
#   'custom_css': '',
#   'custom_js': '',
#   'experiment_type': 'ab',
# }

# an equivalent call
>>> client.Experiments.update(15, {'status': 'Running'})
```

###Delete an Experiment
Deleting an experiment will **permanently delete the experiment and its results**.

In most cases, it's safer to archive the experiment by setting `status = 'Archived'`. This will remove the experiment from the Optimizely snippet and hide it in the project dashboard, but still leave it available under "Archived Experiments" for viewing and recovery later.

####Example Python
```python
>>> experiment = client.Experiments.get(15)
>>> experiment.delete()  # returns None on success
```

###List Experiments in Project
Get a list of all the `experiments` in a project by calling experiments on the associated `Project` object.

####Example Python
```python
>>> project = client.Projects.get(1234)
>>> project.experiments()
# [<optimizely.resource.Experiment object at 0x000000000>, <optimizely.resource.Experiment object at 0x000000010>]
```

###Get Experiment Results
To list all results, call results on the associated `Experiment` object.

This function may return a `ServiceUnavailableError` when the associated endpoint is overloaded. If you experience any issues please email us at [developers@optimizely.com](mailto:developers@optimizely.com).

See [the Optimizely REST API documentation](http://developers.optimizely.com/rest/#get-experiment-results) for response attribute definitions.

####Example Python
```python
>>> experiment = client.Experiments.get(15)
>>> experiment.results()
# [<optimizely.resource.Result object at 0x000000000>, <optimizely.resource.Result object at 0x000000010>]

>>> result = experiment.results()[0]
>>> result.__dict__
# {
#   'variation_id': '925781903',
#   'variation_name': 'My Variation',
#   'goal_id': 820360058,
#   'goal_name': 'Engagement',
#   'baseline_id': '924521605',
#   'begin_time': '2014-07-25T20:30:00Z',
#   'end_time': '2014-07-25T20:38:09Z',
#   'visitors': 853,
#   'conversions': 204,
#   'conversion_rate': 0.239,
#   'status': 'inconclusive',
#   'improvement': 0.014,
#   'confidence': 0.631,
#   'is_revenue': False,
# }
```

###Get Experiment Results (Stats Engine)
To list [Stats Engine results](https://help.optimizely.com/hc/en-us/articles/200039895-Stats-Engine-How-Optimizely-calculates-results-to-enable-business-decisions?flash_digest=ffd1e1a116256b019e5e8109aa843548129129ae), call stats on the associated `Experiment` object.

This function may return a `ServiceUnavailableError` when the associated endpoint is overloaded. If you experience any issues please email us at [developers@optimizely.com](mailto:developers@optimizely.com).

*Only experiments started on or after January 21, 2015 have statistics computed by Optimizely Stats Engine.*

See [the Optimizely REST API documentation](http://developers.optimizely.com/rest/reference/index.html#get-stats) for response attribute definitions.

####Example Python
```python
>>> experiment = client.Experiments.get(15)
>>> experiment.stats()
# [<optimizely.resource.Stat object at 0x000000000>, <optimizely.resource.Stat object at 0x000000010>]

>>> stat = experiment.stats()[0]
>>> stat.__dict__
# {
#   'variation_id': '925781903',
#   'variation_name': 'My Variation',
#   'goal_id': 820360058,
#   'goal_name': 'Engagement',
#   'baseline_id': '924521605',
#   'begin_time': '2014-07-25T20:30:00Z',
#   'end_time': '2014-07-25T20:38:09Z',
#   'visitors': 853,
#   'conversions': 204,
#   'conversion_rate': 0.239,
#   'status': 'inconclusive',
#   'improvement': 0.014,
#   'statistical_significance’: 0.631,
#   'difference': 0.014,
#   'difference_confidence_interval_min': 0.008,
#   'difference_confidence_interval_max': 0.020,
#   'visitors_until_significance': 100,
#   'is_revenue': False,
# }
```

##Schedules
Experiments can be scheduled to start or stop at a particular time. A **Schedule** is a specification of a start time, stop time, or both, associated with a particular experiment. To learn more about scheduling experiments, see the [Experiment Scheduler](https://help.optimizely.com/hc/en-us/articles/200039845-Experiment-Scheduler).

###Read a Schedule
Get data about a particular schedule, including the start time and stop time of the associated experiment.

See [the Optimizely REST API documentation](http://developers.optimizely.com/rest/#read-a-schedule) for response attribute definitions.

####Example Python
```python
>>> schedule = client.Schedules.get(567)
>>> schedule.__dict__
# {
#   'status': 'ACTIVE', 
#   'start_time': '2015-01-01T08:00:00Z', 
#   'stop_time': None,
#   'experiment_id': 5678,
#   'id': 9012
# }
```

###Create a Schedule
Create a schedule for an experiment. You must specify either a `start_time` or `stop_time`, or both. All times are in UTC and must be specified in the format `2015-01-01T08:00:00Z`. The created schedule will always be marked `ACTIVE`, and any previously created schedules will be marked as `INACTIVE`.

####Example Python
```python
>>> schedule = client.Schedules.create({'experiment_id': 5678, 'start_time': '2015-01-01T08:00:00Z'})
>>> schedule.__dict__
# {
#   'status': 'ACTIVE', 
#   'start_time': '2015-01-01T08:00:00Z', 
#   'stop_time': None,
#   'experiment_id': 5678,
#   'id': 9012
# }
```

###Update a Schedule
Update a schedule. You must specify either a `start_time` or `stop_time`, or both. All times are in UTC and must be specified in the format `2015-01-01T08:00:00Z`.

Schedules can be updated by updating the attributes of a fetched object and calling `save` or by calling `update` on a client and passing in an update dictionary and resource Id.

####Example Python
```python
>>> schedule.stop_time = '2015-01-02T08:00:00Z'
>>> schedule.save()
>>> schedule.__dict__
# {
#   'status': 'ACTIVE', 
#   'start_time': '2015-01-01T08:00:00Z', 
#   'stop_time': '2015-01-02T08:00:00Z',
#   'experiment_id': 5678,
#   'id': 9012
# }

# an equivalent call
>>> client.Schedules.update(9012, {'stop_time': '2015-01-02T08:00:00Z'})
```

###Delete a Schedule
Permanently delete a schedule. If the schedule being deleted was marked as `ACTIVE`, the associated experiment will no longer be scheduled.

####Example Python
```python
>>> schedule = client.Schedules.get(567)
>>> schedule.delete()  # returns None on success
```

###List Schedules for Experiment
See a list containing the current schedules for an experiment as well as any previously created `schedules` by calling schedules on the associated `Experiment` object. The current schedule will be marked `ACTIVE` and any previously created schedules will be marked `INACTIVE`.

####Example Python
```python
>>> experiment = client.Experiments.get(15)
>>> experiment.schedules()
# [<optimizely.resource.Schedule object at 0x000000000>, <optimizely.resource.Schedule object at 0x000000010>]
```

##Variations
Every experiment contains a set of variations that each change the visitor's experience in a different way. Variations define the code that should be applied on a page to change the experience, and the percentage of visitors who should see that code. A standard "A/B" test has two variations (including the original), and Optimizely supports adding many more variations.

###Read a Variation
Get metadata for a single variation.

See [the Optimizely REST API documentation](http://developers.optimizely.com/rest/#read-a-variation) for response attribute definitions.

####Example Python
```python
>>> variation = client.Variations.get(859611684)
>>> variation.__dict__
# {
#   'is_paused': False,
#   'description': 'Variation #2',
#   'weight': 5000,
#   'created': '2014-04-17T00:47:06.388650Z',
#   'section_id': None,
#   'js_component': 'alert(\'It works!\');',
#   'experiment_id': 854484703,
#   'project_id': 859720118,
#   'id': 859611684
# }
```

###Create a new Variation
An `experiment_id` and `description` are required in the the call. Most variations will also want to include `js_component`, but an Original can use the default value of an empty string.

Whenever possible, you should also include the correct `weight` and update the other variations so their weights sum to 10000.

Note that newly created experiments come with two variations created automatically, so you may need to update a variation rather than creating it.

####Known Issues
Traffic allocation may not always be set correctly. Changes to the `weight` or `is_paused` property should be double-checked on optimizely.com.

We're working on fixing this issue now. Please contact [developers@optimizely.com](mailto:developers@optimizely.com) to be updated when it is fixed.

####Example Python
```python
>>> variation = client.Variations.create({'experiment_id': 854484703, 'description': 'Variation #1', 'js_component': '$(\'.headline\').text(\'New headline\');', 'weight': 3333})
>>> variation.__dict__
# {
#   'is_paused': False,
#   'description': 'Variation #2',
#   'weight': 3333,
#   'created': '2014-04-17T00:47:06.388650Z',
#   'section_id': None,
#   'js_component': 'alert(\'It works!\');',
#   'experiment_id': 854484703,
#   'project_id': 859720118,
#   'id': 859611684
# }
```

###Update a Variation
Variations can be updated by updating the attributes of a fetched object and calling `save` or by calling `update` on a client and passing in an update dictionary and resource Id.

####Editable Fields
* `description`
* `is_paused` (set this to True to stop the variation from getting traffic)
* `js_component`
* `weight`

####Example Python
```python
>>> variation.js_component = '$(\'.headline\').text(\'Updated headline\');'
>>> variation.save()
>>> variation.__dict__
# {
#   'is_paused': False,
#   'description': 'Variation #2',
#   'weight': 3333,
#   'created': '2014-04-17T00:47:06.388650Z',
#   'section_id': None,
#   'js_component': '$(\'.headline\').text(\'Updated headline\');',
#   'experiment_id': 854484703,
#   'project_id': 859720118,
#   'id': 859611684
# }

# an equivalent call
>>> client.Variations.update(859611684, {'js_component': '$(\'.headline\').text(\'Updated headline\');'})
```

###Delete a Variation
Deleting a variation is the preferred way to remove it from an experiment. Directly editing the `variation_ids` property on experiments is not supported.

####Example Python
```python
>>> variation = client.Variations.get(859611684)
>>> variation.delete()  # returns None on success
```

###List Variations in Experiment
List all variations associated with the experiment.

####Example Python
```python
>>> experiment = client.Experiments.get(854484703)
>>> experiment.variations()
# [<optimizely.resource.Variation object at 0x000000000>, <optimizely.resource.Variation object at 0x000000010>, <optimizely.resource.Variation object at 0x000000020>]
```

##Goals
Goals are the metrics used to decide which variation in an experiment is the winner. Like audiences, goals are defined at the project level and can be reused across multiple experiments within a project. Each goal is tracked for each experiment it's associated with. An experiment with no goals will still run, but its results page will be empty.

###Read a Goal
Optimizely has several different goal types, as explained in [our knowledge base](https://help.optimizely.com/hc/en-us/articles/200039915-Goals-Overview). Depending on the goal type, different fields in the response are important.

See [the Optimizely REST API documentation](http://developers.optimizely.com/rest/#read-a-goal) for information about Goals and Goal types.

####Example Python
```python
>>> goal = client.Goals.get(543071054)
>>> goal.__dict__
# {
#   is_editable': None,
#   target_to_experiments': True,
#   archived': False,
#   description': 'Confirming if the navigation is used more or less. #nav',
#   id': 543071054,
#   target_urls': [],
#   title': 'Navigation button clicks',
#   event': 'nav_button_clicks',
#   url_match_types': [],
#   project_id': 547944643,
#   goal_type': 0,
#   experiment_ids': [
#         561450169
#       ],
#   selector': '.portal-navigation > button',
#   created': '2014-01-09T23:47:51.042343Z',
#   last_modified': '2014-12-08T12:33:27.045543Z',
#   target_url_match_types': [],
#   urls': []
# }
```

###Create a Goal
For all goals, the `title` and `goal_type` are required. For each goal type, other fields are required:

* Click goals need a `selector` and a boolean value for `target_to_experiments` to be set. If it's true, the goal will run on the same pages as the experiment it's it attached to. If it's false, you should also provide `target_urls` and `target_url_match_types`.
* Pageview goals need a list of `urls` and `url_match_types` and will match nowhere if the lists are empty.
* Custom event goals need an `event` name.

####Example Python
```python
>>> goal = client.Goals.create({'project_id': 1234, , 'title': 'Add to cart clicks', 'goal_type': 0, 'selector': 'div.cart > button', 'target_to_experiments': True})
>>> goal.__dict__
# {
#   is_editable': None,
#   target_to_experiments': True,
#   archived': False,
#   description': 'Confirming if the navigation is used more or less. #nav',
#   id': 860850647,
#   target_urls': [],
#   title': 'Add to cart clicks',
#   event': 'nav_button_clicks',
#   url_match_types': [],
#   project_id': 1234,
#   goal_type': 0,
#   experiment_ids': [
#         561450169
#       ],
#   selector': 'div.cart > button',
#   created': '2014-01-09T23:47:51.042343Z',
#   last_modified': '2014-12-08T12:33:27.045543Z',
#   target_url_match_types': [],
#   urls': []
# }
```

###Add or Remove a Goal
To add a goal to an experiment, call `add_goal` on the associated `Experiment` object using the goal's `id`.

To remove a goal, call `remove_goal` on the associated `Experiment` object using the goal's `id`.

####Example Python
```python
>>> experiment = client.Experiments.get(15)
>>> experiment.add_goal(543071054)     # add a goal
>>> experiment.remove_goal(543071054)  # remove that goal
```

###Update a Goal
Goals can be updated by updating the attributes of a fetched object and calling `save` or by calling `update` on a client and passing in an update dictionary and resource Id.

####Editable Fields
* `archived`
* `description`
* `experiment_ids`
* `goal_type`
* `selector`
* `target_to_experiments`
* `target_urls`
* `target_url_match_types`
* `title`
* `urls`
* `url_match_types`

Please note that [old goals cannot be edited](https://help.optimizely.com/hc/en-us/articles/200039915-Goals-Measure-the-success-of-your-experiment#retroactive_goals), and will have `is_editable` set to `False`.

####Example Python
```python
>>> goal.title = 'Updated goal name'
>>> goal.save()
>>> goal.__dict__
# {
#   is_editable': None,
#   target_to_experiments': True,
#   archived': False,
#   description': 'Confirming if the navigation is used more or less. #nav',
#   id': 543071054,
#   target_urls': [],
#   title': 'Updated goal name',
#   event': 'nav_button_clicks',
#   url_match_types': [],
#   project_id': 547944643,
#   goal_type': 0,
#   experiment_ids': [
#         561450169
#       ],
#   selector': '.portal-navigation > button',
#   created': '2014-01-09T23:47:51.042343Z',
#   last_modified': '2014-12-08T12:33:27.045543Z',
#   target_url_match_types': [],
#   urls': []
# }

# an equivalent call
>>> client.Goals.update(543071054, {'title': 'Updated goal name'})
```

###Delete a Goal
Delete a goal and remove it from **all associated experiments**. Deleting a goal will also remove it from past experiments, and you won't be able to see results for that goal on those experiments.

It's usually better to [remove a goal](#add-or-remove-a-goal) from an experiment than delete it directly.

####Example Python
```python
>>> goal = client.Goals.get(543071054)
>>> goal.delete()  # returns None on success
```

###List all Goals in Project
Get a list of all the goals in a project by calling `goals` on the associated `Project` object.

####Example Python
```python
>>> project = client.Projects.get(1234)
>>> project.goals()
# [<optimizely.resource.Goal object at 0x000000000>, <optimizely.resource.Goal object at 0x000000010>]
```

##Audiences
An Audience is a group of visitors that match set conditions. You can target an experiment to one or more audiences, or you can segment experiment results to see how different audiences performed. You can [learn more about audiences in our knowledge base](https://help.optimizely.com/hc/en-us/articles/200039685).

###Read an Audience
Get metadata for a single audience.

See [the Optimizely REST API documentation](http://developers.optimizely.com/rest/#read-an-audience) for response attribute definitions.

####Example Python
```python
>>> audience = client.Audiences.get(567)
>>> audience.__dict__
# {
#   'description': 'People from Canada',
#   'project_id': 1234,
#   'id': 567,
#   'name': 'Canadians',
#   'created': '2014-05-24T00:13:52.784580Z',
#   'conditions': '["and", {"type":"browser", "value":"gc"}, {"type":"query", "name":"utm_campaign", "value":"true"}]',
#   'last_modified': '2014-06-10T22:12:21.707170Z',
#   'segmentation': False,
#   'archived': False
# }
```

###Create an Audience
For all audiences, `name` and `project_id` are required. You can optionally add a `description`.

By default, the `conditions` field will just be a string representing an empty list `'[]'`. In this case, the audience won't match anyone automatically. Instead, you can add visitors to it by `id` using the `addToAudience` function in our [Javascript API](http://developers.optimizely.com/javascript/#audiences). See our [audiences API sample](http://developers.optimizely.com/samples/#dmp) for more information.

Platinum customers can also set the `segmentation` field. The default value is False, but you can set it to True to track the audience's behavior on the results page. See the section below on [updating audiences](http://developers.optimizely.com/rest/#update-audience) for more information.

####Example Python
```python
>>> audience = client.Audiences.create({'project_id': 1234, , 'name': 'Chinese food buyers'})
>>> audience.__dict__
# {
#   'description': '',
#   'project_id': 1234,
#   'id': 568,
#   'name': 'Chinese food buyers',
#   'created': '2014-06-10T22:12:21.707170Z',
#   'conditions': '[]',
#   'last_modified': '2014-06-10T22:12:21.707170Z',
#   'segmentation': False,
#   'archived': False
# }
```

###Update an Audience
Audiences can be updated by updating the attributes of a fetched object and calling `save` or by calling `update` on a client and passing in an update dictionary and resource Id.

####Editable Fields
* `name
* `description
* `conditions` (see [Audience Conditions](http://developers.optimizely.com/rest/conditions))
* `segmentation` (see [creating audiences](https://help.optimizely.com/hc/en-us/articles/200039685-Audiences-Overview-Include-certain-visitors-in-your-experiment#creating))

Only Platinum customers can enable segmentation, and you can only enable segmentation on an audience if you have fewer than ten dimensions or other audiences enabled for segmentation. If you don't have sufficient permissions or already have 10 audiences/dimensions, the API will return an error.

####Example Python
```python
>>> audience.description = 'People who bought Chinese food'
>>> audience.save()
>>> audience.__dict__
# {
#   'description': 'People who bought Chinese food',
#   'project_id': 1234,
#   'id': 568,
#   'name': 'Chinese food buyers',
#   'created': '2014-06-10T22:12:21.707170Z',
#   'conditions': '[]',
#   'last_modified': '2014-06-10T22:12:21.707170Z',
#   'segmentation': False,
#   'archived': False
# }

# an equivalent call
>>> client.Audiences.update(568, {'description': 'People who bought Chinese food'})
```

###Delete an Audience
Deleting audiences is not supported.

###List Audiences in Project
Get a list of all the `audiences` in a project by calling audiences on the associated `Project` object.

####Example Python
```python
>>> project = client.Projects.get(1234)
>>> project.audiences()
# [<optimizely.resource.Audience object at 0x000000000>, <optimizely.resource.Audience object at 0x000000010>]
```

##Dimensions
Dimensions are attributes of visitors to your website or mobile app, such as demographic data, behavioral characteristics, or any other information particular to a visitor. Dimensions can be used to construct audiences and segment experiment results.

The REST API allows you to create, edit, or delete dimensions. If you want to track visitor data for a dimension you must use a client-side API (for websites, use the [Javascript API](https://developers.optimizely.com/javascript/#dimensions)). To learn more about dimensions, see [Dimensions: Capture visitor data through the API](https://help.optimizely.com/hc/en-us/articles/200040865-Dimensions-Capture-visitor-data-through-the-API).

###Read a Dimension
Get metadata for a single dimension.

See [the Optimizely REST API documentation](http://developers.optimizely.com/rest/#read-a-dimension) for response attribute definitions.

####Example Python
```python
>>> dimension = client.Dimensions.get(5678)
>>> dimension.__dict__
# {
#   "name": "My Dimension",  
#   "last_modified": "2015-01-01T00:00:00.000000Z",
#   "client_api_name": "my_dimension_api_name",
#   "project_id": 1234, 
#   "id": 5678, 
#   "description": "Description of my dimension"
# } 
```

###Create a Dimension
Create a new dimension with the specified `name`. The `client_api_name` and `description` fields are optional. If there is an existing dimension with a duplicate `name` or `client_api_name` the client will raise a `BadRequestError`.

####Example Python
```python
>>> dimension = client.Dimensions.create({'project_id': 1234, 'name': 'My Dimension', 'client_api_name', 'my_dimension_api_name', 'description': 'Description of my dimension'})
>>> dimension.__dict__
# {
#   "name": "My Dimension",  
#   "last_modified": "2015-01-01T00:00:00.000000Z",
#   "client_api_name": "my_dimension_api_name",
#   "project_id": 1234, 
#   "id": 5678, 
#   "description": "Description of my dimension"
# } 
```

###Update a Dimension
Update the `name`, `client_api_name`, or `description` of an existing dimension.

Dimensions can be updated by updating the attributes of a fetched object and calling `save` or by calling `update` on a client and passing in an update dictionary and resource Id.

####Example Python
```python
>>> dimension.description = 'A new description of my dimension'
>>> dimension.save()
>>> dimension.__dict__
# {
#   "name": "My Dimension",  
#   "last_modified": "2015-01-01T00:00:00.000000Z",
#   "client_api_name": "my_dimension_api_name",
#   "project_id": 1234, 
#   "id": 5678, 
#   "description": "A new description of my dimension"
# } 

# an equivalent call
>>> client.Dimensions.update(5678, {'description': 'A new description of my dimension'})
```

###Delete a Dimension
Permanently delete a dimension. By taking this action, any audiences using this dimension will stop getting traffic, and results associated with this dimension will be permanently deleted.

####Example Python
```python
>>> dimension = client.Dimensions.get(5678)
>>> dimension.delete()  # returns None on success
```

###List Dimensions in Project
Get a list of all the dimensions in a project by calling `dimensions` on the associated `Project` object.

####Example Python
```python
>>> project = client.Projects.get(1234)
>>> project.dimensions()
# [<optimizely.resource.Dimension object at 0x000000000>, <optimizely.resource.Dimension object at 0x000000010>]
```
