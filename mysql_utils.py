import mysql.connector

# Connects to the MySQL database using 'caching_sha2_password' authentication plugin
def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='$Yaga272002',
            database='academicworld',
            auth_plugin='caching_sha2_password' 
        )
        #print("Connected to MySQL database")
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

# Executes the given query and returns the results.
def execute_query(query):
    try:
        connection = connect_to_mysql()
        if connection:
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        else:
            print("Failed to connect to MySQL database.")
            return None
    except mysql.connector.Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        if connection:
            connection.close()

# Returns a list of all universities in the database
def get_distinct_universities():
    query = "SELECT DISTINCT name FROM university"
    results = execute_query(query)
    if results:
        universities = [row[0] for row in results]
        return universities
    else:
        return []

# Returns the number of faculty members at given university 
def get_total_faculty(uni):
    query = f"SELECT COUNT(*) FROM faculty WHERE university_id = (SELECT id FROM university WHERE name = '{uni}')"
    results = execute_query(query)
    if results:
        facs = results[0][0]
        return facs
    else:
        return None

# Returns the number of total publications across all faculty at given university 
def get_total_publications(uni):
    query = f"""
        SELECT COUNT(DISTINCT publication.id)
        FROM publication
        JOIN faculty_publication ON publication.id = faculty_publication.publication_id
        JOIN faculty ON faculty_publication.faculty_id = faculty.id
        JOIN university ON faculty.university_id = university.id
        WHERE university.name = '{uni}'
    """
    results = execute_query(query)
    if results:
        pubs = results[0][0]
        return pubs
    else:
        return None


# Returns top 10 research interests at given univesity
def get_top_RIs(uni):
    query = f"""
        SELECT research_interest, COUNT(*) FROM faculty
        WHERE research_interest != '' AND university_id = (SELECT id FROM university WHERE name = '{uni}')
        GROUP BY research_interest
        ORDER BY COUNT(*) DESC
        LIMIT 10;
    """
    results = execute_query(query)
    if results:
        RIs = results
        return RIs
    else:
        return None

# Returns all research interests at given univesity
def get_all_RIs(uni):
    query = f"""
        SELECT research_interest, COUNT(*) FROM faculty
        WHERE research_interest != '' AND university_id = (SELECT id FROM university WHERE name = '{uni}')
        GROUP BY research_interest
        ORDER BY COUNT(*) DESC;
    """
    results = execute_query(query)
    if results:
        RIs = results
        return RIs
    else:
        return None
    
# Returns faculty members who have given research interest
def get_facs_given_RI(uni, RI):
    query = f"""
        SELECT DISTINCT name, position, photo_url FROM Faculty 
        WHERE research_interest = '{RI}'
        AND university_id = (SELECT id FROM University WHERE name = '{uni}');
    """
    results = execute_query(query)
    if results:
        RIs = results
        return RIs
    else:
        return None

# Returns top 10 keywords at given university
def get_top_kws(uni):
    query = f"""
        SELECT k.name AS keyword, COUNT(*) AS count
        FROM Faculty f
        JOIN Faculty_keyword fk ON f.id = fk.faculty_id
        JOIN Keyword k ON fk.keyword_id = k.id
        WHERE f.university_id = (SELECT id FROM University WHERE name = '{uni}')
        GROUP BY k.name
        ORDER BY count DESC
        LIMIT 10;
    """
    results = execute_query(query)
    if results:
        kws = results
        return kws
    else:
        return None
    
# Adds a favorite faculty member for a user
def add_favorite_faculty(user_name, uni, fac_name):
    if fac_name=="":
        return None
    
    query = f"""
        INSERT INTO FavoriteFaculty (user_name, uni, fac_name) VALUES ('{user_name}', '{uni}', '{fac_name}');
    """
    try:
        connection = connect_to_mysql()
        if connection:
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            connection.commit()
            return results
        else:
            print("Failed to connect to MySQL database.")
            return None
    except mysql.connector.Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        if connection:
            connection.close()


# Removes favorite faculty member for a user
def remove_favorite_faculty(user_name, uni, fac_name):
    if fac_name=="":
        return None
    
    query = f"""
        DELETE FROM FavoriteFaculty WHERE user_name = '{user_name}' AND uni = '{uni}' AND fac_name = '{fac_name}';
    """ 
    try:
        connection = connect_to_mysql()
        if connection:
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            connection.commit()
            return results
        else:
            print("Failed to connect to MySQL database.")
            return None
    except mysql.connector.Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        if connection:
            connection.close()
    

# Returns list of favorite faculty members for a user
def view_favorite_faculty(user_name, uni):
    query = f"""
        SELECT user_name, uni, fac_name FROM FavoriteFaculty WHERE user_name = '{user_name}' AND uni = '{uni}';
    """ 
    results = execute_query(query)
    if results:
        return results
    else:
        return None
    

# Adds favorite keyword for a user
def add_favorite_keyword(user_name, uni, keyword):
    if keyword=="":
        return None
    
    query = f"""
        INSERT INTO FavoriteKeywords (user_name, uni, keyword) VALUES ('{user_name}', '{uni}', '{keyword}');
    """
    try:
        connection = connect_to_mysql()
        if connection:
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            connection.commit()
            return results
        else:
            print("Failed to connect to MySQL database.")
            return None
    except mysql.connector.Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        if connection:
            connection.close()


# Removes favorite keyword for a user
def remove_favorite_keyword(user_name, uni, keyword):
    if keyword=="":
        return None
    
    query = f"""
        DELETE FROM FavoriteKeywords WHERE user_name = '{user_name}' AND uni = '{uni}' AND keyword = '{keyword}';
    """ 
    try:
        connection = connect_to_mysql()
        if connection:
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            connection.commit()
            return results
        else:
            print("Failed to connect to MySQL database.")
            return None
    except mysql.connector.Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        if connection:
            connection.close()
    

# Returns list of favorite keywords for a user
def view_favorite_keyword(user_name, uni):
    query = f"""
        SELECT user_name, uni, keyword FROM FavoriteKeywords WHERE user_name = '{user_name}' AND uni = '{uni}';
    """ 
    results = execute_query(query)
    if results:
        return results
    else:
        return None
    
# Returns university logo url for selected university
def get_uni_imgs(uni):
    query = f"""
        SELECT photo_url FROM University WHERE name = '{uni}';
    """ 
    img_urls = execute_query(query)
    if img_urls:
        return img_urls[0][0]
    else:
        return None
