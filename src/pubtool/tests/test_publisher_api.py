
from .util import BaseTest

class PublisherApiTest(BaseTest):

    def create_localtest_data(self, mongo):
        from pubtool.logic import Publisher
        self.mongo = mongo
        items = [{'title': 'Test Publisher', 'name': 'testpub'},
                     {'title': 'Test Publisher 2', 'name': 'testpub2'}]
        for item in items:
            Publisher.create(item)


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

    def test_create_fail_slug(self):
        publisher = { 'name': '!!!!', 'title': 'A title field!'}
        response = self.do_post('/api/v1/publisher/new', data=publisher, is_json=True)
        self.assertEqual(response.status_code, 400)

        body = self.response_as_json(response)
        assert body['success'] == False
        assert body['errors'] == ["'name' should consist only of lowercase letters, numbers, underscores or hyphens"]

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

    def test_search_ok(self):
        response = self.do_get('/api/v1/publisher/search?q=test')
        self.assertEqual(response.status_code, 200)

        body = self.response_as_json(response)
        assert len(body['data']['objects']) == 2
        assert body['data']['count'] == 2

    def test_search_ok2(self):
        response = self.do_get('/api/v1/publisher/search?q=2')
        self.assertEqual(response.status_code, 200)

        body = self.response_as_json(response)
        assert len(body['data']['objects']) == 1
        assert body['data']['count'] == 1

    def test_search_ok3(self):
        response = self.do_get('/api/v1/publisher/search?q=wombles')
        self.assertEqual(response.status_code, 200)

        body = self.response_as_json(response)
        assert len(body['data']['objects']) == 0
        assert body['data']['count'] == 0

    def test_search_fail_missing_q(self):
        response = self.do_get('/api/v1/publisher/search')
        self.assertEqual(response.status_code, 400)

        body = self.response_as_json(response)
        assert body['success'] == False
        assert body['errors'] == ['Missing parameter, q is required']
