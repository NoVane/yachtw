# coding=utf-8
import hashlib
import json
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


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
        self.render("index.html", images=self.application.db.query_image_items())

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
        if self.get_argument("action", "") == "new":
            self._add({"desc": self.get_argument("desc", ""),
                            "url": self.get_argument("url", "")})

    @tornado.web.authenticated
    def _add(self, img):
        self.application.db.add_image_item(img)

    @tornado.web.authenticated
    def _query(self):
        rows = self.application.db.query_image_items()
        return rows
        #jsonstring = self._json_encoder.encode(items)


