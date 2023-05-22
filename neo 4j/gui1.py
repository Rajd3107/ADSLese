from neo4j import GraphDatabase

class Neo4jConnection:
    
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__conn = None
        try:
            self.__conn = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the conn:", e)
        
    def close(self):
        if self.__conn is not None:
            self.__conn.close()
        
    def query(self, query, db=None):
        assert self.__conn is not None, "conn not initialized!"
        session = None
        response = None
        try: 
            session = self.__conn.session(database=db) if db is not None else self.__conn.session() 
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response


conn = Neo4jConnection(uri="bolt://localhost:7687", user="", pwd="")


# res = conn.query("show databases")
# print(res)
# conn.query("CREATE OR REPLACE DATABASE coradb")


query_string = '''
CALL {
LOAD CSV WITH HEADERS FROM
'https://raw.githubusercontent.com/ngshya/datasets/master/cora/cora_content.csv'
AS line FIELDTERMINATOR ','
CREATE (:Paper {id: line.paper_id, class: line.label}) }
'''
conn.query(query_string, db='coradb')

query_string = '''
CALL{
LOAD CSV WITH HEADERS FROM
'https://raw.githubusercontent.com/ngshya/datasets/master/cora/cora_cites.csv'
AS line FIELDTERMINATOR ','
MATCH (citing_paper:Paper {id: line.citing_paper_id}),(cited_paper:Paper {id: line.cited_paper_id})
CREATE (citing_paper)-[:CITES]->(cited_paper)}
'''
conn.query(query_string, db='coradb')

# a = '1152448'
# b = '2354'

# query_string = " MATCH (p1:Paper { id: '" + a + "' }),(p2:Paper { id: '"+b+"' }), path = shortestPath((p1)-[*..15]->(p2)) return path "

# print(query_string)

# res = conn.query(query_string,db='coradb')

# print(res)