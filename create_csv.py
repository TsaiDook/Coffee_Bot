import pandas as pd

# базовые версии
# есть трабл с первой колонкой 'Unnamed:0'
users_columns = ['tg_id', 'tg_name', 'push_data', 'gender', 'hobbies', 'conv_topics']
users = pd.DataFrame(columns=users_columns)
users.to_csv('users.csv')

events_columns = ['author_id', 'day', 'month', 'year', 'time']
events = pd.DataFrame(columns=events_columns)
events.to_csv('events.csv')
