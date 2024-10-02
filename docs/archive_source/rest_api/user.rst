Authentication endpoints
========================

Session authentication endpoint
-------------------------------

.. code-block::
   :caption: To log in by Django REST framework html form

   /api/v1/drf-auth/login/

.. code-block::
   :caption: To log out by Django REST framework

   /api/v1/drf-auth/logout/

Token authentication endpoint
-----------------------------

.. code-block::
   :caption: Get link to user list.

   /api/v1/auth/

Obtain user authentication token
""""""""""""""""""""""""""""""""

.. code-block::
   :caption: To obtain user authentication token

   /auth/token/login/

======================= =========================== ================================
Method                  Request                     Response
======================= =========================== ================================
POST                    * username                  HTTP_200_OK
                        * password                   * auth_token
                                                    HTTP_401_Unauthorized
                                                     * detail (optional)
                                                     * non_field_errors (optional)
======================= =========================== ================================

.. code-block::
   :caption: To logout user (remove user authentication token)

   /auth/token/logout/

======================= =========================== ================================
Method                  Request                     Response
======================= =========================== ================================
POST                    --                           HTTP_204_NO_CONTENT
======================= =========================== ================================

User endpoints
==============

Create user endpoint
--------------------

.. code-block::
   :caption: To register

   /api/v1/auth/users/

======================= =========================== ================================
Method                  Request                     Response
======================= =========================== ================================
POST                    * username                  HTTP_201_CREATED
                        * password                   * email
                                                     * username
                                                     * id

                                                    HTTP_400_BAD_REQUEST
                                                     * username (optional)
                                                     * password (optional)
======================= =========================== ================================

Retrieve, delete user endpoints
-------------------------------

You need to obtain user authentication token and add it to the headers.

.. code-block:: python
   :caption: Add token to headers

   request.headers["Authorization"] = "Token <token>"

.. code-block::
   :caption: To retrieve/delete

   /api/v1/auth/users/id/

+----------------------+----------------------------+-------------------------------+
| Method               | Request                    | Response                      |
+======================+============================+===============================+
| GET                  | --                         | HTTP_200_OK                   |
|                      |                            |  * email                      |
|                      |                            |  * id                         |
|                      |                            |  * username                   |
|                      |                            | HTTP_404_Not Found            |
|                      |                            |  * detail                     |
+----------------------+----------------------------+-------------------------------+
| DELETE               | * current_password         | HTTP_204_NO_CONTENT           |
|                      |                            |                               |
|                      |                            | HTTP_400_BAD_REQUEST          |
|                      |                            |  * current_password           |
+----------------------+----------------------------+-------------------------------+

Rename user endpoint
--------------------

You need to obtain user authentication token and add it to the headers.

.. code-block::
   :caption: To rename

   /api/v1/auth/users/set_username/

+----------------------+----------------------------+-------------------------------+
| Method               | Request                    | Response                      |
+======================+============================+===============================+
| POST                 | * new_username             | HTTP_204_NO_CONTENT           |
|                      | * current_password         |                               |
|                      |                            | HTTP_400_BAD_REQUEST          |
|                      |                            |  * new_username (optional)    |
|                      |                            |  * current_password (optional)|
+----------------------+----------------------------+-------------------------------+
