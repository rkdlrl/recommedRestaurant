import restaurant as rst
import math
from collections import defaultdict, Counter
from linear_algebra import dot

def cosine_similarity(v, w):
    try:
        return dot(v, w) / math.sqrt(dot(v, v) * dot(w, w))
    except ZeroDivisionError as e:
        return dot(v, w) / 1

# get rst data 
restaurant_list = rst.get_restaurant_list();
users_list = rst.get_users_list();
user_interested_restaurant = rst.get_user_interested_restaurant();
user_visited_restaurant = rst.get_user_visited_restaurant();
#
# user-based filtering
#
def make_user_interest_vector(user_interests):
    """given a list of interests, produce a vector whose i-th element is 1
    if unique_interests[i] is in the list, 0 otherwise"""
    return [1 if interest in user_interests else 0
            for interest in restaurant_list]
user_interest_rst_matrix = list(map(make_user_interest_vector,user_interested_restaurant))

user_similarities = [[cosine_similarity(interest_vector_i, interest_vector_j)
                      for interest_vector_j in user_interest_rst_matrix]
                     for interest_vector_i in user_interest_rst_matrix]
def user_name_to_user_id(user_name):
    user_id = 0
    for i, user in enumerate(users_list):
        if user == user_name:
            user_id = i
    return user_id

def most_similar_users_to(user_id):
    pairs = [(other_user_id, similarity)                      # find other
             for other_user_id, similarity in                 # users with
                enumerate(user_similarities[user_id])         # nonzero
             if user_id != other_user_id and similarity > 0]  # similarity

    return sorted(pairs,                                      # sort them
                  key=lambda pair: pair[1],                   # most similar
                  reverse=True)                               # first

def user_based_suggestions(user_name, include_current_interests=False):
    #user_name -> user_id
    user_id = user_name_to_user_id(user_name)
    # sum up the similarities
    suggestions = defaultdict(float)
    for other_user_id, similarity in most_similar_users_to(user_id):
        for interest in user_interested_restaurant[other_user_id]:
            suggestions[interest] += similarity

    # convert them to a sorted list
    suggestions = sorted(suggestions.items(),
                         key=lambda pair: pair[1],
                         reverse=True)

    # and (maybe) exclude already-interests
    if include_current_interests:
        return suggestions
    else:
        return [(suggestion, weight)
                for suggestion, weight in suggestions
                if suggestion not in user_visited_restaurant[user_id]]
#
# Item-Based Collaborative Filtering
#
interest_user_matrix = [[user_interest_vector[j]
                         for user_interest_vector in user_interest_rst_matrix]
                        for j, _ in enumerate(restaurant_list)]

interest_similarities = [[cosine_similarity(user_vector_i, user_vector_j)
                          for user_vector_j in interest_user_matrix]
                         for user_vector_i in interest_user_matrix]

def most_similar_interests_to(interest_id):
    similarities = interest_similarities[interest_id]
    pairs = [(restaurant_list[other_interest_id], similarity)
             for other_interest_id, similarity in enumerate(similarities)
             if interest_id != other_interest_id and similarity > 0]
    return sorted(pairs,
                  key=lambda pair: pair[1],
                  reverse=True)

def item_based_suggestions(user_name, include_current_interests=False):
    #user_name -> user_id
    user_id = user_name_to_user_id(user_name)

    suggestions = defaultdict(float)
    user_interest_vector = user_interest_rst_matrix[user_id]
    for interest_id, is_interested in enumerate(user_interest_vector):
        if is_interested == 1:
            similar_interests = most_similar_interests_to(interest_id)
            for interest, similarity in similar_interests:
                suggestions[interest] += similarity

    suggestions = sorted(suggestions.items(),
                         key=lambda pair: pair[1],
                         reverse=True)

    if include_current_interests:
        return suggestions
    else:
        return [(suggestion, weight)
                for suggestion, weight in suggestions
                if suggestion not in user_visited_restaurant[user_id]]