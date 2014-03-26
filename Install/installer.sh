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
    wget "http://www.python.org/ftp/python/2.7.5/Python-2.7.5.tgz"
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

echo Dependency check...
sleep 3
./python/bin/easy_install Babel==1.3
./python/bin/easy_install js.tinymce==3.5.2_1
./python/bin/easy_install js.jqgrid==4.4.4
./python/bin/easy_install js.jquery==1.9.1
./python/bin/easy_install js.jquery_form==3.09
./python/bin/easy_install js.jquery_jgrowl==1.2.5
./python/bin/easy_install js.jquery_markitup==1.1.10_1
./python/bin/easy_install js.jqueryui==1.8.24
./python/bin/easy_install js.jquery_selectmenu==0.1
./python/bin/easy_install fanstatic==0.16
./python/bin/easy_install fa.jquery==0.9.5
./python/bin/easy_install FormAlchemy==1.4.3
./python/bin/easy_install pyramid==1.3.3
./python/bin/easy_install SQLAlchemy==0.7.8
./python/bin/easy_install transaction==1.4.1
./python/bin/easy_install pyramid_tm==0.7
./python/bin/easy_install zope.sqlalchemy==0.7.2
./python/bin/easy_install waitress==0.8.2
./python/bin/easy_install pymysql==0.5
./python/bin/easy_install pyramid_formalchemy==0.4.3
./python/bin/easy_install fa.jquery==0.9.5
./python/bin/easy_install fanstatic==0.16
./python/bin/easy_install pyramid_mailer==0.11
./python/bin/easy_install pisa==3.0.33
./python/bin/easy_install reportlab==2.7
./python/bin/easy_install html5lib==0.95
./python/bin/easy_install requests==1.2.0
./python/bin/easy_install pyPDF==1.11
./python/bin/easy_install pyramid_fanstatic==0.4
./python/bin/easy_install pyramid_rewrite==0.2

# Move D2L Patched Egg.
cp ./Install/D2LValence-0.1.14-py2.7.egg.tar python/lib/python2.7/site-packages/
cd python/lib/python2.7/site-packages/
rm -rf D2LValence-0.1.14-py2.7.egg
tar -xvf D2LValence-0.1.14-py2.7.egg.tar
rm D2LValence-0.1.14-py2.7.egg.tar

# Rebuild Egg
sleep 1
cd $APPDIR
pwd
cd QuizSmith
../python/bin/python setup.py develop



echo Finished!
sleep 1

echo Note: It is okay to rerun this installer.

