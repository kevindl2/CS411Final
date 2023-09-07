import pandas as pd
import random
import names
import datetime

VACCINE_BRANDS = ['Moderna', 'Pfizer', 'Johnson & Johnson']
start_date = datetime.date(2020, 3, 1)
end_date = datetime.date.today()
date_delta = end_date - start_date

# From https://stackoverflow.com/questions/26226801/making-random-phone-number-xxx-xxx-xxxx
def gen_phone_number():
    n = '0000000000'
    while '9' in n[3:6] or n[3:6]=='000' or n[6]==n[7]==n[8]==n[9]:
        n = str(random.randint(10**9, 10**10-1))
    return n[:3] + '-' + n[3:6] + '-' + n[6:]


def create_users(num_users):
    data = {'user_id': [], 'password_hash': [], 'email': [], 'first_name': [], 'last_name': [], 'phone_number': []}
    
    dup_num = 1

    for user in range(num_users):

        first_name = names.get_first_name()
        last_name = names.get_last_name()
        user_id = first_name + last_name

        if (user_id in data['user_id']):
            user_id = user_id + str(dup_num)
            data['user_id'].append(user_id)
            dup_num += 1
        else:
            data['user_id'].append(user_id)

        data['password_hash'].append('')
        data['email'].append(user_id + "@fakeemail.com")
        data['first_name'].append(first_name)
        data['last_name'].append(last_name)
        data['phone_number'].append(gen_phone_number())
    
    df = pd.DataFrame(data)
    df.to_csv('Generated_Data/users.csv', index=False)
    return data


def create_bubbles(num_bubbles):
    data = {'bubble_id': [], 'bubble_name': [], 'description': []}

    for bubble in range(num_bubbles):
        data['bubble_id'].append(bubble)
        data['bubble_name'].append('Bubble ' + str(bubble))
        data['description'].append('This is bubble ' + str(bubble))

    df = pd.DataFrame(data)
    df.to_csv('Generated_Data/bubbles.csv', index=False)
    return data


def create_bubble_assignments(users_data, bubbles_data, lower_bound, upper_bound):
    data = {'user_id': [], 'bubble_id': []}

    for user in users_data['user_id']:
        num_bubbles = random.randint(lower_bound, upper_bound)
        user_bubbles = []
        for bubble in range(num_bubbles):
            bubble_index = random.randint(0, len(bubbles_data['bubble_id']) - 1)  
            while bubble_index in user_bubbles:
                bubble_index = random.randint(0, len(bubbles_data['bubble_id']) - 1)               
            data['user_id'].append(user)
            data['bubble_id'].append(bubbles_data['bubble_id'][bubble_index])
            user_bubbles.append(bubble_index)

    df = pd.DataFrame(data)
    df.to_csv('Generated_Data/contains.csv', index=False)
    return data


def create_test_results(users_data, lower_bound, upper_bound):
    data = {'test_id': [], 'result': [], 'test_date': [], 'user_id': []}
    current_test_id = 0

    for user in users_data['user_id']:
        num_tests = random.randint(lower_bound, upper_bound)
        had_covid = 0
        current_date = start_date + datetime.timedelta(days=random.randrange(date_delta.days))
        for test in range(num_tests):
            covid_chance = random.randint(0, 100)
            if had_covid == 0 and covid_chance == 100:
                had_covid = 1
                has_covid = 1
            else:
                has_covid = 0
            data['test_id'].append(current_test_id)
            data['result'].append(has_covid)
            data['test_date'].append(current_date)
            data['user_id'].append(user)
            current_test_id += 1
            current_date = current_date + datetime.timedelta(days=random.randint(0, 25))
            if current_date > end_date:
                break

    df = pd.DataFrame(data)
    df.to_csv('Generated_Data/test_results.csv', index=False)
    return data


def create_vaccinations(users_data, lower_bound, upper_bound):
    data = {'vac_id': [], 'user_id': [], 'vaccine_brand': [], 'vaccine_date': []}
    current_vaccine_id = 0

    for user in users_data['user_id']:
        num_vaccines = random.randint(lower_bound, upper_bound)
        vaccine_brand_index = random.randint(0, len(VACCINE_BRANDS) - 1)
        vaccine_date = start_date + datetime.timedelta(days=random.randrange(date_delta.days))
        for vaccine in range(num_vaccines):
            data['vac_id'].append(current_vaccine_id)
            data['user_id'].append(user)
            data['vaccine_brand'].append(VACCINE_BRANDS[vaccine_brand_index])
            data['vaccine_date'].append(str(vaccine_date))
            current_vaccine_id += 1
            vaccine_date = vaccine_date + datetime.timedelta(weeks=3)
            if vaccine_date > end_date:
                break

    df = pd.DataFrame(data)
    df.to_csv('Generated_Data/vaccinations.csv', index=False)
    return data


def get_num_users_in_bubble(bubble_assignments_data, bubble_id):
    num_users = 0
    for id in bubble_assignments_data['bubble_id']:
        if id == bubble_id:
            num_users += 1
    return num_users


def create_interactions(users_data, bubbles_data, bubble_assignments_data, lower_bound, upper_bound):
    data = {'interaction_id': [], 'interaction_date': [], 'location': [], 'notes': [], 'bubble_id': []}
    current_interaction_id = 0

    for bubble in bubbles_data['bubble_id']:
        if (get_num_users_in_bubble(bubble_assignments_data, bubble) < 2):
            continue
        num_interactions = random.randint(lower_bound, upper_bound)
        interaction_date = start_date + datetime.timedelta(days=random.randrange(date_delta.days))
        for interaction in range(num_interactions):
            data['interaction_id'].append(current_interaction_id)
            data['interaction_date'].append(str(interaction_date))
            data['location'].append("Location" + str(random.randint(0, 50)))
            data['notes'].append("These are some notes for interaction " + str(current_interaction_id))
            data['bubble_id'].append(bubble)
            current_interaction_id += 1
            interaction_date = interaction_date + datetime.timedelta(days=random.randint(0, 25))
            if interaction_date > end_date:
                break

    df = pd.DataFrame(data)
    df.to_csv('Generated_Data/interactions.csv', index=False)
    return data


def get_users_in_bubble(bubble_assignments_data, bubble_id):
    users = []
    for index in range(len(bubble_assignments_data['bubble_id'])):
        if bubble_assignments_data['bubble_id'][index] == bubble_id:
            users.append(bubble_assignments_data['user_id'][index])
    return users


def create_interaction_participants(interactions_data, users_data, bubble_assignments_data, lower_bound, upper_bound):
    data = {'user_id': [], 'interaction_id': []}

    for index in range(len(interactions_data['interaction_id'])):
        interaction = interactions_data['interaction_id'][index]
        possible_participants = get_users_in_bubble(bubble_assignments_data, interactions_data['bubble_id'][index])
        num_participants = random.randint(lower_bound, min(upper_bound, len(possible_participants)))
        for participant in range(num_participants):
            user_id = random.randint(0, len(users_data['user_id']) - 1)
            data['user_id'].append(user_id)
            data['interaction_id'].append(interaction)

    df = pd.DataFrame(data)
    df.to_csv('Generated_Data/participates.csv', index=False)
    return data


def main():
    # Create 1000 users
    users_data = create_users(1000)
    # Create 250 bubbles
    bubbles_data = create_bubbles(250)
    # Create between 0 and 5 random bubble assignments for each user
    bubble_assignments_data = create_bubble_assignments(users_data, bubbles_data, 0, 5)
    # Create between 0 and 25 test results for each user
    create_test_results(users_data, 0, 25)
    # Create between 0 and 2 vaccinations for each user
    create_vaccinations(users_data, 0, 2)
    # Create between 0 and 10 interactions for each bubble
    interactions_data = create_interactions(users_data, bubbles_data, bubble_assignments_data, 0, 10)
    # Create between 2 and 10 participants for each interaction
    create_interaction_participants(interactions_data, users_data, bubble_assignments_data, 2, 10)


if __name__ == '__main__':
    main()
