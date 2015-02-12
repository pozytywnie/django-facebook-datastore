facebook-datastore
========================

.. image:: https://travis-ci.org/pozytywnie/django-facebook-auth.svg
   :target: https://travis-ci.org/pozytywnie/django-facebook-auth

An application that stores data about Facebook users logged in on your site using Facebook API.
This data can be handy for various reasons.


Usage
-----
Currently it integrates with https://github.com/pozytywnie/django-facebook-auth and expects FacebookUser object in the constructor.

Example::

    from facebook_datastore.engines import UserProfileEngine
    from facebook_auth.models import FacebookUser

    user = FacebookUser.objects.get(id=SOME_ID)
    engine = UserProfileEngine(user)
    engine.run()

Such code should be executed by for example celery - in the background. You will also need a valid user access token.
