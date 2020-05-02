import os
from app import app
from app import db
from database_connection import Connection
from flask import render_template
from flask import request, redirect, url_for, send_from_directory, flash
from app_methods import allowed_file, to_dict, save_file
from database_methods import get_all, get_obj, to_database


@app.route('/', methods=['GET', 'POST'])
def photo_storage():

    con = Connection(db)
    storage_data = get_all(con)

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            input_name = request.form.get('FileName', 'NoName')
            upload_folder = app.config['UPLOAD_FOLDER']
            save_file(file, con, storage_data, input_name, upload_folder)
        else:
            flash('Файл не является изображением',
                  category='error')

    storage_data = get_all(con)
    data = [to_dict(x) for x in storage_data]
    con.close()

    return render_template('index.html',
                           image_names=data,
                           cache_timeout=30*60)


@app.route('/photo_storage/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/delete_file/<file_id>', methods=['GET'])
def delete_file(file_id):
    con = Connection(db)
    file = get_obj(con, file_id)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file.name))
    to_database(con, file, action='delete')
    con.session.commit()
    con.close()

    return redirect(url_for('photo_storage'))
