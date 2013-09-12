# -*- coding: utf8 -*-
from base import LmfdbTest
from flask import url_for


class PermalinkTest(LmfdbTest):
    """
    the following tests check if the url_for() actually gives
    what we expect
    """
    def ec(self):
        assert url_for('by_ec_label', label='17.a3') == '/EllipticCurve/Q/17.a3'


class RootTest(LmfdbTest):

    def test_root(self):
        root = self.tc.get("/")
        assert "database" in root.data

    def test_robots(self):
        r = self.tc.get("/robots.txt")
        assert "Disallow: /" not in r.data

    def test_favicon(self):
        assert len(self.tc.get("/favicon.ico").data) > 10

    def test_db(self):
        assert self.C is not None
        known_dbnames = self.C.database_names()
        expected_dbnames = ['Lfunctions', 'ellcurves', 'elliptic_curves', 'numberfields',
                            'MaassWaveForm', 'HTPicard', 'Lfunction',
                            'upload', 'knowledge', 'hmfs', 'userdb', 'quadratic_twists',
                            'modularforms']
        for dbn in expected_dbnames:
            assert dbn in known_dbnames, 'db "%s" missing' % dbn

    def test_url_map(self):
        """

        """
        for rule in self.app.url_map.iter_rules():
            if "GET" in rule.methods:
                tc = self.app.test_client()
                res = tc.get(rule.rule)
                assert "Database" in res.data, "rule %s failed " % rule

    def test_some_latex_error(self):
        """
          Tests for latex errors, but fails at the moment because of other errors
        """
        for rule in self.app.url_map.iter_rules():
            if "GET" in rule.methods:
                try:
                    tc = self.app.test_client()
                    res = tc.get(rule.rule)
                    assert not ("Undefined control sequence" in res.data), "rule %s failed" % rule
                except KeyError:
                    pass

    random_urls = ["/ModularForm/GL2/Q/Maass/"]
