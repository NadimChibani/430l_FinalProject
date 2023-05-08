from flask import abort
import re

def validate_news(news):
    regex_pattern = r'^(?=[a-zA-Z])(?=.{1,300}$)(?!.*[<>;"\/\[\]{}()=+&%*#@!,\\]).*$'
    if not re.match(regex_pattern, str(news)):
        abort(400, 'News input is incorrect, please change it')