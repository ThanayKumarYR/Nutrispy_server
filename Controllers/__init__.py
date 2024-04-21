from Controllers.home import home
from Controllers.contact import contactEmail,getContacts,contactFirebase
from Controllers.loginSystem import login,logout
from Controllers.food_detection import food_detection
from Controllers.diet_recommendation import diet_recommendation
from Controllers.exercise_recommendation import exercise_recommendation
def __init__():
    return home,contactEmail,login,logout,food_detection,diet_recommendation,exercise_recommendation,getContacts,contactFirebase