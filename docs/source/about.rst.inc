**Simyan** is a python wrapper for the Comic Vine API.

.. code-block:: python

    from simyan.comicvine import Comicvine
    from simyan.sqlite_cache import SQLiteCache

    session = Comicvine(api_key="Comicvine API Key", cache=SQLiteCache())

    # Search for Publisher
    results = session.publisher_list(params={'filter': 'name:DC Comics'})
    for publisher in results:
        print(f"{publisher.id_} | {publisher.name} - {publisher.site_url}")

    # Get details for a Volume
    result = session.volume(volume_id=26266)
    print(result.summary)
