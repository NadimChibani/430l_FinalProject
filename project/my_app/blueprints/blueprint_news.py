from flask import Blueprint
from ..app import  request

class ControllerNews:
    def __init__(self, service_news):
        self.service_news = service_news

    def handle_insert(self):
        return self.service_news.add_new_news(request)
    
    def handle_extract(self):
        return self.service_news.get_all_news()

from project.my_app.services.service_user import service_news
controller_news = ControllerNews(service_news)

blueprint_news = Blueprint(name="blueprint_news", import_name=__name__)

@blueprint_news.route('/news/post',methods=['POST'])
def handle_insert():
    return controller_news.handle_insert()

@blueprint_news.route('/news',methods=['GET'])
def handle_extract():
    return controller_news.handle_extract()
