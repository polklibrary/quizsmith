#!/bin/sh
# Install python and dependencies

# REGISTRATION
echo "Please enter your email: "
read input_variable
if [ "$input_variable" = "" ]; then
  echo "No email, skipping..."
else
  echo "Email set [$input_variable]"
  wget -q "http://www.uwosh.edu/library/quizsmith/support/installer-registration?email=$input_variable&form.submitted=1" -O remove_me
  rm remove_me
fi

# RUN INSTALLER BELOW
cd ../

APPDIR=$(pwd)

if [ -d "/usr/include/openssl" ]; then
    echo OpenSSL Found!
else
    echo You will need to install OpenSSL: apt-get install libssl-dev
    echo Please see solution at
    echo http://www.uwosh.edu/library/quizsmith/support
    exit
fi

if [ -d "python" ]; then
    echo Python already installed... skipping ahead...
else
    echo Installing Python
    sleep 5
    wget "https://www.python.org/ftp/python/2.7.5/Python-2.7.5.tgz" --no-check-certificate
    tar -xvf Python-2.7.5.tgz
    mkdir python
    cd python
    BASEDIR=$(pwd)
    cd ../Python-2.7.5
    echo $BASEDIR
    ./configure --prefix=$BASEDIR
    make
    make install
    sleep 3
    cd ../
    echo Currently...
    pwd
    echo Cleaning up python installer dependencies
    rm -rf Python-2.7.5
    rm Python-2.7.5.tgz
    echo Python Installed!
    echo Preparing application dependencies
    sleep 5
fi

if [ -f "./python/bin/easy_install" ]; then
    echo EasyInstaller already setup
else
    echo Setting up easy installer
    wget "http://peak.telecommunity.com/dist/ez_setup.py"
    sleep 3
    ./python/bin/python ez_setup.py
    sleep 3
    rm ez_setup.py
fi

sleep 3
echo Moving patched eggs...
cp ./Install/D2LValence-0.1.14-py2.7.egg.tar python/lib/python2.7/site-packages/
cd python/lib/python2.7/site-packages/
rm -rf D2LValence-0.1.14-py2.7.egg
tar -xvf D2LValence-0.1.14-py2.7.egg.tar
rm D2LValence-0.1.14-py2.7.egg.tar

# Build Egg and Get Dependencies
sleep 1
cd $APPDIR
pwd
cd QuizSmith
../python/bin/python setup.py develop

echo Finished!
sleep 1

echo Note: It is okay to rerun this installer.
