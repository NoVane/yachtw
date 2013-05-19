# coding=utf-8
#__author__ = 'YuJian'

import sqlite3

class BaseDB(object):
    def __init__(self):
        self._conn = sqlite3.connect(r'yachtw.db')
        self._conn.row_factory = self.dict_factory
    def __exit__(self):
        self._conn.close()

    def sayhi(self):
        print'hello lo'

    def dict_factory(self, c, r):
        d = {}
        for idx, col in enumerate(c.description):
            d[col[0]] = r[idx]
        return d

    def add_image_item(self, img):
        url = img.get("url", "")
        if not url:
            return

        desc = img.get("desc", "")
        c = self._conn.cursor()
        c.execute(u'INSERT INTO image(desc, url) values (?,?)', (desc, url))
        self._conn.commit()

    def query_image_items(self):
        c = self._conn.cursor()
        c.execute(u'SELECT * FROM image ORDER BY iid DESC')

        return c.fetchall()

