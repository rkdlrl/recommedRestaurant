import restaurant as rst
import recommender_system as rcmd

name = '전성훈'
print(name,'님을 위한 추천')

#user_based
recommed_list = rcmd.user_based_suggestions(name)
print('user_based : ',[j[0] for _, j in enumerate(recommed_list)])

#item_based
recommed_list = rcmd.item_based_suggestions(name)
print('item_based : ',[j[0] for _, j in enumerate(recommed_list)])