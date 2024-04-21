from Controllers import home,contactEmail

def routing(app):
    @app.route('/',methods=['GET'])
    def homeRoute():
        return home()

    @app.route('/contact',methods=['GET','POST'])
    def contactRoute():
        return contactEmail()

    