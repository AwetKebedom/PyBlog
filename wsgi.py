#################################################
#######                                   #######
#######             MAIN.PY               #######
#######                                   ####### 
#################################################


from pyblog import models, forms, routes
from pyblog import app, db

@app.shell_context_processor
def shell_context():
    return {
        'models': models,
        'app': app,
        'db': db,
        'forms': forms,
        'routes': routes,
        'myname':'eyal'
    }

if __name__ == "__main__":
    app.run()
