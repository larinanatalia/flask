from settings import app
from models import db
from views import UserView, AdvirtisementsView

if __name__ == "__main__":
    @app.before_first_request
    def create_table():
        db.create_all()

    app.add_url_rule('/users/<user_id>', view_func=UserView.as_view('user'))
    app.add_url_rule('/users/', view_func=UserView.as_view('users'))
    app.add_url_rule('/adv/<adv_id>', view_func=AdvirtisementsView.as_view('adv'))
    app.add_url_rule('/adv/', view_func=AdvirtisementsView.as_view('advs'))

    app.run(host='0.0.0.0', port=5000)
