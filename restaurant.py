import csv
import math
#open, read csv
with open('./gachon.csv', 'r') as csvfile:
    matrix = [] 
    reader = csv.DictReader(csvfile)
    for row in reader:
        ke = list(row.keys())
        #평균값 입력
        mean = float(row[ke[2]])**2 + float(row[ke[3]])**2 + float(row[ke[4]])**2
        row['mean'] = math.sqrt(mean)
        matrix.append(row)

restaurant_list = sorted(list({row[ke[1]] for row in matrix}))
users_list = sorted(list({row[ke[0]] for row in matrix}))

'''
    유저가 준 식당별 평점 평균을 내고
    평균이 2.5 이상인 레스토랑을 1, 아닌경우 0
'''
#유저가 평균 2.5이상 평점을 준 음식점 리스트 만들기
def make_user_interested_restaurant():
    rst_intrest_line = math.sqrt(75)/2
    return [sorted([row['업소명'] for row in matrix 
            if(row['mean']>=rst_intrest_line and user == row['이름'])])
            for user in users_list]

#유저가 방문한(별점을 준) 음식점 리스트 만들기
def make_user_visited_restaurant():
    return [sorted([row['업소명'] for row in matrix 
            if(user == row['이름'])])
            for user in users_list]

user_interested_restaurant = make_user_interested_restaurant()
user_visited_restaurant = make_user_visited_restaurant()

def get_restaurant_list():
    return restaurant_list

def get_users_list():
    return users_list

def get_user_interested_restaurant():
    return user_interested_restaurant

def get_user_visited_restaurant():
    return user_visited_restaurant

if __name__ == "__main__":
    #print data
    for user in user_interest:
        print(user)
    print('\n', restaurant_list)
    print(users_list)