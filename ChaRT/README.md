
# Using _ChaRT_ container image 

This README provides information on how to run (ChaRT)[https://cxc.cfa.harvard.edu/ciao/PSFs/chart2/] 
from the container image provided.

ChaRT is the web-based front end to the official Chandra Ray 
Tracing software: SAOTrace. ChaRT provides a simple interface that allows
users to simulate the Point Spread Function (PSF) for a Chandra observation
given an input spectrum and location in the field. 

> The Chandra PSF varies significantly across the field of view.


## Load ChaRT image

Download the ChaRT container image from **TBD**. Then load the image
into podman (or Docker) using the following command:

```bash
podman image load -i chart-2.0.5-4.17.0.tar.gz
```

To check that the image has been loaded use

```bash
podman image ls
```

## Run ChaRT

ChaRT will run inside the container and will generate output file(s).
These output files will be "ray" files which contain simulated photons
at the exit of the HRMA which then need to be projected onto the
Chandra detectors using either MARX or psf_project_ray. 

### Identify output directory

ChaRT outputs will be generated in the

```bash
/workdir/output
```

directory. The easiest way to access these output will be to mount
a directory on the host machine to that location.  In the example below we
are using `/Users/mac_user/Temp/workdir/output`.

### Run ChaRT web server

We can now run the web server from the command line

```bash
podman run --rm -t -p 8888:8888 --arch=amd64 -v /Users/mac_user/Temp/workdir/output:/workdir/output --name=chart chart:2.0.5-4.17.0
```

The arguments are as follows.

`--rm` will remove the container (and all files inside it) when the container exits.

`-t` connects the standard output & error from the virtual machine
to the host; upshot is that you will see outputs from the webserver 
and jobs display in the terminal window where `podman` was run.

`-p 8888:8888` maps port 8888 on the host (ie your mac) to port 8888 on the 
container image (virtual machine). The ChaRT web server is setup to serve on port
8888; but you can choose whatever port number, over 1000, you want on the host.

`--arch=amd64` lets your mac know that you are running a Linux
virtual machine that is built for AMD64 architecture. This allows it to run
on Apple silicon (M1/ARM chips).

`-v host_path:/workdir/output` mounts the `/workdir/output` directory on the
VM to a directory on the host machine. The output files will be 
available in the `host_path` directory.

`--name=chart` just gives the container a nice, easy to remember name.

`chart:2.0.5-4.17.0` is the name of the container image that you saw
when you did the `podman image ls` command (above).


### Run ChaRT

In you browser go to

```
http://localhost:8888/
```

which will redirect you to a different page. From here you specify
the ChaRT parameters.  For more information on these values see
(Preparing to Run ChaRT)[https://cxc.cfa.harvard.edu/ciao/threads/prep_chart/index.html].

That is all there is to it. Once SAOTrace has simulated the rays and
ChaRT has packaged everything up, the outputs will be in a compressed
tar file in the `host_post` directory.


### Stop ChaRT web server

To stop the ChaRT web server you cannot simply Ctrl+C to kill it. 
You have to run the `container stop` command in a separate terminal window:

```bash
podman container stop chart
```

## Building ChaRT image

Below are instructions for building the ChaRT image.  All the files
are available on github **TBD**.


### Install SAOTrace image

We will use the official SAOTrace docker image as our base image.

You need to load the docker image just like above

```bash
podman image load -i saotrace-docker-image-2.0.5.tar.gz
```

### Create ChaRT image

Next we build the ChaRT image 

```bash
cd .../ciao-docker/ChaRT
podman build --arch=amd64 -t chart:2.0.5-4.17.0 .
``` 

The `Dockerfile` installs CIAO 4.17.0 and the manually removes 
a bunch of stuff that is not needed by ChaRT including 
xspec models, jupyter notebook, matplotlib, x11 libs, qt stuff,
and some random data files. This is all to reduce the VM from 6Gb to 1.2Gb. 

It then installs a bare minimal CALDB w/ only the files  used by pixlib
(needed for coordinate conversions). After which it then installs the
ChaRT web pages and CGI scripts. Finally it patches the version of 
the simulate_psf script with the version used by ChaRT that has 
SAOTrace enabled. 


### Save ChaRT image

Finally 

```
podman image save -o chart-2.0.5-4.17.0.tar chart:2.0.5-4.17.0
gzip chart-2.0.5-4.17.0.tar
```
