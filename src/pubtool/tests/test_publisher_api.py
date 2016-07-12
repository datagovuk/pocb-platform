
from .util import BaseTest

class PublisherApiTest(BaseTest):

    def create_localtest_data(self, mongo):
        self.mongo = mongo
        mongo.db.publishers.insert_one({'title': 'Test Publisher', 'name': 'testpub'})
        mongo.db.publishers.insert_one({'title': 'Test Publisher 2', 'name': 'testpub2'})

    def test_list_ok(self):
        response = self.do_get('/api/v1/publisher')
        self.assertEqual(response.status_code, 200)

        body = self.response_as_json(response)
        self.assertEquals(len(body['data']), 2)

    def test_create_ok(self):
        publisher = {
            "name": "created", "title": "Newly Created Publisher"
        }
        response = self.do_post('/api/v1/publisher/new', data=publisher, is_json=True)
        self.assertEqual(response.status_code, 200)

        body = self.response_as_json(response)['data']
        assert body['name'] == 'created'

        response = self.do_get('/api/v1/publisher')
        self.assertEqual(response.status_code, 200)

        body = self.response_as_json(response)
        assert len(body['data']) ==  3

    def test_create_name_dupe(self):
        publisher = {'title': 'Test Publisher', 'name': 'testpub'}
        response = self.do_post('/api/v1/publisher/new', data=publisher, is_json=True)
        self.assertEqual(response.status_code, 400)

        body = self.response_as_json(response)
        assert body['success'] == False
        assert body['errors'] == ["'name' is already in use"]

    def test_create_name_dupe_and_missing_field(self):
        publisher = { 'name': 'testpub'}
        response = self.do_post('/api/v1/publisher/new', data=publisher, is_json=True)
        self.assertEqual(response.status_code, 400)

        body = self.response_as_json(response)
        assert body['success'] == False
        assert body['errors'] == ["'title' is a required property",
            "'name' is already in use"]


    def test_show_ok(self):
        response = self.do_get('/api/v1/publisher/testpub')
        self.assertEqual(response.status_code, 200)

        body = self.response_as_json(response)
        self.assertEquals(body['data']['title'], 'Test Publisher')

    def test_show_fail(self):
        response = self.do_get('/api/v1/publisher/fake')
        self.assertEqual(response.status_code, 404)

        body = self.response_as_json(response)
        self.assertEquals(body['success'], False)

    def test_list_fail(self):
        # Test with wrong url
        response = self.do_get('/api/v1/publishers')
        self.assertEqual(response.status_code, 404)

    def test_delete_fail_noauth(self):
        pass

    def test_delete_fail_404(self):
        response = self.do_post('/api/v1/publisher/fake?_method=delete', data=None)
        self.assertEqual(response.status_code, 404)


    def test_delete_ok(self):
        response = self.do_post('/api/v1/publisher/testpub?_method=delete', data=None)
        self.assertEqual(response.status_code, 200)

        body = self.response_as_json(response)
        self.assertEquals(body['success'], True)

        # Check it has disappeared from the list
        response = self.do_get('/api/v1/publisher')
        self.assertEqual(response.status_code, 200)

        body = self.response_as_json(response)
        self.assertEquals(len(body['data']), 1)

        # Put the data back before other tests run
        self.mongo.db.publishers.insert_one({'name': 'Test Publisher', 'slug': 'testpub'})
