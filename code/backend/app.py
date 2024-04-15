# --------------------  Imports  --------------------

from application import create_app
from application.globals import HOST, PORT, DEBUG, ENV_TYPE
from celery_worker import celery_init_app

# --------------------  Initialization  --------------------

app = create_app(env_type=ENV_TYPE)

celery_app = celery_init_app(app)


# --------------------  Main  --------------------
if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)


# --------------------  End  --------------------