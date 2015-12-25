# JOSA Session

This repo will help you get started with our session using docker 1.7 +  

### Installation for Session 1

On your linux machine

Download Pentaho community edition using the following link

http://community.pentaho.com/projects/data-integration/

    ## navigate to your cloned repo and use the below command.
    unzip pentaho-jobs.zip

Open the exercise files

### Installation for Session 2

You need to be running docker 1.7 +

```sh
$ docker build -t josa-ds .
```
You need to get the new image id that was created from the docker build.

```sh
$ docker images
```

Expected result

      REPOSITORY                 TAG                 IMAGE ID            CREATED           VIRTUAL SIZE
    <composed-image-id>         <TAG>              ca1e8215c861        few seconds ago      473.4 MB
      <some-image>              <TAG>              fb9c051ae80a         13 hours ago        473.4 MB

Spin off a new container
```sh
$ docker run <composed-image-id>
```

To ensure the container has started.

```sh
$ docker ps
```
Expected result

    CONTAINER ID        IMAGE                 COMMAND           ...                   PORTS
    9f544db853f3  <composed-image-id> "/bin/sh -c 'exec /s      ...    22/tcp, 3306/tcp, 8082/tcp      

To SSH into the container (Not Recommended)

    docker inspect <container-id>

Notice the auto-assigned IP
```sh
$ ssh ubuntu@<container-ip>
$ enter pass:
The password is -> "u"
```

### Demonizing Tornado/luigi static visualiser and central scheduler
    docker exec -i <running-container-id/Name> luigid --background --logdir /var/log/luigi/

### Running the main command (Languages Count)
    docker exec -i <running-container-id/Name> bash -c "cd /home/ubuntu/josa/pipelines && PYTHONPATH=. luigi --module josagit AggregateLanguages"

### Viewing the output from docker (Languages count job)
    docker exec -i <running-container-id/Name> less /home/ubuntu/josa/pipelines/cleaned-data/aggregated-languages.json
