import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import pickle

# Load player data
data = pd.read_csv("/content/player_attributes.csv")

# Define relevant columns using 
player_features = ['potential', 'crossing', 'finishing', 'heading_accuracy', 'short_passing', 'volleys', 'dribbling', 'curve', 'free_kick_accuracy', 'long_passing', 'ball_control', 'acceleration', 'sprint_speed', 'agility', 'reactions', 'balance', 'shot_power', 'jumping', 'stamina', 'strength', 'long_shots', 'aggression', 'interceptions', 'positioning', 'vision', 'penalties', 'marking', 'standing_tackle', 'sliding_tackle']
target = 'overall_rating'

# Extract features and target variable
X = data[player_features].copy()
y = data[target].copy()

# Clean the data by removing rows with missing values
X.dropna(inplace=True)
y = y.loc[X.index]

# Perform data scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Initialize RandomForestRegressor and fit the model
clf = RandomForestRegressor(random_state=42)
clf.fit(X_train, y_train)

# Evaluate the model on the testing set
score = clf.score(X_test, y_test)

#print("R-Squared Score:", score)

# Save the trained model to disk
pickle.dump(clf, open('model.pkl', 'wb'))
