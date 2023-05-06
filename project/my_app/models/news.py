from ..app import db, ma, datetime


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    newscaster_username = db.Column(db.String(30), db.ForeignKey('user.user_name'),
    nullable=True)
    news = db.Column(db.String(1000),nullable=False)
    added_date = db.Column(db.DateTime)

    def __init__(self,newscaster_username, news):
        super(News, self).__init__(
            newscaster_username=newscaster_username,
            news=news,
            added_date=datetime.datetime.now()
            )
        
class NewsSchema(ma.Schema):
    class Meta:
        fields = ("id", "newscaster_username", "news", "added_date")
        model = News

news_schema = NewsSchema()
