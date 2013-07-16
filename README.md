idservice
=========
A Django application for the creation of unique identifiers for library collections and items.
This was created as a replacement of the NOID software.
This application can mint new identifiers, bind urls and descriptions to them, and supports a lookup call as well.


Installation Instructions
-------------------------
This software should be runnable on any kind of operating system. However, these installation instructions are tailored to a Linux server, and have only been tested on ubuntu 10.04 LTS.

**Part I - Basic server requirements**

1. Install Apache if not already installed. Also install the WSGI module if not already installed

        sudo apt-get install apache2

        sudo apt-get install libapache2-mod-wsgi

2. Install git if not already installed

    	sudo apt-get install git-core

3. Install MySQL and build dependency libraries for Python

        sudo apt-get install mysql-server libmysqlclient-dev 

    Create root account when prompted


- - -

**Part II - Setting up the project environment**

4. Install virtualenv

        sudo apt-get install python-setuptools python-dev

        sudo easy_install virtualenv

5. Create directory for your projects (replace <user> with your user name)

        mkdir /home/<user>/Projects/

        cd /home/<user>/Projects/

6. Pull down the project from github

        git clone git@github.com:gwu-libraries/idservice.git

7. Create virtual Python environment for the project

        cd /home/<user>/Projects/idservice
        
        virtualenv --no-site-packages ENV

8. Activate your virtual environment

        source ENV/bin/activate

9. Install django, mysqldb, arkpy, pytz

        pip install -r requirements.txt

10. create a logs folder 

        mkdir /home/<user>/Projects/idservice/lids/lids/logs


- - -

**Part III - Configuring your installation**

10. Log in to MySQL and create the idservice user and database. Make up a user name and password.

        mysql -u root -p

        CREATE DATABASE idservice;

        CREATE USER <django user name>@localhost IDENTIFIED BY '<django password>';

        GRANT ALL ON idservice.* TO <django user name>@'localhost';
    
        FLUSH PRIVILEGES;

        exit

11. Edit wsgi file

        mv /home/<user/Projects/idservice/lids/lids/wsgi.py.template /home/<user/Projects/idservice/lids/lids/wsgi.py
        vim /home/<user/Projects/idservice/lids/lids/wsgi.py

    Change parameter for site.addsitedir() to your local path. You will need to change the user name and possibly the Python version number.

12. Configure database and other settings in a local_settings file

        cd lids/lids

        mv local_settings.py.template local_settings.py

        vim local_settings.py

    Change database login and password and any other parameters you wish to change.

13. Edit Apache config file

        vim /home/<user>/Projects/idservice/apache/id

    Change the values of the server, user, and python version in the document

14. Add apache config file to sites-enabled and enable it

        sudo mv /home/<user>/Projects/idservice/apache/id /etc/apache2/sites-available/id

        sudo a2dissite default

        sudo a2ensite id

        sudo /etc/init.d/apache2 restart

15. Let Django create the database tables for you

        cd ..

        python manage.py syncdb

16. Create primary minters and requesters in the DB

        python manage.py dbshell

        INSERT INTO lidapp_minter SET name='<name>', authority_number='<your NMA#>', prefix='<optional prefix>', template='<your template>', minter_type='<types of IDs to mint>', date_created=NOW(), description='<optional>';

        INSERT INTO lidapp_requester SET name='<name>', organization='<your org>', date_created=NOW(), description='<optional>', 'ip'=<ip of requester>;
- - -

**Part IV - Testing**

Your system should now run. 

17. You may want to restart Apache just in case. 

        sudo /etc/init.d/apache2 restart

18. Test the minting function

        http://<your domain name>/mint/<minter name>/<quantity of ids to mint>?requester=<your requester name>

19. Test the binding function

        http://<your domain name>/bind/<identifier>?object_url=<url to bind>&object_type=<choice of i or c>&description=<optional text field>

    For object type, there are currently only two types: i for Item and c for Collection. You can add to these by editing the local_settings.py file

20. Test the lookup function

        http://<your domain name>/lookup/<identifier>
