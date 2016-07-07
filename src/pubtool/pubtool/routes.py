
import pubtool.views as v
import pubtool.api as api

def create_routes(app):
    app.add_url_rule('/', 'home', v.home)
    app.add_url_rule('/publisher/', 'publisher_list', v.publisher_list)
    app.add_url_rule('/publisher/<slug>', 'publisher_show', v.publisher_show)

    app.add_url_rule('/api/v1/<path:path>', 'api', api.api_call)
    app.add_url_rule('/api/v1', 'api_home', api.api_home)
