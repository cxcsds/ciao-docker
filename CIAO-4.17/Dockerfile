FROM debian:stable

LABEL maintainer="Ken Glotfelty <glotfeltyk@si.edu>" \
      description="CIAO 4.17/debian:stable; this is *not* an official CXC product" \
      version="ciao-4.17/conda/debian:stable"

ARG CONDA_DIR=/opt/conda
ARG USERNAME=docker
ARG USERID=1000

RUN apt-get update && \
    apt-get install -y --no-install-recommends git wget unzip bzip2 build-essential ca-certificates x11-apps libxml2 sudo file curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV DISPLAY :0

# For Jupyter labs/notebook
EXPOSE 8888

# Create the user
RUN useradd --create-home -s /bin/bash --no-user-group -u $USERID $USERNAME && \
    mkdir -p /opt && \
    chmod 777 /opt && \
    chown $USERNAME /opt && \
    adduser $USERNAME sudo && \
    echo "$USERNAME ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    echo 'export PATH=$CONDA_DIR/bin:$PATH' > /etc/profile.d/conda.sh

USER $USERNAME
WORKDIR /home/$USERNAME
ADD ./ciao-4.17.0.yml jupyter_lab_config.py jupyter_notebook_config.py .

# Install miniconda
ENV PATH $CONDA_DIR/bin:$PATH
RUN wget --quiet https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    /bin/bash /tmp/miniconda.sh -b -p $CONDA_DIR && \
    rm -rf /tmp/* && \
    mkdir ~/.jupyter && \
    mv jupyter_lab_config.py jupyter_notebook_config.py ~/.jupyter/

RUN conda env create -n ciao-4.17.0 --file ./ciao-4.17.0.yml &&\
    conda clean -tipy && \
    conda init bash && \
    echo "conda activate ciao-4.17.0" >> /home/$USERNAME/.bashrc 


