# coding=utf-8
#__author__ = 'YuJian'
from setting import *

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

        target = img.get("target", "")
        c = self._conn.cursor()
        c.execute(u'INSERT INTO image(desc, url, target) values (?,?,?)', (desc, url, target))
        self._conn.commit()

    def update_image_item(self, img):
        iid = img.get("iid", "")
        if not iid:
            return

        url = img.get("url", "")
        if not url:
            return

        desc = img.get("desc", "")
        target = img.get("target", "")
        c = self._conn.cursor()
        c.execute(u'UPDATE image SET desc=?, url=?, target=? WHERE iid=?', (desc, url, target, iid))
        self._conn.commit()

    def del_image_item(self, id):
        if not id:
            return
        c = self._conn.cursor()
        c.execute(u'DELETE FROM image WHERE iid=?', [id])
        self._conn.commit()

    def query_image_count(self):
        c = self._conn.cursor()
        c.execute(u'SELECT COUNT(*) FROM image')
        count = c.fetchone()
        return count['COUNT(*)']

    def query_image_items(self, page=0):
        c = self._conn.cursor()
        page = page - 1
        if page == -1:
            c.execute(u'SELECT * FROM image ORDER BY iid DESC  LIMIT ?', [str(ITEMS_IN_PAGE)])
        else:
            c.execute(u'SELECT * FROM image ORDER BY iid DESC  LIMIT ? OFFSET ?', (str(ITEMS_IN_PAGE), str(int(page) * ITEMS_IN_PAGE)))

        return c.fetchall()


    def add_news_item(self, n):
        desc = n.get("desc", "")

        target = n.get("target", "")
        c = self._conn.cursor()
        c.execute(u'INSERT INTO news(desc, target) values (?,?)', (desc, target))
        self._conn.commit()
    def del_news_item(self, id):
        if not id:
            return
        c = self._conn.cursor()
        c.execute(u'DELETE FROM news WHERE nid=?', [id])
        self._conn.commit()

    def update_news_item(self, new):
        nid = new.get("nid", "")
        if not nid:
            return


        desc = new.get("desc", "")
        target = new.get("target", "")
        c = self._conn.cursor()
        c.execute(u'UPDATE news SET desc=?, target=? WHERE nid=?', (desc, target, nid))
        self._conn.commit()

    def query_news_items(self):
        c = self._conn.cursor()
        c.execute(u'SELECT * FROM news')

        return c.fetchall()


    def check_password(self, u, p):
        c = self._conn.cursor()
        c.execute(u'SELECT passwd FROM user where name=?', [u])
        x = c.fetchone()
        try:
            if x.get('passwd') == p:
                return True
        except:
            return False
        return False
