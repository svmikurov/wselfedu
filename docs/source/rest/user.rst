Authentication endpoints
========================

Obtain user authentication token
--------------------------------

.. code-block::
   :caption: To obtain user authentication token

   /auth/token/login/

+-----------+-----------------------------+---------------------------------+
| Method    | Request                     | Response                        |
+===========+=============================+=================================+
| POST      | * username                  | HTTP_200_OK                     |
|           | * password                  |  * auth_token                   |
|           |                             |                                 |
|           |                             | HTTP_401_Unauthorized           |
|           |                             |  * detail (optional)            |
|           |                             |  * non_field_errors (optional)  |
+-----------+-----------------------------+---------------------------------+

.. code-block::
   :caption: To logout user (remove user authentication token)

   /auth/token/logout/

+-----------+-----------------------------+---------------------------------+
| Method    | Request                     | Response                        |
+===========+=============================+=================================+
| POST      | --                          | HTTP_204_NO_CONTENT             |
+-----------+-----------------------------+---------------------------------+

.. code-block::
   :caption: To retrieve user data.

   /api/v1/auth/users/me/

+-----------+-----------------------------+---------------------------------+
| Method    | Request                     | Response                        |
+===========+=============================+=================================+
| POST      | --                          | HTTP_200_OK                     |
|           |                             |  * email                        |
|           |                             |  * id                           |
|           |                             |  * username                     |
|           |                             |                                 |
|           |                             | HTTP_401_Unauthorized           |
|           |                             |  * detail                       |
+-----------+-----------------------------+---------------------------------+
