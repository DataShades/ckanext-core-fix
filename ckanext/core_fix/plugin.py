import logging

import ckan.plugins as p
import ckan.plugins.toolkit as tk

import ckanext.core_fix.utils as utils
import ckanext.core_fix.helpers as helper


log = logging.getLogger(__name__)


class CoreFixPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)
    p.implements(p.IMiddleware, inherit=True)

    # IConfigurer

    def update_config(self, config_: tk.CKANConfig):
        utils.check_disabled_fixes()
        utils.notify()
        utils.register_fix_templates(config_)

        tk.add_template_directory(config_, "templates")
        tk.add_public_directory(config_, "public")
        tk.add_resource("assets", "core_fix")

    # IMiddleware
    def make_middleware(self, app, config):
        utils.apply_redis_session_fix(app, config)
        return app

    # ITemplateHelpers

    def get_helpers(self):
        return helper.get_helpers()
