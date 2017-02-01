Using Docker for ESMValTool
***************************

To build a docker image run::

   $ docker build -t esmvaltool .

Run docker container::

   $ docker run -i -t esmvaltool /bin/bash

Edit the Dockerfile if you want to change the docker build::

   $ vim Dockerfile

Links:

* https://www.docker.com/ 
* http://docs.docker.com/reference/builder/

 
