""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from app import database as db_helper


# Begin Kevin's Routes
@app.route("/create_user", methods=['POST'])
def create_user():
    """ recieves post requests to add new task """
    data = request.get_json()
    print(request)
    db_helper.insert_new_user(data['user_id'], data['password'], data['email'], data['first_name'], data['last_name'], data['phone_number'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    query_result = db_helper.login_user(data['user_id'], data['password'])
    result = {'success':True, 'response': 'Login Success'}
    if (query_result == 'No User Found'):
        result['success'] = False
        result['response'] = 'No User Found'
    elif (query_result == 'Wrong Password'):
        result['success'] = False
        result['response'] = 'Wrong Password'
    return jsonify(result)

@app.route("/profile/<string:user_id>", methods=['GET'])
def profile(user_id):
    user = db_helper.search_user(user_id)
    bubbles = db_helper.search_bubbles(user_id)
    is_vac = db_helper.is_vaccinated(user_id)
    risk = db_helper.is_at_risk(user_id)
    is_infected = db_helper.is_infected(user_id)
    print(is_vac)
    print(risk)
    print(is_infected)
    return render_template("profile.html", user=user, bubbles=bubbles, is_vac=is_vac, risk=risk, is_infected=is_infected)

@app.route("/edit-first-name", methods=['POST'])
def edit_first_name():
    data = request.get_json()
    db_helper.change_first_name(data['user_id'], data['first_name'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/edit-last-name", methods=['POST'])
def edit_last_name():
    data = request.get_json()
    db_helper.change_last_name(data['user_id'], data['last_name'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/edit-email", methods=['POST'])
def edit_email():
    data = request.get_json()
    db_helper.change_email(data['user_id'], data['email'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/edit-phone", methods=['POST'])
def edit_phone():
    data = request.get_json()
    db_helper.change_phone(data['user_id'], data['phone_number'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/edit-password", methods=['POST'])
def edit_password():
    data = request.get_json()
    db_helper.change_password(data['user_id'], data['password'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/")
def homepage():
    """ returns rendered homepage """
    return render_template("login.html")



# End Kevin's Routes

### NATALIA'S ROUTES (BUBBLES PAGES)

@app.route("/user-bubbles/<string:user_id>")
def user_bubbles_page(user_id):
    """ returns rendered user bubbles page """
    bubbles = db_helper.fetch_user_bubbles(user_id)
    user = db_helper.fetch_user(user_id)
    return render_template("user_bubbles.html", user_id=user_id, first_name=user['first_name'], last_name=user['last_name'], bubbles=bubbles)


@app.route("/bubble-page/<string:user_id>/<int:bubble_id>")
def bubble_page(user_id, bubble_id):
    """ returns rendered bubble page """
    bubble = db_helper.fetch_bubble(bubble_id)
    users = db_helper.fetch_bubble_users(bubble_id)
    return render_template("bubble_page.html", user_id=user_id, bubble=bubble, users=users)


@app.route('/edit-bubble/<int:bubble_id>', methods=['POST'])
def edit_bubble(bubble_id):
    data = request.get_json()
    db_helper.edit_bubble(bubble_id, data)
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route('/create-bubble', methods=['POST'])
def create_bubble():
    data = request.get_json()
    db_helper.create_bubble(data)
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route('/delete/<int:bubble_id>/<string:user_id>', methods=['POST'])
def remove_bubble_user(bubble_id, user_id):
    db_helper.remove_bubble_user(bubble_id, user_id)
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route('/user-search/<int:bubble_id>/<string:search_string>', methods=['GET'])
def user_search(bubble_id, search_string):
    user_list = db_helper.user_search(search_string, bubble_id)

    result = {'success': True, 'response': user_list}
    return jsonify(result)


@app.route('/add-users', methods=['POST'])
def add_users():
    data = request.get_json()
    db_helper.add_users(data['bubble_id'], data['user_ids'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)



##############BADRI's ROUTES - Start (Interaction table page)##############################

@app.route("/interactions/<string:user_id>", methods=['GET'])
def interactions(user_id):
    """ receives post requests to add new task """
    user = db_helper.search_user(user_id)
    items,lists = db_helper.fetch_todo_interactions(user['user_id'])
    items2 = db_helper.fetch_todo_interactions3(user['user_id'])

    
    
    bubbles = db_helper.search_bubbles(user_id)
    
    return render_template("interaction_table.html", items=items, user = user,items2=items2, bubbles=bubbles, lists=lists)


@app.route("/interactions/<string:user_id>/search_date/<string:input>", methods=['GET'])
def search_interactions(user_id,input):
    """ receives post requests to add new task """
    value=input
    user = db_helper.search_user(user_id)
    # items = db_helper.fetch_todo_interactions2(int(value.split('-')[0]),int(value.split('-')[1]),int(value.split('-')[2]),user['user_id'])
    items,lists = db_helper.fetch_todo_interactions2(value,user['user_id'])
    items2 = db_helper.fetch_todo_interactions3(user['user_id'])
    return render_template("interaction_table.html", items=items, user = user,items2=items2,lists=lists)

@app.route("/edit_interaction/<int:task_id>", methods=['POST'])
def update_task_interactions(task_id):
    """ recieved post requests for entry updates """

    data = request.get_json()
    print('the data in update is ',data)
    try:
        if data["description1"]!='':
            db_helper.update_interactions('interaction_date',task_id, data["description1"])
            result = {'success': True, 'response': 'Status Updated'}
        if data["description2"]!='':
            db_helper.update_interactions('location',task_id, data["description2"])
            result = {'success': True, 'response': 'Task Updated'}
        if data["description3"]!='':
            db_helper.update_interactions('notes',task_id, data["description3"])
            result = {'success': True, 'response': 'Task Updated'}
        if data["description4"]!='':
            db_helper.update_interactions('bubble_id',task_id, data["description4"])
            result = {'success': True, 'response': 'Task Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

@app.route("/create_interaction/<string:user_id>", methods=['POST'])
def create_task_interactions(user_id):
    """ receives post requests to add new task """
    data = request.get_json()

    print('the data is ',data)

    db_helper.insert_new_interactions(data['description1'],data['description2'],data['description3'],data['description4'],user_id)
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route("/delete_interaction/<int:task_id>", methods=['POST'])
def delete_interaction(task_id):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_interactions(task_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)



@app.route("/search_interaction/<string:search_string>", methods=['GET'])
def search_interactions_query(search_string,user_id):
    """ receives post requests to add new task """
    print('It is',search_string)
    # data = request.get_json()

    user = db_helper.search_user(user_id)

    items = db_helper.fetch_todo_interactions()
    items2 = db_helper.fetch_todo_search_interaction(search_string)

    print('done')

    return render_template("interaction_table.html",items=items,items2=items2,user=user)


##############BADRI's ROUTES - End (Interaction table page)##############################




### Pratheek's Routes (Vaccination and test pages)

@app.route("/delete-vaccination/<int:task_id>", methods=['POST'])
def delete(task_id):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_vac_by_id(task_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/edit-vaccination/<int:task_id>/<string:user_id>", methods=['POST'])
def update(task_id,user_id):
    """ recieved post requests for entry kdb"""

    data = request.get_json()


    try:
        if user_id!='':
            db_helper.update_vac_entry('user_id',task_id, user_id)
            result = {'success': True, 'response': 'Task Updated'}
        if data["vaccine_brand"]!='':
            db_helper.update_vac_entry('vaccine_brand',task_id, data["vaccine_brand"])
            result = {'success': True, 'response': 'Task Updated'}
        if data["vaccine_date"]!='':
            db_helper.update_vac_entry('vaccine_date',task_id, data["vaccine_date"])
            result = {'success': True, 'response': 'Task Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/create-vaccination/<string:user_id>", methods=['POST'])
def create(user_id):
    """ recieves post requests to add new task """
    data = request.get_json()
    db_helper.insert_new_vac(user_id,data['vaccine_brand'],data['vaccine_date'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/vaccinations")
def vaccinations():
    """ returns rendered homepage """
    items = db_helper.fetch_vac()
    return render_template("vaccinations.html", items=items)

@app.route("/search-vaccination/<string:user_id>", methods=['GET'])
def search(user_id):
    """ recieves get requests to search for a key word """
    # data = request.glt_json()
    items = db_helper.search_vac(user_id)
    result = {'success': True, 'response': 'Done'}
    return render_template("user_vaccinations.html", vaccinations=items,user_id = user_id)


@app.route("/query")
def querypage():
    """ returns rendered homepage """
    items = db_helper.fetch_query()
    return render_template("testing_frequency.html", items=items)

@app.route("/searchQ/<string:search_string>", methods=['GET'])
def searchQ(search_string):
    """ recieves get requests to search for a key word """
    # data = request.glt_json()
    items = db_helper.searchQ_task(search_string)
    result = {'success': True, 'response': 'Done'}
    

    return render_template("testing_frequency.html", items=items,user_id = search_string)

@app.route("/delete-test/<int:task_id>", methods=['POST'])
def delete_test(task_id):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_test_by_id(task_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

@app.route("/create-test/<string:user_id>", methods=['POST'])
def create_test(user_id):
    """ recieves post requests to add new task """
    data = request.get_json()
    db_helper.insert_new_test(data['result'],data['test_date'],user_id)
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/tests")
def homepage_tests():
    """ returns rendered homepage """
    items = db_helper.fetch_test()
    return render_template("tests.html", items=items)

@app.route("/edit-test/<int:task_id>/<string:user_id>", methods=['POST'])
def update_test(task_id,user_id):
    """ recieved post requests for entry kdb"""

    data = request.get_json()


    try:
        # if "description1" in data:
        #     db_helper.update_task_entry(task_id, data['description2'],data['description3'],data['description4'])
        #     result = {'success': True, 'response': 'Task Updated'}
        # else:
        #     result = {'success': True, 'response': 'Nothing Updated'}
        if data["result"]!='':
            db_helper.update_test_entry('result',task_id, data["result"])
            result = {'success': True, 'response': 'Task Updated'}
        if data["test_date"]!='':
            db_helper.update_test_entry('test_date',task_id, data["test_date"])
            result = {'success': True, 'response': 'Task Updated'}
        if user_id!='':
            db_helper.update_test_entry('user_id',task_id, user_id)
            result = {'success': True, 'response': 'Task Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/search-test/<string:user_id>", methods=['GET'])
def search_test(user_id):
    """ recieves get requests to search for a key word """
    # data = request.glt_json()
    items = db_helper.search_test(user_id)
    result = {'success': True, 'response': 'Done'}
    

    return render_template("user_tests.html", items=items,user_id = user_id)


@app.route("/user-statistics/<string:search_string>",methods=['GET','POST'])
def user_statistics(search_string):
    """ recieves get requests to search for a key word """
    # data = request.glt_json()
    tests = db_helper.search_test(search_string)
    vaccinations = db_helper.search_vac(search_string)
    stats = db_helper.searchQ_task(search_string) 
    result = {'success': True, 'response': 'Done'}

    return render_template("user_statistics.html",items = tests, vaccinations = vaccinations,stats = stats,user_id = search_string)
