#!/bin/env bash
#
# Wrapper to run Condor glidein (master + startd)
# Configured via args 
#
# Author: John Hover <jhover@bnl.gov>
#
WRAPPER_VERSION=0.9.0
CONDOR_VERSION=8.0.6
ARCH=x86_64
PLATFORM=RedHat6
TARBALL_NAME=condor-${CONDOR_VERSION}-${ARCH}_${PLATFORM}-stripped.tar.gz
TARBALL_URL=http://dev.racf.bnl.gov/dist/condor/$CONDOR_VERSION/rhel6/$ARCH/$TARBALL_NAME
CONDOR_DIR=~/condor
CONFIG=~/condor/etc/condor_config
DEFAULT_COLLECTOR=gridtest05.racf.bnl.gov
DEFAULT_COLLECTOR_PORT=29618

usage()
{
cat << EOF
usage: $0 [options]

Run glidein against given collector:port and auth. 

OPTIONS:
 -h     
 -c      Collector name
 -p      Collector port
 -v      Verbose
EOF
}

get_args() {

	COLLECTOR=
	PORT=
	AUTH=
	
	while getopts “ht:r:p:v” OPTION
	do
	     case $OPTION in
	         h)
	             usage
	             exit 1
	             ;;
	         t)
	             TEST=$OPTARG
	             ;;
	         r)
	             SERVER=$OPTARG
	             ;;
	         p)
	             PASSWD=$OPTARG
	             ;;
	         v)
	             VERBOSE=1
	             ;;
	         ?)
	             usage
	             exit
	             ;;
	     esac
	done

}


print_header() {
	echo "condor_glidein version $WRAPPER_VERSION"
	HOST=`hostname -f`
	DATE=`date -u +"%Y-%m-%d %H:%M:%SUTC"`
	echo "running on $HOST $DATE" 
}

setup_dir() {
	cd 
	WD=`pwd`
	echo "working dir is $WD"
	echo "creating Condor dir"
	mkdir -p $CONDOR_DIR
	cd $CONDOR_DIR

}

handle_tarball() {
	echo "retrieving tarball from $TARBALL_URL"
	wget $TARBALL_URL
	echo "unpacking tarball..."
	tar --verbose --extract --gzip --strip-components=1  --file=$TARBALL_NAME

}

install_condor() {
echo "running condor_install..."
./condor_install --type=execute
export CONDOR_CONFIG=$CONDOR_DIR/etc/condor_config

}

configure_condor() {
 echo "adding COLLECTOR_HOST=$DEFAULT_COLLECTOR:$DEFAULT_COLLECTOR_PORT to config"
 echo COLLECTOR_HOST=$DEFAULT_COLLECTOR:$DEFAULT_COLLECTOR_PORT >> $CONFIG

}

f_exit(){
        if [ "$1" == "" ]; then
                RETVAL=0
        else
                RETVAL=$1
        fi
        echo "exiting with RC = $RETVAL"
        exit $RETVAL
}

get_args
print_header
setup_dir
rc=$?
if [ $rc -ne 0 ]; then
        f_exit $rc
fi

handle_tarball
rc=$?
if [ $rc -ne 0 ]; then
        f_exit $rc
fi

install_condor
rc=$?
if [ $rc -ne 0 ]; then
        f_exit $rc
fi

configure_condor
rc=$?
if [ $rc -ne 0 ]; then
        f_exit $rc
fi
