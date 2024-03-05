# --------------------  Imports  --------------------

from application import create_app
from application.globals import HOST, PORT, DEBUG, ENV_TYPE

# --------------------  Initialization  --------------------

app = create_app(env_type=ENV_TYPE)

# --------------------  Main  --------------------
if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)

# --------------------  End  --------------------