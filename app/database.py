"""Defines all the functions related to the database"""
from app import db
import hashlib
import datetime as dt

def insert_new_user(user_id: str, password: str, email: str, first_name: str, last_name: str, phone_number: str) ->  str:
    """Insert new user to users table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """

    password_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = db.connect()
    query = 'Insert Into Users (user_id, password_hash, email, first_name, last_name, phone_number) VALUES ("{}", "{}", "{}", "{}", "{}", "{}");'.format(
        user_id, password_hash, email, first_name, last_name, phone_number)
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    user_id = query_results[0][0]
    conn.close()

    return user_id

def login_user(user_id:str, password:str) -> str:
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    conn = db.connect()
    query = 'SELECT password_hash FROM Users WHERE user_id = "{}";'.format(user_id)
    query_results = conn.execute(query).fetchall()

    if (not query_results):
        return 'No User Found'

    for result in query_results:
        if (not (password_hash == result[0])):
            return 'Wrong Password'

    return 'Success'

def change_first_name(user_id:str, first_name:str):
    conn = db.connect()
    query = 'UPDATE Users SET first_name="{}" WHERE user_id="{}";'.format(first_name, user_id)
    conn.execute(query)

def change_last_name(user_id:str, last_name:str):
    conn = db.connect()
    query = 'UPDATE Users SET last_name="{}" WHERE user_id="{}";'.format(last_name, user_id)
    conn.execute(query)

def change_email(user_id:str, email:str):
    conn = db.connect()
    query = 'UPDATE Users SET email="{}" WHERE user_id="{}";'.format(email, user_id)
    conn.execute(query)

def change_phone(user_id:str, phone_num:str):
    conn = db.connect()
    query = 'UPDATE Users SET phone_number="{}" WHERE user_id="{}";'.format(phone_num, user_id)
    conn.execute(query)

def change_password(user_id:str, password:str):
    conn = db.connect()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    query = 'UPDATE Users SET password_hash="{}" WHERE user_id="{}";'.format(password_hash, user_id)
    conn.execute(query)


def search_user(user_id:str):
    conn = db.connect()
    query = 'SELECT user_id, first_name, last_name, email, phone_number FROM Users WHERE user_id="{}"'.format(user_id)
    query_results = conn.execute(query).fetchall()

    result = query_results[0]
    output = {'user_id': user_id, 'first_name': result[1], 'last_name': result[2], 'email': result[3], 'phone_number': result[4]}
    return output

def search_bubbles(user_id:str):
    conn = db.connect()
    query = 'SELECT bubble_id, bubble_name, description FROM Bubbles NATURAL JOIN (SELECT bubble_id FROM Contains WHERE user_id="{}") AS userBubbles;'.format(user_id)
    query_results = conn.execute(query).fetchall()

    output = []
    for result in query_results:
        curr_dict = {'bubble_id': result[0], 'bubble_name': result[1], 'description': result[2]}
        output.append(curr_dict)

    return output

def is_vaccinated(user_id):
    conn = db.connect()
    query = """
    SELECT DISTINCT v1.user_id
    FROM Vaccinations v1 JOIN Vaccinations v2 ON
	(v1.user_id=v2.user_id 
    AND (
    (v1.vaccine_brand='Johnson & Johnson' AND v2.vaccine_brand='Johnson & Johnson')
    OR (v1.vaccine_brand='Moderna' AND v2.vaccine_brand='Moderna' AND v1.vaccine_date > v2.vaccine_date AND DATEDIFF(v1.vaccine_date, v2.vaccine_date) >= 28 AND DATEDIFF(v1.vaccine_date, v2.vaccine_date) <= 42) 
    OR ((v1.vaccine_brand='Pfizer' AND v2.vaccine_brand='Pfizer' AND v1.vaccine_date > v2.vaccine_date AND DATEDIFF(v1.vaccine_date, v2.vaccine_date) >= 21 AND DATEDIFF(v1.vaccine_date, v2.vaccine_date) <= 42))));
    """
    query_results = conn.execute(query).fetchall()
    for result in query_results:
        if (result[0] == user_id):
            return True

    return False

def is_infected(user_id):
    conn = db.connect()
    query = """
            SELECT tests.user_id
            FROM Test_Results tests JOIN (SELECT MAX(test_id) AS last_id
					FROM Test_Results
					GROUP BY user_id) AS latest_test
                    ON (tests.test_id=latest_test.last_id)
                    WHERE tests.result = 1;
            """
    query_results = conn.execute(query).fetchall()
    for result in query_results:
        if (result[0] == user_id):
            return True

    return False

def is_at_risk(user_id):
    conn = db.connect()
    query = 'Select user_id FROM AtRisk'
    query_results = conn.execute(query).fetchall()
    for result in query_results:
        if (result[0] == user_id):
            return True

    return False

### NATALIA'S DATABASE (BUBBLES PAGES)

def get_num_users(bubble_id) -> int:
    """ Finds the number of users in bubble with specified bubble id

    Returns:
        The number of users in the bubble
    """

    conn = db.connect()
    query = """
    SELECT Bubbles.bubble_id, bubble_name, description, num_users
    FROM Bubbles
    JOIN (
        SELECT bubble_id, COUNT(user_id) AS num_users
        FROM Contains
        GROUP BY Contains.bubble_id
    ) AS User_Count
    ON Bubbles.bubble_id = User_Count.bubble_id
    ORDER BY num_users DESC;
    """
    query_results = conn.execute(query).fetchall()
    conn.close()
    for result in query_results:
        if result[0] == bubble_id:
            return result[3]
    return 0


def fetch_user_bubbles(user_id) -> dict:
    """ Reads all bubbles that this user is in

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query = """
    SELECT Bubbles.bubble_id, bubble_name, description
    FROM Contains
    JOIN Bubbles ON Contains.bubble_id = Bubbles.bubble_id
    WHERE Contains.user_id = '{}'
    """.format(user_id)
    query_results = conn.execute(query).fetchall()
    conn.close()
    bubbles = []
    for result in query_results:
        bubble = {
            "bubble_id": result[0],
            "name": result[1],
            "description": result[2],
            "num_users": get_num_users(result[0])
        }
        bubbles.append(bubble)
    return bubbles


def fetch_bubble_users(bubble_id) -> dict:
    """ Reads all users in this bubble

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query = """
    SELECT Users.user_id, first_name, last_name
    FROM Users
    JOIN Contains ON Users.user_id = Contains.user_id
    WHERE bubble_id = {}
    """.format(bubble_id)
    query_results = conn.execute(query).fetchall()
    conn.close()
    users = []
    for result in query_results:
        user = {
            "user_id": result[0],
            "first_name": result[1],
            "last_name": result[2]
        }
        users.append(user)
    return users


def fetch_user(user_id) -> dict:
    """ Gets the user information for a given user

    Return:
        The user information in a dictionary
    """

    conn = db.connect()
    query = """
    SELECT *
    FROM Users
    WHERE Users.user_id = '{}'
    """.format(user_id)
    query_results = conn.execute(query).fetchone()
    conn.close()
    return query_results


def fetch_bubble(bubble_id) -> dict:
    """ Gets the information for a given bubble

    Return:
        The information related to the specified bubble
    """

    conn = db.connect()
    query = """
    SELECT *
    FROM Bubbles
    WHERE Bubbles.bubble_id = {}
    """.format(bubble_id)
    query_results = conn.execute(query).fetchone()
    conn.close()
    return query_results


def edit_bubble(bubble_id, data) -> None:
    """ Update the bubble name and description

    Args:
        bubble_id (int): Targeted bubble_id
        data (dict): Dictionary containing new bubble name and description

    Returns:
        None
    """

    conn = db.connect()
    query = """
    UPDATE Bubbles
    SET bubble_name = '{}', description = '{}'
    WHERE bubble_id = {}
    """.format(data['bubble_name'], data['bubble_description'], int(bubble_id))
    query_results = conn.execute(query)
    conn.close()


def create_bubble(data) -> None:
    """ Create a new bubble

    Args:
        data (dict): Dictionary containing new bubble name, description, 
        and the id of the user who created the bubble

    Returns:
        None
    """

    conn = db.connect()
    query1 = """
    SELECT MAX(bubble_id)
    FROM Bubbles
    """
    max_bubble = conn.execute(query1).fetchone()[0]
    max_bubble += 1
    query2 = """
    INSERT INTO Bubbles (bubble_id, bubble_name, description)
    VALUES ({}, '{}', '{}')
    """.format(max_bubble, data['bubble_name'], data['bubble_description'])
    conn.execute(query2)
    query3 = """
    INSERT INTO Contains (user_id, bubble_id)
    VALUES ('{}', {})
    """.format(data['user_id'], max_bubble)
    conn.execute(query3)
    conn.close()


def remove_bubble_user(bubble_id, user_id) -> None:
    """ Remove a user from a bubble

    Args:
        bubble_id (int): Targeted bubble_id
        user_id (str): Targeted user_id

    Returns:
        None
    """

    conn = db.connect()
    query = """
    DELETE
    FROM Contains
    WHERE Contains.user_id = '{}' AND Contains.bubble_id = {}
    """.format(user_id, bubble_id)
    conn.execute(query)
    conn.close()


def user_search(search_string, bubble_id) -> list:
    """ Searches for users starting with search string

    Args:
        search_string (str): String to search for

    Returns:
        A list of users matching the search string
    """

    search_string = search_string.lower()
    conn = db.connect()
    query = """
    SELECT user_id, first_name, last_name
    FROM Users
    WHERE ((LOWER(user_id) LIKE '%%{}%%') OR (LOWER(first_name) LIKE '%%{}%%') OR (LOWER(last_name) LIKE '%%{}%%')) AND (user_id NOT IN (
        SELECT user_id
        FROM Contains
        WHERE Contains.bubble_id = {}
    ))
    """.format(search_string, search_string, search_string, bubble_id)
    
    query_results = conn.execute(query).fetchall()
    conn.close()
    users = []
    for result in query_results:
        user = {
            "user_id": result[0],
            "first_name": result[1],
            "last_name": result[2],
        }
        users.append(user)
    return users


def add_users(bubble_id, user_list) -> None:
    """ Adds all the users to the given bubble

    Args:
        bubble_id: What bubble to add the users to
        user_list: Which users to add
    
    Returns:
        None:
    """

    conn = db.connect()
    for user in user_list:
        query = """
        INSERT INTO Contains (user_id, bubble_id)
        VALUES ('{}', {})
        """.format(user, bubble_id)
        conn.execute(query)
    conn.close()
    

### BADRIS'S DATABASE - START (INTERACTION TABLE)

def fetch_todo_interactions(user_id) -> dict:
    # """Reads all tasks listed in the todo table

    # Returns:
    #     A list of dictionaries
    # """

    conn = db.connect()
    # query_results = conn.execute("select case when days='Monday' then interactions else '' end as Monday,\
    #                             case when days='Tuesday' then interactions else '' end as Tuesday,\
    #                             case when days='Wednesday' then interactions else '' end as Wednesday,\
    #                             case when days='Thursday' then interactions else '' end as Thursday,\
    #                             case when days='Friday' then interactions else '' end as Friday,\
    #                             case when days='Saturday' then interactions else '' end as Saturday,\
    #                             case when days='Sunday' then interactions else '' end as Sunday\
    #                             from\
    #                             (select dayname(a.interaction_date) as days,group_concat(c.user_id SEPARATOR ';') as interactions from Interactions a\
    #                             join (select * from Participates where interaction_id in (select interaction_id from Participates where user_id='AdelaGowans'))c\
    #                             on a.interaction_id=c.interaction_id\
    #                             join(select '1',max(interaction_date) as max_date from Interactions group by '1') b\
    #                             on a.interaction_id>=1\
    #                             WHERE a.interaction_date>=  max_date- INTERVAL 7 DAY and user_id!='AdelaGowans'\
    #                             group by dayname(a.interaction_date))a;").fetchall()

    query="call proc1('{}','2021-03-01');".format(user_id)
    query_results = conn.execute(query).fetchall()

    list1=[]
    for v in query_results:
        for column, value in v.items():
            list1.append(column)
    dates=[x.strip("'") for x in list1]
    dates1=[dt.datetime.strptime(i, '%Y-%m-%d') for i in dates]
    list1=[i.strftime('%b %d,%y') for i in dates1]

    # print(query_results)
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "Day1": result[0],
            "Day2": result[1],
            "Day3": result[2],
            "Day4": result[3],
            "Day5": result[4],
            "Day6": result[5],
            "Day7": result[6]
        }
        todo_list.append(item)

    # return todo_list
    # todo_list = [
    # {"interaction_id": 1, "interaction_date": "2020-01-01" , "location": "Loc1","notes":"123","bubble_id":12},
    # {"interaction_id": 2, "interaction_date": "2020-01-01" , "location": "Loc2","notes":"234","bubble_id":14}\
    # ]
    
    # todo_list=pd.read_csv('Interactions-2.csv')

    return todo_list,list1


def fetch_todo_interactions3(user_id) -> dict:
    conn = db.connect()
    query="select interaction_id, interaction_date, location, notes, bubble_id, bubble_name from Interactions NATURAL JOIN (SELECT interaction_id FROM Participates WHERE user_id='{}') AS b  NATURAL JOIN (SELECT bubble_id, bubble_name FROM Bubbles) AS bubs;".format(user_id)
    # query="select * from Interactions;"
    query_results = conn.execute(query).fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "interaction_id": result[0],
            "interaction_date": result[1],
            "location": result[2],
            "notes": result[3],
            "bubble_id": result[4],
            "bubble_name": result[5]
        }
        todo_list.append(item)

    return todo_list


def fetch_todo_interactions2(value, user_id) -> dict:
    # """Reads all tasks listed in the todo table

    # Returns:
    #     A list of dictionaries
    # """

    conn = db.connect()
    # query="select case when days='Monday' then interactions else '' end as Monday,\
    #                             case when days='Tuesday' then interactions else '' end as Tuesday,\
    #                             case when days='Wednesday' then interactions else '' end as Wednesday,\
    #                             case when days='Thursday' then interactions else '' end as Thursday,\
    #                             case when days='Friday' then interactions else '' end as Friday,\
    #                             case when days='Saturday' then interactions else '' end as Saturday,\
    #                             case when days='Sunday' then interactions else '' end as Sunday\
    #                             from\
    #                             (select dayname(a.interaction_date)as days,group_concat(c.user_id SEPARATOR ';') as interactions from Interactions a\
    #                             join (select * from Participates where interaction_id in (select interaction_id from Participates where user_id='{}'))c\
    #                             on a.interaction_id=c.interaction_id\
    #                             join(select '1',max(interaction_date) as max_date from Interactions where interaction_date<=DATE(CONCAT_WS('-',{},{},{})) group by '1') b\
    #                             on a.interaction_id>=1\
    #                             WHERE a.interaction_date>=  max_date- INTERVAL 7 DAY and a.interaction_date<=max_date and user_id!='{}'\
    #                             group by dayname(a.interaction_date))a;".format(user_id, year,month,day, user_id)

    query="call proc1('{}','{}');".format(user_id,value)
    query_results = conn.execute(query).fetchall()
    list1=[]
    for v in query_results:
        for column, value in v.items():
            
            list1.append(column)
    dates=[x.strip("'") for x in list1]
    dates1=[dt.datetime.strptime(i, '%Y-%m-%d') for i in dates]
    list1=[i.strftime('%b %d,%y') for i in dates1]


    print(query_results)
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "Day1": result[0],
            "Day2": result[1],
            "Day3": result[2],
            "Day4": result[3],
            "Day5": result[4],
            "Day6": result[5],
            "Day7": result[6]
        }
        todo_list.append(item)

    # return todo_list
    # todo_list = [
    # {"interaction_id": 1, "interaction_date": "2020-01-01" , "location": "Loc1","notes":"123","bubble_id":12},
    # {"interaction_id": 2, "interaction_date": "2020-01-01" , "location": "Loc2","notes":"234","bubble_id":14}\
    # ]
    
    # todo_list=pd.read_csv('Interactions-2.csv')

    return todo_list,list1


def update_interactions(location: str,task_id: int, text: str) -> None:
    """Updates task description based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated description

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update Interactions set {} = "{}" where interaction_id = {};'.format(location,text, task_id)
    print('Updated')
    conn.execute(query)
    conn.close()


def insert_new_interactions(dates: str,location: str,notes: str,bubble_id: int,user_id) ->  int:
    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
  

    query = 'Insert Into Interactions (interaction_date,location,notes,bubble_id) VALUES ("{}","{}","{}","{}");'.format(dates,location,notes,bubble_id)
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")

    query_results = [x for x in query_results]
    task_id = query_results[0][0]


    # query_results1='insert into Participates VALUES ("{}","{}");'.format(user_id,task_id)
    # conn.execute(query_results1)

    query='select distinct user_id from Contains where bubble_id={}'.format(bubble_id)
    query_results2=conn.execute(query).fetchall()

    final_result = [i[0] for i in query_results2]

    for i in final_result:
        temp='insert into Participates VALUES ("{}","{}");'.format(i,task_id)
        conn.execute(temp)
        

    
    conn.close()

    return task_id    


def remove_interactions(task_id: int) -> None:
    """ remove entries based on task ID """
    conn = db.connect()
    query = 'Delete From Interactions where interaction_id={};'.format(task_id)
    conn.execute(query)

    query = 'Delete From Participates where interaction_id={};'.format(task_id)
    conn.execute(query)


    conn.close()



def fetch_todo_search_interaction(keyword: str) -> dict:
    # """Reads all tasks listed in the todo table

    # Returns:
    #     A list of dictionaries
    # """

    conn = db.connect()
    query = 'select * From Interactions where location="{}";'.format(keyword)
    query_results = conn.execute(query).fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "interaction_id": result[0],
            "interaction_date": result[1],
            "location": result[2],
            "notes": result[3],
            "bubble_id": result[4]
        }
        todo_list.append(item)

    return todo_list


### BADRIS'S DATABASE - END (INTERACTION TABLE)




    
    
    
 ### Pratheek's Databas (Vaccination and Test results pages)

def fetch_vac() -> dict:
    """"Reads all vaccination records listed in the vaccine table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("Select * from Vaccinations;").fetchall()
    conn.close()
    vac_list = []
    for result in query_results:
        item = {
            "vac_id": result[0],
            "user_id": result[1],
            "vaccine_brand": result[2],
            "vaccine_date": result[3]
        }
        vac_list.append(item)

    return vac_list



def fetch_query() -> dict:
    """"Reads all the testing frequency  from the advanced query

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("SELECT tr.user_id,COUNT(DISTINCT tr.test_date) as num_tests,COUNT(DISTINCT tr.test_date)/COUNT(DISTINCT month(tr.test_date)) as testing_frequency, MAX(tr.test_date) as recent_test,COUNT(DISTINCT v.vac_id) as num_vaccinations,MAX(v.vaccine_date)as recent_vaccination FROM Test_Results tr JOIN Vaccinations v ON tr.user_id = v.user_id GROUP BY tr.user_id ORDER BY tr.user_id ASC").fetchall()
    conn.close()
    result_list = []
    for result in query_results:
        item = {
            "user_id": result[0],
            "num_tests": result[1],
            "testing_frequency": result[2],
            "recent_test": result[3],
            "num_vaccinations":result[4],
            "recent_vaccination":result[5]
        }
        result_list.append(item)

    return result_list


def update_vac_entry(location: str,vac_id: int, text: str) -> None:
    """Updates vaccination entry based on given `vac_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated description

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update Vaccinations Set {} = "{}" Where vac_id = {};'.format(location,text, vac_id)
    conn.execute(query)
    conn.close()




def insert_new_vac(user_id: str,vaccine_brand : str,vaccine_date: str) ->  int:
    """Insert new vaccination record to vaccination table.


    Returns: The vac ID for the inserted entry
    """

    conn = db.connect()
    query = 'Insert Into Vaccinations (user_id,vaccine_brand,vaccine_date) VALUES ("{}","{}","{}");'.format(
        user_id,vaccine_brand,vaccine_date )
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id


def remove_vac_by_id(vac_id: int) -> None:
    """ remove entries based on vac ID """
    conn = db.connect()
    query = 'Delete From Vaccinations where vac_id={};'.format(vac_id)
    conn.execute(query)
    conn.close()

def search_vac(key : str)-> dict:
    """ search and return the vaccination records of the given user id"""
    conn = db.connect()
    query_results = conn.execute('Select * From Vaccinations where user_id like "{}";'.format(key)).fetchall()
    conn.close()

    todo_list = []

    for result in query_results:
        item = {
            "vac_id": result[0],
            "user_id": result[1],
            "vaccine_brand": result[2],
            "vaccine_date": result[3]
        }
        todo_list.append(item)
        
    return todo_list



def searchQ_task(key : str)-> dict:
    """ search and return the testing frequency statistics of the given user id"""

    conn = db.connect()
    query_results = conn.execute('SELECT * FROM (SELECT tr.user_id as user_id,COUNT(DISTINCT tr.test_date) as num_tests,COUNT(DISTINCT tr.test_date)/COUNT(DISTINCT month(tr.test_date)) as testing_frequency, MAX(tr.test_date) as recent_test,COUNT(DISTINCT v.vac_id) as num_vaccinations,MAX(v.vaccine_date)as recent_vaccination FROM Test_Results tr JOIN Vaccinations v ON tr.user_id = v.user_id GROUP BY tr.user_id ORDER BY tr.user_id ASC) as temp WHERE temp.user_id LIKE "{}";'.format(key)).fetchall()
    conn.close()

    tf_list = []

    for result in query_results:
        item = {
            "user_id": result[0],
            "num_tests": result[1],
            "testing_frequency": result[2],
            "recent_test": result[3],
            "num_vaccinations":result[4],
            "recent_vaccination":result[5]
        }
        tf_list.append(item)
        
    return tf_list

def fetch_test() -> dict:
    """"Reads all tests listed in the Test Results table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("Select * from Test_Results;").fetchall()
    conn.close()
    test_list = []
    for result in query_results:
        item = {
            "test_id": result[0],
            "result": result[1],
            "test_date": result[2],
            "user_id": result[3]
        }
        test_list.append(item)

    return test_list

def remove_test_by_id(test_id: int) -> None:
    """ remove entries based on test ID """
    conn = db.connect()
    query = 'Delete From Test_Results where test_id={};'.format(test_id)
    conn.execute(query)
    conn.close()

def insert_new_test(result: int,test_date : str,user_id: str) ->  int:
    """Insert new task to test results table.


    Returns: The test ID for the inserted entry
    """
    print('Inserting new test')
    print('Result: ')
    print(result)
    conn = db.connect()
    query = 'Insert Into Test_Results (result,test_date,user_id) VALUES ("{}","{}","{}");'.format(
        result,test_date,user_id )
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]

    if (result == '1'):
        print('Result is Positive')
        print('Calling Stored Procedure')
        store_proc = 'CALL HandlePositiveResult("{}", "{}");'.format(user_id, test_date)
        proc_results = conn.execute(store_proc)
        for res in proc_results:
            print(res[0])

    
    conn.close()

    return task_id

def update_test_entry(location: str,test_id: int, text) -> None:
    """Updates test entry based on given `vac_id'

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update Test_Results Set {} = "{}" Where test_id = {};'.format(location,text, test_id)
    conn.execute(query)
    conn.close()

def search_test(key : str)-> dict:
    """ search and return the testing records of the given user id"""

    conn = db.connect()
    query_results = conn.execute('Select * From Test_Results where user_id like "{}";'.format(key)).fetchall()
    conn.close()

    test_record_list = []

    for result in query_results:
        item = {
            "test_id": result[0],
            "result": result[1],
            "test_date": result[2],
            "user_id": result[3]
        }
        test_record_list.append(item)
        
    return test_record_list
