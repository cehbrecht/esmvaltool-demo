ESMValWPS: ESMValTool Web Processing Services
=============================================

ESMValWPS provides the ESMValTool as Web Processing Service.

Installation
************

The installation is done with `Buildout <http://www.buildout.org/>`_.
It is using the Python distribution system `Anaconda <http://www.continuum.io/>`_ to maintain software dependencies.

If Anaconda is not available then a minimal Anaconda will be installed during the installation processes in your home directory ``~/anaconda``.

The installation process setups a conda environment named ``wps``. All additional packages and configuration files are going into this conda environment.
The location is ``~/.conda/envs/wps``.

Now, check out the code from the ESMValTool subversion repo and start the installation::

   $ svn co https://svn.dlr.de/ESM-Diagnostic/source/branches/carsten_dev/
   $ cd wps
   $ make clean install

After successful installation you need to start the services. All installed files (config etc ...) are by default in your home directory ``~/birdhouse``. Now, start the services::

   $ make start  # starts supervisor services
   $ make status # shows supervisor status

The depolyed WPS service is available on http://localhost:8095/wps?service=WPS&version=1.0.0&request=GetCapabilities.

Check the log files for errors::

   $ cd ~/birdhouse
   $ tail -f  var/log/pywps/esmvalwps.log
   $ tail -f  var/log/supervisor/esmvalwps.log

For other install options run ``make help`` and read the documention for the `Makefile <http://birdhousebuilderbootstrap.readthedocs.org/en/latest/>`_.


Configuration
*************

If you want to run on a different hostname or port then change the default values in ``custom.cfg``::

   $ cd wps
   $ vim custom.cfg
   $ cat custom.cfg
   [settings]
   hostname = localhost
   http-port = 8095


The demo service uses the ncl package (version 6.3.0) from conda. If you want to use a different ncl then edit the ``../esmval.sh`` script.

The path to ESGF archive is configured in ``../nml/to_be/checked/esgf_config.xml``.

After any change to your ``custom.cfg`` you **need** to run ``make install`` again and restart the ``supervisor`` service::

  $ make install
  $ make restart
  $ make status


Further Readings
****************

Using the Phoenix web-client for WPS:
http://pyramid-phoenix.readthedocs.org/en/latest/

Trying the Emu Web Processing Service:
http://emu.readthedocs.org/en/latest/

Birdhouse: Web Processing Services to support data processing in the climate science community:
http://bird-house.github.io/
