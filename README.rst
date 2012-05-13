====================================================
Assembla: Python wrapper for Assembla's RESTful API
====================================================

An easy to use wrapper around the Assembla API.

 - `Basic Example`_
 - `Examples for Spaces`_
 - `Examples for Milestones`_
 - `Examples for Users`_
 - `Examples for Tickets`_
 - `Examples for Tasks`_
 - `Examples for Stream`__  
 - `Model Reference`_
 - `Caching`_


Basic Example
-------------

::

	from assembla import API

	assembla = API(auth=('Username', 'Password',))

	print assembla.space(name='Big Project').ticket(number=201).status_name

Examples for Spaces
-------------------
::

	# Retrieve your available spaces
	spaces = assembla.spaces()

	# Select a specific space
	space = assembla.space(name='Big Project')

	# Retrieve the space's milestones
	milestones = space.milestones()

	# Retrieve a specific milestone from the space
	milestone = space.milestone('Release Candidate 1')

	# Retrieve all of the space's tickets
	tickets = space.tickets()

	# Retrieve the space's tickets which are awaiting testing
	tickets = space.tickets(status_name='Test')

	# Retrieve a specific ticket from the space
	ticket = space.ticket(number=301)

	# Retrieve all of the space's users
	users = space.users()

	# Retrieve a specific user from the space
	user = space.user(name='John Smith')

Examples for Milestones
-----------------------
::

	# Select a specific milestone
	milestone = assembla.space(name='Big Project').milestone('Release Candidate 1')

	# Retrieve the milestone's tickets
	tickets = milestone.tickets()

	# Retrieve a specific ticket from the milestone
	ticket = milestone.ticket(number=301)

	# Retrieve the milestone's users
	users = milestone.users()

	# Retrieve a specific user from the milestone
	user = milestone.user(name='John Smith')

Examples for Users
------------------
::

	# Select a specific user
	user = assembla.space(name='Big Project').user(name='John Smith')

	# Retrieve the user's tickets
	tickets = user.tickets()

	# Retrieve a specific ticket from the user
	ticket = user.ticket(status_name='Test')

Examples for Tickets
--------------------
::

	# Retrieve a specific ticket
	ticket = space.ticket(number=201)

	# Retrieve all tickets awaiting code review
	tickets = space.tickets(status_name='Code Review')

	# Retrieve all tickets assigned to an individual which are of a certain priority
	# and awaiting testing
	tickets = space.tickets(
		assigned_to_id=user.id,
		priority=1,
		status_name='Test'
		)

Example for Tasks
-----------------
::

	# Retrieve tasks for a user.
	api = API(auth, use_cache=False)
	tasks = api.tasks()
	spaces = api.spaces()

	# Retrieve the total hours, for which an
	# individual has worked in a space!
	for space in spaces:
	    total_hours = 0
	    print space.name
	    for task in tasks:
		if task.space_id == space.id:
	            total_hours += task.hours		
	    print total_hours

Example for Stream
------------------
::

	# Retrieve the events.

	from datetime import datetime, date, timedelta

	api = API(auth, use_cache=False)
	events = api.events()
	spaces = api.spaces()

	# Retrieve the events happened in all spaces for an Organization, for a day.

	this_day = (datetime.now() - timedelta(hours=24)).date()
	print 'Agiliq-Assembla Summary for the day ', this_day.strftime("%b %d %Y")

	for event in events:
	    event_date_time = datetime.strptime(event.date, '%a %b %d %H:%M:%S +0000 %Y')
	    event_date = event_date_time.date()
	    if not event_date > this_day:
	        break
	    for space in spaces:
	        for user in space.users():
	            if user.id == event.author['id'] and event.space['id'] == space.id:
	                print '\n', event_date_time.strftime("%H:%S"), \
		        event.author['name'], '@', space.name, event.operation, \
	                '\n', event.title, '\n', event.url, '\n'
	                if event.object == 'Ticket' and event.operation != 'created':
			    if getattr(event, 'whatchanged', None):
	                        print event.whatchanged
		            elif getattr(event, 'comment_or_description', None):
			        print event.comment_or_description

	#You can use send_mail to send a summary email for a day.
		  
Model Reference
---------------
All models (Space, Milestone, User and Ticket) are returned with fields corresponding
to the data from Assembla. Naming conventions generally follow Assembla's `API
Reference <http://www.assembla.com/spaces/breakoutdocs/wiki/Assembla_REST_API>`_.
Where possible, values are coerced to native Python types.

Caching
-------
Spaces have an in-memory caching system, which reduces the overheard on repeated
requests to Assembla. By default, it is activated. You can deactivate it::

	# Deactivate the cache for a space, all subsequent requests will return fresh data
	space.cache.deactivate()

	# Deactivate the cache for all spaces instantiated from `assembla`
	assembla = API(auth=('Username', 'Password',), use_cache=False)

If you want to purge stale data from a space's cache and begin refilling it::

	# Purge stale data from the space's cache, any subsequent request will update the cache
	space.cache.purge()

Original Source: https://github.com/markfinger/assembla
Tasks API, Stream API, added in this Source: https://github.com/arjunc77/assembla
