# coding=utf-8
import hashlib
import json
import tornado.web
from setting import *

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def render_error(self):
        print 'error'


class LoginHandler(BaseHandler):
    _salt = '_xlolo_'
    def get(self):
        self.set_cookie("checkflag", "true")
        self.render("login.html", error='')

    def post(self):
        if not self.request.headers.get("Cookie"):
            self.render("login.html", error=u"当前浏览器不支持Cookie")
            return

        username = self.get_argument("name")
        if not username:
            self.render("login.html", error=u"用户名为空")
            return

        password = self.get_argument("password")

        if not self.do_login(username, password):
            self.render("login.html", error=u"用户名或密码错误")
            return

        self.set_secure_cookie("user", self.get_argument("name"), expires_days=None)
        self.redirect("/manage")

    def do_login(self, u, p):
        secure_password_md5 = hashlib.md5(p + self._salt).hexdigest()
        print secure_password_md5
        return True

class IndexHandler(BaseHandler):
    def get(self):
        page = 1
        page = self.get_argument("p", 1)
        try:
            page = int(page)
        except:
            self.render_error()
            return
        if not page:
            page = 1
            self.redirect("/?p=1")

        total_page = self.application.db.query_image_count() / ITEMS_IN_PAGE + 1


        if page > total_page:
            page = 1
            self.redirect("/?p=1")

        if page < 0:
            page = total_page


        pagination = []
        start_page = 1
        if page < 3:
            start_page = 1
        elif page > total_page - 2:
            start_page = total_page - SHOW_PAGE_NUM + 1
        else:
            start_page = page - 2

        if start_page < 1:
            start_page = 1

        if start_page + SHOW_PAGE_NUM - 1 > total_page:
            for i in range(start_page, total_page + 1):
                p = {}
                p['number'] = i
                if i == page:
                    p['class'] = 'disabled'
                else:
                    p['class'] = ''

                pagination.append(p)

        else:
            for i in range(start_page, start_page + SHOW_PAGE_NUM):
                p = {}
                p['number'] = i
                if i == page:
                    p['class'] = 'disabled'
                else:
                    p['class'] = ''

                pagination.append(p)



        self.render("index.html", curr=page, total=total_page, pagination = pagination, images=self.application.db.query_image_items(page))

class NewsHandler(BaseHandler):
    def get(self):
        news = self.application.db.query_news_items()
        self.render("news.html", news=news)
class ManageHandler(BaseHandler):
    _json_encoder = json.JSONEncoder()
    @tornado.web.authenticated
    def get(self):
        self.redirect("/manage/image")

    def _add(self, o):
        pass

    def _delete(self, o):
        pass

    def _modify(self, o):
        pass


class ManageImageHandler(ManageHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("manage/image.html", images=self._query())

    @tornado.web.authenticated
    def post(self):
        action = self.get_argument("action", "")
        if action == "new":
            self._add({"desc": self.get_argument("desc", ""),
                            "url": self.get_argument("url", ""),
                            "target":self.get_argument("target", "")})
        elif action =="delete":
            self._delete(self.get_argument("iid", -1))
        elif action == "update":
            self._update({"iid": self.get_argument("iid", ""),
                        "desc": self.get_argument("desc", ""),
                        "url": self.get_argument("url", ""),
                        "target":self.get_argument("target", "")})



    @tornado.web.authenticated
    def _add(self, o):
        self.application.db.add_image_item(o)

    @tornado.web.authenticated
    def _delete(self, o):
        self.application.db.del_image_item(o)

    @tornado.web.authenticated
    def _update(self, o):
        if not o.get("iid" ,""):
            return

        self.application.db.update_image_item(o)

    @tornado.web.authenticated
    def _query(self):
        rows = self.application.db.query_image_items()
        return rows
        #jsonstring = self._json_encoder.encode(items)


class ManageNewsHandler(ManageHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("manage/news.html", news=self._query())

    @tornado.web.authenticated
    def post(self):
        action = self.get_argument("action", "")
        if action == "new":
            self._add({"desc": self.get_argument("desc", ""),
                            "target":self.get_argument("target", "")})
        elif action =="delete":
            self._delete(self.get_argument("nid", -1))
        elif action == "update":
            self._update({"nid": self.get_argument("nid", ""),
                        "desc": self.get_argument("desc", ""),
                        "target":self.get_argument("target", "")})



    @tornado.web.authenticated
    def _add(self, o):
        self.application.db.add_news_item(o)

    @tornado.web.authenticated
    def _delete(self, o):
        self.application.db.del_news_item(o)

    @tornado.web.authenticated
    def _update(self, o):
        if not o.get("nid" ,""):
            return

        self.application.db.update_news_item(o)

    @tornado.web.authenticated
    def _query(self):
        rows = self.application.db.query_news_items()
        return rows

