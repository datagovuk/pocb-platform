import pubtool.lib.schema as s
from .util import BaseTest

from nose.tools import raises


class SchemaTest(BaseTest):

    def test_load_schema(self):
        p = s._get_schema("publisher")
        assert p is not None, "Failed to load publisher, but it should work"

    def test_load_schema(self):
        p = s._get_schema("fake")
        assert p is None

    def test_validate_publisher_fail_required(self):
        publisher_data = {}
        res = s.validation_check("publisher", publisher_data)
        assert res == ["'name' is a required property",
            "'title' is a required property"], res

    def test_validate_publisher_fail_types(self):
        publisher_data = {
            "name": "testpub", "title": 200
        }
        res = s.validation_check("publisher", publisher_data)
        assert len(res) == 1, res
        assert res[0] == "200 is not of type 'string'"

    def test_validate_publisher_ok(self):
        publisher_data = {
            "name": "testpub", "title": "Test Publisher"
        }
        res = s.validation_check("publisher", publisher_data)
        assert len(res) == 0, res
