import json

from database import queries
from database.utils import execute_select_query, execute_update_query


def get_state(pool, user_id):
    results = execute_select_query(pool, queries.get_user_state, user_id=user_id)
    if len(results) == 0:
        return None
    if results[0]["state"] is None:
        return None
    return json.loads(results[0]["state"])


def set_state(pool, user_id, state):
    execute_update_query(
        pool, queries.set_user_state, user_id=user_id, state=json.dumps(state)
    )


def clear_state(pool, user_id):
    execute_update_query(pool, queries.set_user_state, user_id=user_id, state=None)


def add_user_info(pool, user_id, first_name, last_name, age):
    execute_update_query(
        pool,
        queries.add_user_info,
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        age=age,
    )


def get_user_info(pool, user_id):
    result = execute_select_query(pool, queries.get_user_info, user_id=user_id)

    if len(result) != 1:
        return None
    return result[0]


def delete_user_info(pool, user_id):
    execute_update_query(pool, queries.delete_user_info, user_id=user_id)
