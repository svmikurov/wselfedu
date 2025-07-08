API
===

Authentication with JWT
-----------------------

Request token pair
^^^^^^^^^^^^^^^^^^

POST /api/token/

{'username': ..., 'password': ...}

Response:
.........

{"refresh": "eyJhbG...", "access": "eyJhbG..."}

Request with "access" token
^^^^^^^^^^^^^^^^^^^^^^^^^^^

GET /.../

Headers: "Authorization: Bearer eyJhbG..."

Refresh "access" token with "refresh" token
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

POST /api/token/refresh/

{"refresh": "eyJhbG..."}'

Response:
.........

{"access": "eyJhbG..."}
