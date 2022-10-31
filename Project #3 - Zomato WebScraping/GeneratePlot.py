import pickle
from getData import Review
from matplotlib import pyplot as plt
import collections
import numpy as np
from sklearn.linear_model import LinearRegression

j=1
actual_ratings = []
shown_ratings = []
while j < 41:
    with open( str(j) + '.pkl', 'rb') as f:
        link, data, deliveryRating, diningRating  = pickle.load(f)
        print (link)
        average_rating_this_restaurant_list=0
        c=0
        for i in range (0, len(data)):
            if data[i].stars is not None:
                average_rating_this_restaurant_list+=data[i].stars
                c+=1
        average_rating = average_rating_this_restaurant_list/c
        actual_ratings.append(average_rating)
        shown_ratings.append(float(deliveryRating))
        j+=1
xvalues = np.linspace(0,5,num=100)
yvalues = np.linspace(0,5,num=100)


plt.scatter(xvalues,yvalues)
plt.scatter(shown_ratings,actual_ratings)
plt.gcf().set_size_inches(8, 5)
plt.title("Actual ratings vs shown rating for Zomato Restaurants")
plt.xlabel("Shown ratings")
plt.ylabel("Actual rating (average of all customer ratings)")
plt.show()


