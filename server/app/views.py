from flask import Blueprint, render_template

general_views = Blueprint('user_views', __name__)

@general_views.route('/')
def showIndex():
    return render_template('index.html')


