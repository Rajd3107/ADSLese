# first run this code

from cassandra.cluster import Cluster

# Connect to Cassandra
cluster = Cluster(['127.0.0.1'])  # Provide Cassandra cluster IP addresses
session = cluster.connect()

# Create a keyspace
keyspace_name = 'root1'
replication_options = {
    'class': 'SimpleStrategy',
    'replication_factor': 3
}
create_keyspace_query = f"CREATE KEYSPACE {keyspace_name} WITH replication = {replication_options};"
session.execute(create_keyspace_query)

# Close the Cassandra session and cluster connection
session.shutdown()
cluster.shutdown()








# delete above code and then run below code

from cassandra.cluster import Cluster


# Connect to Cassandra
cluster = Cluster(['127.0.0.2'])
session = cluster.connect('root1')




def create_table(table_name):
    query = f"CREATE TABLE IF NOT EXISTS {table_name} (name TEXT PRIMARY KEY, age INT, address TEXT)"
    session.execute(query)

def create_data(table_name, data):
    query = f"INSERT INTO {table_name} (name, age, address) VALUES (?, ?, ?)"
    session.execute(query, data)

def read_data(table_name):
    query = f"SELECT * FROM {table_name}"
    result = session.execute(query)
    for row in result:
        print(row)

def update_data(table_name, key_value, new_value):
    query = f"UPDATE {table_name} SET column1 = ? WHERE key_column = ?"
    session.execute(query, (new_value, key_value))

def delete_data(table_name, key_value):
    query = f"DELETE FROM {table_name} WHERE key_column = ?"
    session.execute(query, (key_value,))

create_table('mytable')
create_data('mytable', ('John Doe', 25, 'New York'))
read_data('mytable')
update_data('mytable', 'John Doe', 'Jane Doe')
delete_data('mytable', 'Jane Doe')

session.shutdown()
cluster.shutdown()
