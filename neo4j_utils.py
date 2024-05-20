from neo4j import GraphDatabase
import pandas as pd

# Connect to Neo4j Database
class Neo4jConnection:
    def __init__(self, uri, user, password):
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = None
        self._connect()

    def _connect(self):
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def execute_query(self, query, **parameters):
        with self._driver.session() as session:
            result = session.run(query, **parameters)
            return result
        
    def query(self, query, db=None):
        assert self._driver is not None
        session = None
        response = None
        try:
            if db is not None:
                session = self._driver.session(database=db)
            else:
                session = self._driver.session()
            response = list(session.run(query))
        
        except Exception as e:
            print(e)
        
        finally:
            if session is not None:
                session.close()
        return response

# Create connection instance
connection = Neo4jConnection(uri='bolt://localhost:7687', user='neo4j', password='cs411ypatel55')

# Returns list of all faculty at given university
def get_all_faculty(uni):
    query = f"""
        MATCH (i:INSTITUTE {{name: '{uni}'}})<-[:AFFILIATION_WITH]-(f:FACULTY)
        RETURN DISTINCT f.name
    """
    result = connection.query(query, db='academicworld')
    faculty_list = [{'label': record['f.name'], 'value': record['f.name']} for record in result]
    return faculty_list

# Returns list of all faculty who have co-published with given faculty member
def get_co_publications(name):
    query = f"""
        MATCH (faculty1:FACULTY {{name: '{name}'}})-[:PUBLISH]->(PUBLICATION)<-[PUBLISH]-(faculty2:FACULTY)
        WHERE faculty1 <> faculty2
        WITH faculty1, faculty2, COUNT(PUBLICATION) AS co_publications
        RETURN faculty1.name, co_publications, faculty2.name
    """

    result = connection.query(query, db='academicworld')

    cyto_elements = []
    cyto_elements.append({'data': {'id': name, 'label': name}})
    for record in result:      
        cyto_elements.append({'data': {'id': record['faculty2.name'], 'label': record['faculty2.name']}})
        cyto_elements.append({
            'data': {
                'source': name,
                'target': record['faculty2.name'],
                'co_publications': record['co_publications']
            }
        })
    return cyto_elements

# Returns the number of publications per year at given university 
def get_publications_per_year(uni):
    query = f"""
        MATCH (i:INSTITUTE {{name: '{uni}'}})<-[:AFFILIATION_WITH]-(f:FACULTY)-[:PUBLISH]->(p:PUBLICATION)
        WHERE p.year <> 0
        RETURN p.year AS year, count(*) AS count
        ORDER BY year
    """

    result = connection.query(query, db='academicworld')
    data = []
    for item in result:
        year = list(item.keys())[0]
        count = list(item.keys())[1]
        data.append({'year': item[year], 'count': item[count]})
    
    df = pd.DataFrame(data)
    return df