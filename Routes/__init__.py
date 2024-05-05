from Controllers import home,login,logout,food_detection,diet_recommendation,exercise_recommendation,contactFirebase,contact_operations,deleteContact

def routing(app):
    @app.route('/',methods=['GET'])
    def homeRoute():
        return home()

    @app.route('/contact',methods=['POST'])
    def contactRoute():
        return contactFirebase()
    
    @app.route('/contact', methods=['GET','DELETE'])
    def contact_operationsRoute():
        return contact_operations()
    
    @app.route('/contact/<contact_id>', methods=['DELETE'])
    def deleteContactRoute(contact_id):
        return deleteContact(contact_id)

    @app.route('/login',methods=['POST'])
    def loginRoute():
        return login()
    
    @app.route('/logout',methods=['GET'])
    def logoutRoute():
        return logout()
    
    @app.route('/foodDetection',methods=['GET'])
    def foodDetectionRoute():
        return food_detection()
    
    @app.route('/dietRecommedation',methods=['GET'])
    def dietRecommedationRoute():
        return diet_recommendation()
    
    @app.route('/exerciseRecommendation',methods=['GET'])
    def exerciseRecommendationRoute():
        return exercise_recommendation()

    