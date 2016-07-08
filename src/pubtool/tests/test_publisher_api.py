
from .util import BaseTest

class PublisherApiTest(BaseTest):

    def create_localtest_data(self, mongo):
        mongo.db.publishers.insert_one({'name': 'Test publisher', 'slug': 'testpub'})

    def test_list_ok(self):
        response = self.do_get('/api/v1/publisher')
        self.assertEqual(response.status_code, 200)

        body = self.response_as_json(response)
        self.assertEquals(len(body['data']), 1)

    def test_show_ok(self):
        response = self.do_get('/api/v1/publisher/testpub')
        self.assertEqual(response.status_code, 200)

        body = self.response_as_json(response)
        self.assertEquals(body['data']['name'], 'Test publisher')

    def test_show_fail(self):
        response = self.do_get('/api/v1/publisher/fake')
        self.assertEqual(response.status_code, 404)

        body = self.response_as_json(response)
        self.assertEquals(body['success'], False)


    def test_list_fail(self):
        # Test with wrong url
        response = self.do_get('/api/v1/publishers')
        self.assertEqual(response.status_code, 404)
