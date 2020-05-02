from models import Storage
from flask import flash


def get_all(con):
    return con.session.query(Storage).order_by(Storage.uploaded.desc()).all()


def get_obj(con, obj_id):
    return con.session.query(Storage).get(obj_id)


def to_database(con, obj, action='add'):
    try:
        if action == 'add':
            con.session.add(obj)
        elif action == 'delete':
            con.session.delete(obj)
        con.session.flush()
    except Exception as err:
        flash('Ошибка при работе с БД', category='error')
        print(err)
        con.session.rollback()
