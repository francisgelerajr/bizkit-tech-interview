from flask import Blueprint, request
from .data.search_data import USERS

bp = Blueprint("search", __name__, url_prefix="/search")

@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200

def search_users(args):
    """
    Search users database based on provided parameters.

    Parameters:
        args (dict): Dictionary containing search parameters:
            id (str): Unique identifier for user.
            name (str): Name of the user, partially matched, case insensitive.
            age (str): Age of the user, matched within a range of ±1 year.
            occupation (str): Occupation of the user, partially matched, case insensitive.

    Returns:
        list: A list of users that match the search parameters, sorted by match priority.
              If no parameters are provided, returns all users.
    """
    search_id = args.get('id')
    search_name = args.get('name', '').lower()
    search_age = args.get('age')
    search_occupation = args.get('occupation', '').lower()

    results = []

    # helper function to add a user to the result list with priority (added for bonus :D)
    def add_user(user, priority):
        user_tuple = (tuple(user.items()), priority)
        if user_tuple not in results:
            results.append(user_tuple)

    # return all users if there are no parameters 
    if not any([search_id, search_name, search_age, search_occupation]):
        for user in USERS:
            add_user(user, 0)  # give priority 0 for no search parameters
        return [dict(user) for user, priority in results]

    for user in USERS:
        if search_id and user['id'] == search_id:
            add_user(user, 1)
            continue  # skip to the next user if the ID matches
        matched = False
        if search_name and search_name in user['name'].lower():
            add_user(user, 2)
            matched = True
        if search_age:
            try:
                age = int(search_age)
                if age - 1 <= int(user['age']) <= age + 1:
                    add_user(user, 3)
                    matched = True
            except ValueError:
                continue  # skip to the next user if the age is not an int
        if search_occupation and search_occupation in user['occupation'].lower():
            add_user(user, 4)
            matched = True


    # if no users are found, return an error message
    if not results:
        return {'error': 'User not found'}

    # sort results by priority
    results.sort(key=lambda x: x[1])

    # return result as list of dictionaries
    return [dict(user) for user, priority in results]