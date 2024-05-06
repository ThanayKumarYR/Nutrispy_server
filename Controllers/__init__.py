from Controllers.home import home
from Controllers.contact import contactEmail,contactFirebase,deleteContact,contact_operations
from Controllers.loginSystem import login,logout
from Controllers.food_detection import food_detection
from Controllers.diet_recommendation import diet_recommendation,recommedation
from Controllers.session import check_session
def __init__():
    return home,contactEmail,login,logout,food_detection,diet_recommendation,contactFirebase,contact_operations,deleteContact,recommedation, check_session