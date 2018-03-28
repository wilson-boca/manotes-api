from app.initialize import web_app

if __name__ == "wsgi":
    web_app.run()
