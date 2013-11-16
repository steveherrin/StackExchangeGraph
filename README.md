StackExchangeGraph
==================

Introduction
------------
This is a semi-recreational project to example the user graph of Stack Overflow
based on questions/answers. Semi- because this is also done in conjunction with
Lada Adamic's [Social Network Analysis course on Coursera](https://class.coursera.org/sna-003/class).

Getting More Quota
------------------
To get a more generous quota, you'll want to register as an app with
the [Stack Exchange API](http://stackapps.com). Once you've registered,
create a file `StackAppsConstants.py` with the following constants that
you should get from the registation process. Right now, only the key
is strictly necessary:
```python
client_id = 0
client_secret = 'your secret'
key = 'your key'
```

