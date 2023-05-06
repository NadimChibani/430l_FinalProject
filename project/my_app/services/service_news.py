from project.my_app.models.news import News

def handle_number_of_news():
    news = News.query.order_by(News.added_date.desc()).all()
    if len(news) == 3:
        News.query.filter_by(id=news[2].id).delete()

def get_all_news():
    return News.query.order_by(News.added_date.desc()).all()