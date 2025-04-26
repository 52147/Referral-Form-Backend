from controller import app
from flask_cors import CORS
import os

CORS(app)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # 加這一行！
    app.run(host='0.0.0.0', port=port, debug=True)
