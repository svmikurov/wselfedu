.. _run_stop_app:

Run and stop application
------------------------

Run application::

    make up

Stop application::

    make down

Docker console commands
-----------------------

See
`all docker compose <https://docs.docker.com/reference/>`_ commands.

Docker system info
^^^^^^^^^^^^^^^^^^

To display information regarding the amount of disk space used by the
Docker daemon
(`source <https://docs.docker.com/reference/cli/docker/system/df/>`_)::

    docker system df

stdout::

    TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
    Images          4         3         4.083GB   425.4MB (10%)
    Containers      3         3         364.9kB   0B (0%)
    Local Volumes   0         0         0B        0B
    Build Cache     95        0         187.5MB   187.5MB

Images
^^^^^^

List of all images::

    docker image ls

or::

    docker images

Remove image
(`docker compose rm <https://docs.docker.com/reference/cli/docker/compose/rm/>`_)::

    docker compose rm [OPTIONS] [SERVICE...]

Remove all dangling images. If -a is specified, also remove all images
not referenced by any container
(`docker image prune <https://docs.docker.com/reference/cli/docker/image/prune/>`_).::

    docker image prune -a

or::

    docker rmi -f $(docker images -aq)

Containers
^^^^^^^^^^

List of all containers::

    docker ps -a

Stop container
(`docker container stop <https://docs.docker.com/reference/cli/docker/container/stop/>`_)::

    docker container stop [OPTIONS] CONTAINER [CONTAINER...]

Remove container
(`docker container rm <https://docs.docker.com/reference/cli/docker/container/rm/>`_)::

    docker container rm [OPTIONS] CONTAINER [CONTAINER...]

Removes all stopped containers
(`docker container prune <https://docs.docker.com/reference/cli/docker/container/prune/>`_)::

    docker container prune

To delete all containers including its volumes use::

    docker rm -vf $(docker ps -aq)

Local Volumes
^^^^^^^^^^^^^

Build Cache
^^^^^^^^^^^

Remove build cache
(`docker builder prune <https://docs.docker.com/reference/cli/docker/builder/prune/>`_)::

    docker builder prune
