from controller import app
from flask_cors import CORS
# Enable CORS for your app, which can be customized with parameters
CORS(app)
if __name__ == '__main__':
    app.run(debug=True)
