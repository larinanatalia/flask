from flask import request, jsonify, Response
from flask.views import MethodView
from models import db, Users, Advertisements
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json


class UserView(MethodView):

    def invalid_id(self, user_id: int) -> dict:
        return {"result": f'User {user_id} not found'}

    def access_denided(self, user_id: int) -> dict:
        return {'result': f'Access denided to notification: {user_id}'}

    def passwords_problem(self) -> dict:
        return {'result': 'Entered passwords are different'}

    def users_exists(self, name: str, mail: str) -> dict:
        return {'result': f'User {name} with e-mail: {mail} already exists'}


    def autentification(self, user_pas: str, input_pas: str) -> bool:
        return check_password_hash(user_pas, input_pas)

    def get(self, user_id=None) -> Response:
        if user_id:
            user = Users.query.get(user_id)
            if user:
                result = user.dict_data()
            else:
                result = self.invalid_id(user_id)
        else:
            users = Users.query.all()
            print(users)
            users_name = [item.dict_data() for item in users]
            result = {'counts users': len(users_name),
                      'result': users_name
                      }
        return jsonify(result)

    def post(self) -> Response:
        name = request.get_json()['name']
        mail = request.get_json()['mail']
        pas = request.get_json()['password']

        users_exists = Users.query.filter(Users.name == name,
                                          Users.mail == mail
                                          ).first()
        if users_exists:
            return jsonify(self.users_exists(name, mail))
        else:
            user = Users(name=name,
                         mail=mail,
                         password=generate_password_hash(pas)
                         )
            db.session.add(user)
            db.session.commit()
            return jsonify(user.dict_data())

    def patch(self, user_id: int) -> Response:
        user = Users.query.get(user_id)
        if user:
            if self.autentification(user.password_hash, request.get_json()['password']):
                new_name = request.get_json()['name']
                new_mail = request.get_json()['mail']
                new_password = generate_password_hash(request.get_json()['new_password'])
                user.name = new_name
                user.mail = new_mail
                user.password_hash = new_password
                db.session.add(user)
                db.session.commit()
                result = user.dict_data()
            else:
                result = self.access_denided(user_id)
        else:
            result = self.invalid_id(user_id)
        return jsonify(result)

    def delete(self, user_id: int) -> Response:
        user = Users.query.get(user_id)
        if user:
            if self.autentification(user.password_hash, request.get_json()['password']):
                db.session.delete(user)
                db.session.commit()
                result = user.dict_data()
            else:
                result = self.access_denided(user_id)
        else:
            result = self.invalid_id(user_id)
        return jsonify(result)


class AdvirtisementsView(MethodView):

    def invalid_id(self, adv_id) -> dict:
        return {'result': f'Advertisement {adv_id} not found'}

    def access_denided(self, user_name: str) -> dict:
        return {'result': f'Access denided for user: {user_name}'}

    def user_doesnt_exist(self, user_name: str) -> dict:
        return {'result': f'User {user_name} does not exist'}

    def autentification(self,
                        owner_name: str,
                        owner_mail: str,
                        owner_pas: str
                        ) -> int:
        owner = Users.query.filter(Users.name == owner_name,
                                   Users.mail == owner_mail
                                   ).first()
        if owner:
            if check_password_hash(owner.password_hash, owner_pas):
                return owner.id
            else:
                return -1
        else:
            None

    def get(self, adv_id=None) -> Response:
        if adv_id:
            advertisement = Advertisements.query.get(adv_id)
            if advertisement:
                result = advertisement.dict_data()
            else:
                result = self.invalid_id(adv_id)
        else:
            advs = Advertisements.query.all()
            adv_list = [item.dict_data() for item in advs]
            result = {'counts': len(adv_list),
                      'result': adv_list
                      }
        return jsonify(result)

    def post(self) -> Response:
        owner_name = request.get_json()['owner']
        owner_mail = request.get_json()['mail']
        owner_pas = request.get_json()['password']

        owner_id = self.autentification(owner_name, owner_mail, owner_pas)

        if owner_id:
            if owner_id != -1:
                title = request.get_json()['title']
                description = request.get_json()['description']
                date = datetime.datetime.now()
                advertisement = Advertisements(title=title,
                                             description=description,
                                             date=date,
                                             owner_id=owner_id
                                             )
                db.session.add(advertisement)
                db.session.commit()
                result = jsonify(advertisement.dict_data())
            else:
                result = self.access_denided(owner_name)
        else:
            result = self.user_doesnt_exist(owner_name)
        return result

    def patch(self, adv_id: int) -> Response:
        adv = Advertisements.query.get(adv_id)
        if adv:
            input_name = request.get_json()['owner']
            input_mail = request.get_json()['mail']
            input_pas = request.get_json()['password']
            input_id = self.autentification(input_name, input_mail, input_pas)
            if input_id:
                if input_id != -1 and input_id == adv.owner_id:
                    adv.title = request.get_json()['title']
                    adv.description = request.get_json()['description']
                    adv.date = datetime.datetime.now()
                    db.session.add(adv)
                    db.session.commit()
                    result = adv.dict_data()
                else:
                    result = self.access_denided(input_name)
            else:
                result = self.user_doesnt_exist(input_name)
        else:
            result = self.invalid_id(adv_id)
        return jsonify(result)

    def delete(self, adv_id: int) -> Response:
        adv = Advertisements.query.get(adv_id)
        if adv:
            input_name = request.get_json()['owner']
            input_mail = request.get_json()['mail']
            input_pas = request.get_json()['password']
            input_id = self.autentification(input_name, input_mail, input_pas)
            if input_id:
                if input_id != -1 and input_id == adv.owner_id:
                    db.session.delete(adv)
                    db.session.commit()
                    tmp = adv.dict_data()
                    tmp['status'] = "removed"
                    result = tmp
                else:
                    result = self.access_denided(input_name)
            else:
                result = self.user_doesnt_exist(input_name)
        else:
            result = self.invalid_id(adv_id)
        return jsonify(result)