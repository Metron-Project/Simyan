**Simyan** is a python wrapper for the Comic Vine API.

.. code-block:: python

    from simyan import create_session, SQLiteCache

    session = create_session(api_key="ComicVine API Key", cache=SQLiteCache())

    # Search for Publisher
    results = session.publisher_list(params={'filter': 'name:DC Comics'})
    for publisher in results:
        print(f"{publisher.id} | {publisher.name} - {publisher.site_url}")

    # Get details for a Volume
    result = session.volume(_id=26266)
    print(result.summary)
