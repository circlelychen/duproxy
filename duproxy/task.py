# -*- coding: utf-8 -*-
"""
duproxy.tasks
~~~~~~~~~~~~~~

duproxy tasks module for Celery
"""
from celery.utils.log import get_task_logger
from celery.signals import task_postrun
from flask import current_app

from .core import db
from .application import create_celery_app

logger = get_task_logger(__name__)
celery = create_celery_app()


@celery.task(ignore_result=True)
def update_filestore(g_id, md5):
    filestore = filestores.get_or_404(id_md5)
    logger.info(filestore)
    new_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'],
                                 g_id + md5)
    try:
        shutil.move(filestore.local_path, new_file_path)
    except Exception as e:
        logger.exception(e)
        return
    filestore.local_path = new_file_path
    filestore.g_id = g_id
    return

@task_postrun.connect
def close_session(*args, **kwargs):
    db.session.remove()