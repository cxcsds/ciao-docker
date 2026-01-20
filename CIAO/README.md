
# CIAO-4.17 Docker Image

## Install podman (or docker)

[`podman`](https://podman.io/) is a open source alternative to the commercial docker product.
It is a drop-in replacement.  It also does not require root/admin
privileges to run, and does not require any system services to be running.

It's available in most Linux distro's repositories.  Also available for
Mac and Windows.

Note: mac will need Xquartz; windows needs an X server. Linux wayland users ...
don't know.

In the examples below I will be using the variable `$docker` to reference the
command to run, for podman use

```bash
docker=podman
```

for docker use

```bash
docker=docker
```


---

## Download ciao-4.17 image tar file


This is just a temporary location. 

```bash
curl -O https://saotrace.cfa.harvard.edu/ciao/ciao-4.17.0.pod.tar.gz 
```

The download is ~3Gb. Do not un-tar and do not un-gzip the file. 


---

## Install docker image

**Note** Do not do this on your HEAD machine/account.  The files are stored
in your home directory, and you will exceed quota.

Run

```bash
$docker load -i ciao-4.17.0.pod.tar.gz
```

For those in the know, this is equivalent to running

```bash
$docker pull ...stuff...
```

from a hosted repository.

---

## Check the image is loaded

Run

```bash
$docker image ls
REPOSITORY                TAG         IMAGE ID      CREATED         SIZE
localhost/ciao            4.17        6c2c8a2b5041  11 minutes ago  6.85 GB
```

You can refer to the image as `ciao:4.17` or by the SHA `6c2c8a2b5041`


---

## Run the image

### Linux:

Run:

```bash
$docker run -i -t --rm \
  -h $HOSTNAME -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v $XAUTHORITY:/home/docker/.Xauthority \
  -p 8888:8888 \
  ciao:4.17
```

The last `ciao:4.17` is the tag for the image.

Most of the various flags are to get X11 to work securely. **Note**: You
may not have `$XAUTHORITY` set.  If that's the case then try
`$HOME/.Xauthority`.  Are you using _Wayland_?  No idea if this will
work; you might need to try the macOS instructions.

The `-p` flag is needed to run Jupyter labs/notebooks.

You will probably need to `chown` the `.Xauthority` file 

```bash
sudo chown docker:docker /home/docker/.Xauthority
```

to allow ds9/matplotlib to display correctly.


### macOS


Before starting you need to install Xquartz.  You will need to logout
or reboot after installing Xquartz for the DISPLAY to be set.
In Xquartz go to Settings, Security, and enable "Allow connections from network clients"
then exit and restart Xquartz for the setting to take effect.

Next, in your `terminal` you will need to run

```bash
xhost + 127.0.0.1
```

before running the container. 

Then

```bash
$docker run --rm -i -t \
    -e DISPLAY=host.docker.internal:0 \
    -p 8888:8888 \
    ciao:4.17
```

You should run `xhost -` after you are done and exit the container.


### Windows

Window users -- if you have an Xserver running you can try the same command
as macos.  Otherwise you can simply run

```bash
$docker run --rm -i -t -p 8888:8888 ciao:4.17
```

Note that ds9 and matplotlib will not work w/o an Xserver.

## Start Working

At this point you will be logged into the container and the prompt will
change and look something like:

```bash
(ciao-4.17.0) docker@my_laptop_name:~$
```

The `(ciao-4.17.0)` is the standard conda prompt change.  `docker` is the
username inside the container.


---
## Go to work

You now have CIAO running in a container.  Note that there is no
CALDB installed so you would need to install it separately or use the
`download_obsid_caldb` script.

This also probably is not too useful because it's not able to see
any files/folders on your host machine.  You might want to exit out
of the container and add another "-v" flag to add a data directory
to share/export/mount to the container

For example:

```bash
$docker run -i -t \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -h $HOSTNAME -e DISPLAY=$DISPLAY \
  -v $XAUTHORITY:/home/docker/.Xauthority \
  -v $HOME/MyDataDirectory:/home/docker/data \
  -p 8888:8888 \
  ciao:4.17
```

would mount the `$HOME/MyDataDirectory` directory on the host
as `/home/docker/data`, eg `$HOME/data`, on the container. If you
have a CALDB then you can also mount it the same way.


## Note on `Dockerfile`

The google oracles recommend installing into the `base`
environment because w/ containers not really meant to be switching
between environments.  But since `base` is using a different version
of Python, I had to install into a separate environment.

## Note on Jupyter

The Dockerfile adds files to the ~/.jupyter container to allow
jupyter notebook and lab to listen to external IP address '0.0.0.0'
You can run

```bash
jupyter lab
```

and then access the notebook server using the `127.0.0.1` URL it provides.






