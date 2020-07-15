import pandas as pd

data = pd.read_csv('RatingsInput.csv')
user_data=pd.read_csv('NewUsers.csv')

new_movie_data=data.copy()
#--------------Task 1--------------
# Split the moviename by comma
new_movie_data['MovieName'] = new_movie_data['MovieName'].str.split(',')
# Extra the movie id 
new_movie_data['MovieID'] = new_movie_data['MovieName'].apply(lambda x: x[0])
# Extract MovieName
new_movie_data['MovieName'] = new_movie_data['MovieName'].apply(lambda x: x[1])
# Task1 required file
new_movie_data.to_csv('Task1-MovieCleanData.csv')

#--------------Task 2--------------
new_movie_data2 = new_movie_data.copy()
new_movie_data2['MovieName'] = new_movie_data2['MovieName'].apply(lambda x : x.title())

#--------------Task 3--------------
new_movie_data3 = new_movie_data2[['UserAge','MovieName','Rating']]
# Group the data based on the UserAge
new_movie_data3.groupby('UserAge')
# Sorting the data based on Rating on descending order
new_movie_data3 = new_movie_data3.sort_values(by=['Rating'], ascending = False)
# Create the dictionary 
total_list = []
for user_name, user in new_movie_data3.groupby('UserAge'):
    lst = {movie['Rating']: movie['MovieName'] for _, movie in user.iterrows()}
    total_list.append({user_name: lst})

#--------------Task 4--------------
# Get the keys from dictionary
def getList(dict): 
    list = [] 
    for key in dict.keys(): 
        list.append(key) 
    return list

age_list = []
def movies(user_age, movie_num):
    # Extract the user_age in the map above
    for i in total_list:
        age_list.append(getList(i))
    # Find the closest num in the list
    user_age = min(age_list, key=lambda x:abs(x[0]-user_age))
    # Find the movies based on the conditions
    for i in total_list:
        if user_age[0] in i:
            out = dict(list(i[user_age[0]].items())[0: movie_num])
            return str(out.values())

#--------------Task 5--------------
new_user_data = user_data.copy()
#----------Function Application----------
user_age_list = []
movie_nums = []
for i in new_user_data['UserAge']:
    user_age_list.append(i)
for j in new_user_data['NoOfMoviesToRecommend']:
    movie_nums.append(j)

actual_movies = []
for i in range(len(user_age_list)):
    x = movies(user_age_list[i], movie_nums[i])
    actual_movies.append(x)

new_user_data['Movies'] = actual_movies
# Adjust data to required format
new_user_data['Movies'] = new_user_data['Movies'].apply(lambda x:x.replace('dict_values',''))
new_user_data['Movies'] = new_user_data['Movies'].apply(lambda x:x.replace('[','').replace(']','').replace('(','').replace(')','').replace("'",'').replace('"',''))
new_user_data.to_csv('Task5-TargetMovies.csv')