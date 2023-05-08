from flask import jsonify
from project.my_app.models.news import News, news_schema, newss_schema
from project.my_app.services.service_validator import service_validator

class ServiceNews:
    def __init__(self, storage_instance):
        self.storage = storage_instance

    def add_new_news(self,request):
        news = request.json["news"]
        user_id = get_id_from_authentication(request)
        newscaster_username = service_validator.validate_user_role("newscaster",user_id).user_name
        self.storage.handle_number_of_news()
        new_News = News(newscaster_username,news)
        self.storage.add_to_database(new_News)
        return jsonify(news_schema.dump(new_News)),201
    
    def get_all_news(self):
        news = self.storage.get_all_news()
        return jsonify(newss_schema.dump(news)),200
    
from project.my_app.app import get_id_from_authentication, storage
service_news = ServiceNews(storage)