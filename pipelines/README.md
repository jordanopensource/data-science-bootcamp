# JOSA Session

This repo will help you get started with our session using docker 1.7 +  

### Pre-sessions

   1. Install git

	```sh
	sudo apt-get install git
	```
   2. Clone this repository

	```sh
	git clone https://github.com/jordanopensource/data-science-bootcamp.git
	```

### Installation for Session 1

1. Install java for Pentaho

	```sh
	sudo apt-get install default-jre openjdk-7-jre default-jdk openjdk-7-jdk
	```

2. Install mongo
	```sh
	sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
	
	echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
	
	sudo apt-get update
	
	sudo apt-get install -y mongodb-org
	```

	* If you are facing some warnings (transparent_hugepage/defrag warning), do the following:
	
		* Open /etc/init/mongod.conf file.

		* Add the lines below immediately after chown $DEAMONUSER /var/run/mongodb.pid and before end script.
		
		```sh
		################################################################
		if test -f /sys/kernel/mm/transparent_hugepage/enabled; then
		   echo never > /sys/kernel/mm/transparent_hugepage/enabled
		fi
		if test -f /sys/kernel/mm/transparent_hugepage/defrag; then
		   echo never > /sys/kernel/mm/transparent_hugepage/defrag
		fi
		################################################################
		```

		* Restart mongod (service mongod restart).

3. Install MySQL

	```sh
	sudo apt-get install mysql-client mysql-server
	```

4. Login and create "josa" database

	```sh
	mysql -uroot -p

	create database josa;
	```

5. Download mysql JDBC connector and move it to $home/data-integration/lib

	```sh
	http://dev.mysql.com/downloads/connector/j/
	```

6. Download Pentaho community edition using the following link

	```sh
	http://community.pentaho.com/projects/data-integration/
	```


7. Unzip the Pentaho directory. To check your installation, navigate to the data-integration directory, and do the below command. If the installation is successful, a GUI will open. (For Windows users: you should only need to double click on the file)

	```sh
	sh spoon.sh
	```
8. For session 1, you will be using the exercise files under **Session1** in your cloned repository.


### Installation for Session 2

You need to be running docker 1.7 +. You can install it from https://docs.docker.com/linux/step_one/ or 	https://docs.docker.com/engine/installation/ubuntulinux/

*Note for Windows users: You will need to run all the below docker steps in a Virtual Machine running Ubuntu*

Proceed with the following steps: (If they don't work, you may need to write "sudo" before all the docker commands)

```sh
$ docker build -t josa-luigi .
```
You need to get the new image id that was created from the docker build.

```sh
$ docker images
```

Expected result

      REPOSITORY                 TAG                 IMAGE ID            CREATED           VIRTUAL SIZE
      josa-luigi                <TAG>              ca1e8215c861        few seconds ago      473.4 MB
      <some-image>              <TAG>              fb9c051ae80a         13 hours ago        473.4 MB

Spin off a new container

  * For Linux users:

	```sh
	$ docker run --name josa-luigi josa-luigi
	```

  * For Mac users:

	```sh
	$ docker run --name josa-luigi -P josa-luigi
	```


To ensure the container has started.

```sh
$ docker ps
```
Expected result

    CONTAINER ID        IMAGE                 COMMAND           ...                   PORTS
    9f544db853f3      josa-luigi        "/bin/sh -c 'exec /s      ...    22/tcp, 3306/tcp, 8082/tcp      

To SSH into the container (Not Recommended)

    docker inspect josa-luigi

Notice the auto-assigned IP (If running on a virtual machine, please use your host IP)
```sh
$ ssh ubuntu@<container-ip>
$ enter pass:
The password is -> "u"
```

### Demonizing Tornado/luigi static visualiser and central scheduler
    docker exec -i josa-luigi luigid --background --logdir /var/log/luigi/
    ## To access the web application
    ## From your host browser navigate to "http://<your-container-ip>:8020"

### Running the main command (Languages Count)
    docker exec -i josa-luigi bash -c "cd /home/ubuntu/josa/pipelines && PYTHONPATH=. luigi --module josagit AggregateLanguages"

### Viewing the output from docker (Languages count job)
    docker exec -i josa-luigi less /home/ubuntu/josa/pipelines/cleaned-data/aggregated-languages.json
