from flask import Flask, request, json
from database import connection, initialize_database
from models.eventsClass import Event
from static.apiUrls import API_URLS
from PostgreSQL import *
from models.listenerClass import listener_class

app = Flask(__name__)


# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World'


# @app.route('api_v1_0/fill', methods=['GET'])
# def fill_base():
#     with connection, connection.cursor() as cursor:
#         pass
#         initialize_database(cursor)  # Инициализация таблиц при необходимости
#


@app.route('/api_v1_0/bot_api', methods=['GET'])
def get_events_as_json():
    init_base()
    with connection, connection.cursor() as cursor:
        cursor.execute("SELECT object, municipality, event_name, event_date, event_address FROM events ORDER BY id DESC LIMIT 10;")
        rows = cursor.fetchall()

    # Mapping rows to Event instances
    events = []
    for row in rows:
        event = Event(*row)  # Assuming row order matches the Event dataclass attributes
        events.append(event)

    # Serialize events to JSON
    serialized_events = [vars(event) for event in events]  # Convert instances to dictionaries
    json_data = json.dumps(serialized_events)

    cursor.close()
    return json_data


# def month_to_interval(month_str):
#     # Преобразование русского месяца в интервал для запроса
#     months = [
#         "январь", "февраль", "март", "апрель",
#         "май", "июнь", "июль", "август",
#         "сентябрь", "октябрь", "ноябрь", "декабрь"
#     ]
#     index = months.index(month_str.lower()) + 1  # индексы месяцев начинаются с 1
#     return f"{months[index - 1]} - {months[index % 12]}"

@app.route('/api_v1_0/bot_api_filter', methods=['GET'])
def filtered():
    if request.args is not None:
        init_base()
        query_parameters = request.args
        city = query_parameters.get('city')
        month = query_parameters.get('date')

        query = "SELECT object, municipality, event_name, event_date, event_address FROM events"

        if city or month:
            query += " WHERE"

            if city:
                query += f" to_tsvector('russian', object || ' ' || municipality || ' ' || event_name || ' ' || event_date || ' ' || event_address) @@ to_tsquery('russian', '{city}')"


            if month:
                # month_interval = month_to_interval(month)
                query += f" to_tsvector('russian', event_date) @@ to_tsquery('russian', '{month}')"

        query += " ORDER BY id DESC;"

        with connection, connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        # Mapping filtered rows to Event instances
        events = []
        for row in rows:
            event = Event(*row)  # Assuming row order matches the Event dataclass attributes
            events.append(event)

        # Serialize events to JSON
        serialized_events = [vars(event) for event in events]  # Convert instances to dictionaries
        json_data = json.dumps(serialized_events)

        return json_data, 200

    return [], 400



def init_base():
    for name, url in API_URLS.items():
        listener = listener_class(url=url)
        stack = listener.get_data()

        with connection, connection.cursor() as cursor:
            initialize_database(cursor)  # Инициализация таблиц при необходимости
            for data in stack:
                cursor.execute(DB_INSERT_TABLE_EVENTS, (data.object,
                                                        data.municipality,
                                                        data.event_name,
                                                        data.event_date,
                                                        data.event_address))
                connection.commit()
            # article_id = cursor.fetchone()[0]

        return 'Done!', 201



# @app.route('/api_v1_0/events', methods=['GET', 'POST'])
# def events():
#     if request.is_json == 'POST':
#         pass
#
#     if request.method == 'GET':
#         if request.is_json:
#             requested_data = json.loads(request.get_json())
#
#         pass


if __name__ == '__main__':
    app.run()
