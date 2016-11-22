from db import session as db
from db_setup import Category, Item
from flask import flash, url_for, redirect
from functools import wraps


def validate_record(table_name):
    '''View decorator that validates record existance.

    Record is valid if it exists.
    Args:
        table_name: Table (model) to look in.

    Returns:
        Decorated function if record is valid, error if
        record is not valid.

    '''

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # get first argument as record id
            record_id = kwargs[list(kwargs)[0]]
            records = db.query(globals()[table_name]).filter_by(id=record_id)
            if records.count() == 0:
                flash('<strong>Warning!</strong> %s %s does not exist!'%(table_name, record_id), 'warning')
                return redirect(url_for('catalog'))
            return func(*args, **kwargs)
        return wrapper
    return decorator
