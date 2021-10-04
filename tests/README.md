# Testing

These tests use the Simyan requests caching for mocking tests, so tests will run quickly and not require credentials.

If your code adds a new URL to the cache, set the `COMICVINE_API_KEY` environment variable before running the test, and
it will be populated in the `Simyan-Cache.sqlite` database.

At any point you should be able to delete the database, set any credentials, and run the full test suite to repopulate
it *(though some results might be different if any of the data has changed at Comic Vine)*.
