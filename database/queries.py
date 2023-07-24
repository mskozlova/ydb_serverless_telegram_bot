USERS_INFO_TABLE_PATH = "user_personal_info"
STATES_TABLE_PATH = "states"
    

# Manage tables queries
# truncate_tables_queries = [
#     """
#     DELETE FROM `{}` ON SELECT * FROM `{}`
#     """.format(table_name, table_name)
#     for table_name in [
#         USERS_TABLE_PATH,
#         VOCABS_TABLE_PATH,
#         GROUPS_TABLE_PATH,
#         GROUPS_CONTENTS_TABLE_PATH,
#         LANGUAGES_TABLE_PATH,
#         TRAINING_SESSIONS_TABLE_PATH,
#         TRAINING_SESSIONS_INFO_TABLE_PATH,
#         STATES_TABLE_PATH,
#     ]
# ]

get_user_state = f"""
    DECLARE $user_id AS Uint64;

    SELECT state
    FROM `{STATES_TABLE_PATH}`
    WHERE user_id == $user_id;
"""

set_user_state = f"""
    DECLARE $user_id AS Uint64;
    DECLARE $state AS Utf8?;

    UPSERT INTO `{STATES_TABLE_PATH}` (`user_id`, `state`)
    VALUES ($user_id, $state);
"""

get_user_info = f"""
    DECLARE $user_id AS Int64;
    
    SELECT * FROM `{USERS_INFO_TABLE_PATH}`
    WHERE user_id == $user_id;
"""

add_user_info = f"""
    DECLARE $user_id AS Uint64;
    DECLARE $first_name AS Utf8;
    DECLARE $last_name AS Utf8;
    DECLARE $age AS Uint64;

    INSERT INTO `{USERS_INFO_TABLE_PATH}` (user_id, first_name, last_name, age)
    VALUES ($user_id, $first_name, $last_name, $age);
"""

delete_user_info = f"""
    DECLARE $user_id AS Uint64;

    DELETE FROM `{USERS_INFO_TABLE_PATH}`
    WHERE user_id == $user_id;

    DELETE FROM `{STATES_TABLE_PATH}`
    WHERE user_id == $user_id;
"""
