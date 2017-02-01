#! /bin/bash

function usage {
    echo "Usage: esmval.sh namelist.xml logfile.txt"
}

esmval_root=`dirname $0`

if [ $# -ne 2 ]; then
    usage
    exit 1
fi

#NCARG_ROOT="/opt/ncl"
#export NCARG_ROOT
#PATH="$NCARG_ROOT/bin:$PATH"
#export PATH

cd "$esmval_root"
#which ncl 2>&1 | tee $2
#ncl -V 2>&1 | tee $2
python main.py $1 2>&1 | tee $2
cd -
