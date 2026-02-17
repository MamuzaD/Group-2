"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""

import pytest
from src import app
from src import status

@pytest.fixture()
def client():
    """Fixture for Flask test client"""
    return app.test_client()

@pytest.mark.usefixtures("client")
class TestCounterEndpoints:
    """Test cases for Counter API"""

    def test_create_counter(self, client):
        """It should create a counter"""
        result = client.post('/counters/foo')
        assert result.status_code == status.HTTP_201_CREATED

    def test_duplicate_counter(self, client):
        """It should create a counter with a duplicate name"""
        result1 = client.post('/counters/dup')
        assert result1.status_code == status.HTTP_201_CREATED

        result2 = client.post('/counters/dup')
        assert result2.status_code == status.HTTP_409_CONFLICT
  
    def test_nonexistent_counter(self, client):
        # Create a counter.
        client.post('/counters/topsushi')

        # Try to access a different, nonexistent counter, should return 404.
        self.assert_counter_does_not_exist(client, 'gorillasushi')


    def test_delete_counter(self, client):
        """after a counter has been deleted, it should be non-existant"""

        #Arrange -> create a counter
        counter_name = 'counter'
        client.post('/counters/' + counter_name)

        #Act -> delete the counter
        deletion_result = client.delete('/counters/' + counter_name)

        #Assert -> check for 204 code and that counter is no longer extant
        assert deletion_result.status_code == status.HTTP_204_NO_CONTENT
        self.assert_counter_does_not_exist(client, counter_name)




    #helper function - asserts that no counters exist with the given name
    def assert_counter_does_not_exist(self, client, counter_name):
        check_existence_result = client.get('/counters/' + counter_name)
        assert check_existence_result.status_code == status.HTTP_404_NOT_FOUND