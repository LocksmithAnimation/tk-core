# Copyright (c) 2016 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import tempfile

from tank_test.tank_test_base import *
from tank_vendor import shotgun_deploy
from tank_vendor import shotgun_base



class TestApi(TankTestBase):
    """
    Testing the Shotgun deploy main API methods
    """

    def _touch_info_yaml(self, path):
        """
        Helper method that creates an info.yml dummy
        file in the given location
        """
        shotgun_base.ensure_folder_exists(path)
        fh = open(os.path.join(path, "info.yml"), "wt")
        fh.write("# unit test placeholder file\n\n")
        fh.close()


    def test_factory(self):
        """
        Basic test of descriptor construction
        """
        d = shotgun_deploy.create_descriptor(
            self.tk.shotgun,
            shotgun_deploy.Descriptor.CONFIG,
            {"type": "app_store", "version": "v0.1.6", "name": "tk-testbundlefactory"}
        )

        app_root_path = os.path.join(
            shotgun_base.get_cache_root(),
            "bundle_cache",
            "app_store",
            "tk-testbundlefactory",
            "v0.1.6"
        )

        self._touch_info_yaml(app_root_path)

        self.assertEqual(app_root_path, d.get_path())


    def test_alt_cache_root(self):
        """
        Testing descriptor constructor in alternative cache location
        """
        sg = self.tk.shotgun

        bundle_root = tempfile.gettempdir()

        d = shotgun_deploy.create_descriptor(
                sg,
                shotgun_deploy.Descriptor.CONFIG,
                {"type": "app_store", "version": "v0.4.2", "name": "tk-testaltcacheroot"},
                bundle_root
        )

        # get_path() returns none if path doesn't exists
        self.assertEqual(d.get_path(), None)

        # now create info.yml file and try again
        app_root_path = os.path.join(
            bundle_root,
            "app_store",
            "tk-testaltcacheroot",
            "v0.4.2")
        self._touch_info_yaml(app_root_path)
        self.assertEqual(d.get_path(), app_root_path)


    def _test_uri(self, uri, location_dict):

        computed_dict = shotgun_deploy.io_descriptor.descriptor_uri_to_dict(uri)
        computed_uri = shotgun_deploy.io_descriptor.descriptor_dict_to_uri(location_dict)
        self.assertEqual(uri, computed_uri)
        self.assertEqual(location_dict, computed_dict)

    def test_descriptor_uris(self):
        """
        Test dict/uri syntax and conversion
        """
        uri = "sgtk:descriptor:app_store?version=v0.1.2&name=tk-bundle"
        dict = {"type": "app_store", "version": "v0.1.2", "name": "tk-bundle"}
        self._test_uri(uri, dict)

        uri = "sgtk:descriptor:path?path=/foo/bar"
        dict = {"type": "path", "path": "/foo/bar"}
        self._test_uri(uri, dict)