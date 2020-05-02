import os
import hashlib
import datetime
from werkzeug.utils import secure_filename
from flask import flash
from models import Storage
from database_methods import to_database
from exif import Image

ALLOWED_EXTENSIONS = ['exif', 'jpg', 'jpeg', 'gif', 'png']


def to_dict(obj, class_name=Storage):
    res = dict()
    for col in class_name.__table__.columns:
        val = getattr(obj, col.name)
        if col.name in ['created', 'uploaded'] and val:
            val = val.strftime("%d-%m-%Y %H:%M")
        elif col.name == 'size' and val:
            val = val / 1024 / 1024
            val = f'{round(val, 2)} Мб'
        elif not val:
            val = ' '
        res[col.name] = val
    return res


def allowed_file(filename):
    return '.' in filename and \
           get_extension(filename) in ALLOWED_EXTENSIONS


def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()


def save_file(file, con, storage_data, input_name, upload_folder):
    img_obj = dict()
    origin_name = secure_filename(file.filename)
    ext = get_extension(origin_name)
    filename = f'{input_name}.{ext}'
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    size = os.path.getsize(file_path)

    system_name = hashlib.md5(
        origin_name.encode('utf-8') + file.content_type.encode(
            'utf-8') + str(size).encode('utf-8')).hexdigest()

    has_file = [x for x in storage_data if x.system_name == system_name]
    if not has_file:
        img_obj.update({
            'name': filename,
            'system_name': system_name,
            'size': size,
            'uploaded': datetime.datetime.now()
        })
        with open(file_path, 'rb') as image_file:
            image = Image(image_file)
            if image.has_exif:

                if getattr(image, 'datetime_original', ''):
                    created = getattr(image, 'datetime_original', '')
                    if created:
                        created = datetime.datetime.strptime(
                            created, '%Y:%m:%d %H:%M:%S')

                img_obj.update({
                    'maker': getattr(image, 'make', ''),
                    'model': getattr(image, 'model', ''),
                    'created': created,
                })

        img = Storage(**img_obj)
        to_database(con, img, action='add')
        con.session.commit()
    else:
        # выдача ошибки о дубликате и удаление из хранилища
        flash('Вы пытаетесь сохранить дубликат файла',
              category='error')
