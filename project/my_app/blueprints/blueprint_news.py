from flask import Blueprint

from project.my_app.models.news import News, news_schema, newss_schema
from project.my_app.services.service_news import get_all_news, handle_number_of_news
from project.my_app.services.service_user import get_user
from project.my_app.services.validator_user import validate_user_role
from ..app import add_to_database, get_id_from_authentication, request, jsonify

blueprint_news = Blueprint(name="blueprint_news", import_name=__name__)

@blueprint_news.route('/news',methods=['POST'])
def handle_insert():
    news = request.json["news"]
    user_id = get_id_from_authentication(request)
    newscaster_username = validate_user_role("newscaster",user_id).user_name

    handle_number_of_news()
    new_News = News(newscaster_username,news)
    add_to_database(new_News)
    return jsonify(news_schema.dump(new_News)),201

@blueprint_news.route('/news',methods=['GET'])
def handle_extract():
    news = get_all_news()
    return jsonify(newss_schema.dump(news)),200