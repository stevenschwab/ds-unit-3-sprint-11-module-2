from flask import Flask, render_template
from .models import DB, User, Post
from dotenv import load_dotenv
import spacy
from .x import add_or_update_user

def create_app():
    '''
    Create app factory
    '''
    load_dotenv()

    app = Flask(__name__)

    # database configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # register database with the app
    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)
    
    @app.route('/reset')
    def reset():
        # Drop all database tables
        DB.drop_all()
        # Recreate all database tables according to the
        # indicated schema in models.py
        DB.create_all()
        return render_template('base.html', title='Reset Database')
    
    @app.route('/populate')
    def populate():
        # create users in the DB
        add_or_update_user('Austen')
        add_or_update_user('NASA')
        add_or_update_user('Austen')
        add_or_update_user('elonmusk')

        return render_template('base.html', title='Populate Database')
    
    @app.route('/update')
    def update():
        # get list of usernames of all users
        users = User.query.all()
        
        for username in [user.username for user in users]:
            add_or_update_user(username)

        return render_template('base.html', title='Users Updated')

    return app


nlp = spacy.load('my_model/')
# we have the same tool we used in the flask shell
def vectorize_post(post_text):
    '''
    Give the function some text
    Returns a word embedding
    '''
    return nlp(post_text).vector