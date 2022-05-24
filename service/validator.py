from typing import Any, Dict, List, Tuple

from marshmallow import ValidationError

from database.set_db import db


def validator(method: str, request_data: Any, Obj: object, Obj_schema: object) -> dict:
    # validating data structure

    try:
        movie_keys = set(Obj_schema.fields.keys())
        movie_keys.remove('id')
        data_keys = request_data.keys()
        if 'id' in data_keys:
            data_keys = set(data_keys.remove('id'))
        else:
            data_keys = set(data_keys)
        if data_keys != movie_keys:
            messages = {}
            diff1 = movie_keys.difference(data_keys)
            diff2 = data_keys.difference(movie_keys)
            if method in ["PUT", "POST"]:
                for diff_entry in diff1:
                    messages[diff_entry] = "Missing field"
            for diff_entry in diff2:
                messages[diff_entry] = "Unknown field"
            if len(messages) > 0:
                raise ValidationError(message=messages)
    except ValidationError as err:
        error_text_entry = {"PUT": [" full", "required"],
                            "POST": [" full", "required"],
                            "PATCH": ["", "available"]}
        return {'is_error': True,
                "error_message": {"response_status_code": 422,
                                  "response_status": "UNPROCESSABLE ENTITY",
                                  "error_text": "Validation Error. Invalid structure found in request body data. "
                                                "{} request must contain only{} dataset with valid keys for successful "
                                                "processing. {} data keys enumerated in corresponding field"
                                      .format(method, error_text_entry[method][0], error_text_entry[method][1].title()),
                                  f"{error_text_entry[method][1]}_keys": list(movie_keys),
                                  "incorrect_data": err.messages},
                "status_code": 422}

    if method == 'POST':
        # validating if database already contains data
        try:
            if Obj.__name__ == "Movie":
                query = db.session.query(Obj).filter(Obj.title == request_data['title'],
                                                     Obj.year == request_data['year'],
                                                     Obj.director_id == request_data['director_id']).first()
                db.session.close()
            else:
                query = db.session.query(Obj).filter(Obj.name == request_data['name']).first()
                db.session.close()
        except Exception:
            return {'is_error': True,
                    "error_message": f"Database error.",
                    "status_code": 500}

        query_data = Obj_schema.dump(query)
        if len(query_data) > 0:
            return {'is_error': True,
                    "error_message": f"Data already in database. Data ID: {query.id}",
                    "status_code": 400}

    return {'is_error': False, "error_message": None, "status_code": 200}
