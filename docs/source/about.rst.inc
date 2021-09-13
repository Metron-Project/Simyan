**Simyan** is a python wrapper for the Comic Vine API.

.. code-block:: python

    from Simyan import api
    # Your config/secrets
    from config import comicvine_api_key

    session = api(api_key=comicvine_api_key)

    # Search for Publisher
    results = session.publisher_list(params={'filter': 'name:DC Comics'})
    for publisher in results:
        print(f"{publisher.id} | {publisher.name} - {publisher.site_url}")

    # Get details for a Volume
    result = session.volume(_id=26266)
    print(result.summary)


*There is a cache option to limit required calls to API*

.. code-block:: python

    from Simyan import api, SqliteCache
    # Your config/secrets
    from config import comicvine_api_key

    session = api(api_key=comicvine_api_key, cache=SqliteCache())

    # Get details for an Issue
    result = session.issue(_id=189810)
    print(f"{result.volume.name} #{result.number}")
    print(result.description)
