FROM debian:wheezy
MAINTAINER Carsten Ehbrecht <ehbrecht@dkrz.de>

# install common packages
RUN apt-get update -y
RUN apt-get install -y apt-utils
RUN apt-get install -y aptitude
RUN apt-get install -y vim
RUN apt-get install -y wget

# install ncl
RUN mkdir -p /opt/ncl
WORKDIR /opt/ncl
RUN wget --no-check-certificate -O ncl_ncarg-6.2.1.Linux_Debian7.6_x86_64_gcc472.tar.gz "https://www.earthsystemgrid.org/download/fileDownload.htm?logicalFileId=38263864-351d-11e4-a4b4-00c0f03d5b7c"
RUN tar xvfz ncl_ncarg-6.2.1.Linux_Debian7.6_x86_64_gcc472.tar.gz
ENV NCARG_ROOT /opt/ncl
ENV PATH /opt/ncl/bin:$PATH
RUN apt-get install -y gcc
RUN apt-get install -y gfortran
RUN apt-get install -y ldap-utils
RUN apt-get install -y libssh2-1
RUN apt-get install -y librtmp0
RUN apt-get install -y libfontconfig1
RUN apt-get install -y libxrender1
RUN apt-get install -y libxext6

# install esmval dependencies
RUN apt-get install -y python
RUN apt-get install -y python-nose
RUN apt-get install -y make
RUN apt-get install -y less

# setup esmval user
RUN useradd esmval

# install esmvaltool
ADD . /home/esmval/esmvaltool
#RUN make tests
RUN chown -R esmval:esmval /home/esmval

# run everyting else as esmval user
USER esmval
ENV HOME /home/esmval
WORKDIR /home/esmval/esmvaltool

# mount workspace volume
VOLUME ["/workspace"]

# run demo script
# TODO: catch output and write to log file
#ENTRYPOINT ["python", "main.py", "nml/namelist_MyDiag_generated.xml"]
#CMD python main.py nml/namelist_MyDiag_generated.xml > /workspace/log.txt
#ENTRYPOINT ["bash", "esmval.sh", "/workspace/namelist.xml", "/workspace/log.txt"]










