import pickle
import matplotlib.pyplot as plt

dbfile = open('LOG', 'rb')      
db = pickle.load(dbfile) 

fig, axs = plt.subplots(5, sharex=True, figsize=(12,6))
fig.suptitle('Evolution of animal stats with time')

axs[0].plot(db['Speed'])
axs[0].set_ylabel('Speed')
axs[1].plot(db['EnergyCapacity'])
axs[1].set_ylabel('Energy Capacity')
axs[2].plot(db['Sight'])
axs[2].set_ylabel('Sight')
axs[3].plot(db['Number of Animals'])
axs[3].set_ylabel('Number of \nAnimals')
axs[4].plot(db['Number of Plants'])
axs[4].set_ylabel('Number of \nPlants')

plt.show()

dbfile.close()


