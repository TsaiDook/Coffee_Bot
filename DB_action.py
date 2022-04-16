from mysql.connector import connect, Error


def make_connection(host, username, password):
    try:
        with connect(
                host=host,
                user=username,
                password=password,
        ) as connection:
            return connection
    except Error as e:
        raise Exception(e.msg)


def add_user(connection, gender, username, hobbies):
    insert_user_query = f"""
    INSERT INTO USERS (gender, username, hobbies)
    VALUES ({gender}, {username}, {hobbies})
    """
    with connection.cursor() as cursor:
        cursor.execute(insert_user_query)
        connection.commit()


def add_event(connection, author_nickname, topics, activities, place, date, time):
    insert_event_query = f"""
    INSERT INTO EVENTS (author_nickname, topics, activities, place, date, time)
    VALUES ({author_nickname}, {topics}, {activities}, {place}, {date}, {time})
    """
    with connection.cursor() as cursor:
        cursor.execute(insert_event_query)
        connection.commit()


def get_data(connection, users=True):
    table = "USERS" if users else "EVENTS"
    select_data_query = f"SELECT * FROM {table}"
    with connection.cursor() as cursor:
        cursor.execute(select_data_query)
        result = cursor.fetchall()
    return result
