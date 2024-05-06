from Controllers import home,login,logout,food_detection,recommedation,contactFirebase,contact_operations,deleteContact,check_session

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
    
    @app.route('/detect',methods=['GET'])
    def foodDetectionRoute():
        return food_detection()
    
    @app.route('/recommend',methods=['GET','POST'])
    def dietRecommedationRoute():
        return recommedation()
    
    @app.route('/check_session')
    def check_sessionRoute():
        return check_session()