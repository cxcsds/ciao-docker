FROM saotrace:2.1.0

LABEL maintainer="Ken Glotfelty <glotfeltyk@si.edu>" \
      description="ChaRT: Chandra Ray Tracer; this is *not* an official CXC product" \
      version="chart-2.1.0-4.18.0/debian:stable"

ARG CONDA_DIR=/opt/conda
ARG CIAOVER=4.18.0
ARG CALDBVER=4.12.0

# For ChaRT
EXPOSE 8888

RUN mkdir -p /proj/saotrace && chmod 777 /opt /proj/saotrace

WORKDIR /workdir

# Add minimal CALDB w/ just pixlib CALDB files (needs w/ dmcoords)
COPY chandra_caldb_pixlib-${CALDBVER}.tar ./
RUN \
	tar xf chandra_caldb_pixlib-${CALDBVER}.tar && \
	chmod -R a+rwx CALDB  && \
    mkdir -p /workdir/linux-64 && \
    chmod -R a+rwx /workdir/linux-64

# The SAOTrace docker image creates the saotrace user w/ /workdir as the homedir
USER saotrace

COPY ciao-4.18.0-py312h946e58c_0.conda ./linux-64/

# Install miniconda
ENV PATH $CONDA_DIR/bin:$PATH
RUN curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh -o /tmp/miniconda.sh && \
    /bin/bash /tmp/miniconda.sh -b -p $CONDA_DIR && \
    rm -rf /tmp/miniconda.sh && \
    conda install conda-build --yes && \
    conda index /workdir && \
    conda create -n ciao-${CIAOVER} -c file://`pwd`/ -c https://cxc.cfa.harvard.edu/conda/ciao \
       ciao=${CIAOVER} sherpa ciao-contrib file &&\
    conda clean -tipy && \
    conda env config vars set CALDB=$CONDA_DIR/envs/ciao-${CIAOVER}/CALDB -n ciao-${CIAOVER} && \
    conda env config vars set CALDBCONFIG=$CONDA_DIR/envs/ciao-${CIAOVER}/CALDB/software/tools/caldb.config -n ciao-${CIAOVER} && \
    conda env config vars set CALDBALIAS=none -n ciao-${CIAOVER} && \
    conda remove -n ciao-${CIAOVER} --force -y xspec-modelsonly && \
    /bin/rm -rf .cache noarch linux-64 && \
    conda init bash && \
    /bin/rm -rf $CONDA_DIR/pkgs && \
    echo "conda activate ciao-${CIAOVER}" >> /workdir/.bashrc && \
    mv -vf ./CALDB $CONDA_DIR/envs/ciao-${CIAOVER}/

# Now install ChaRT website files
COPY index.html /proj/saotrace/
COPY cgi-bin /proj/saotrace/cgi-bin
COPY soft /proj/saotrace/soft
COPY htdocs/v2.1 /proj/saotrace/htdocs/v2.1
COPY htdocs  /proj/saotrace/htdocs
COPY launch /proj/saotrace

ENTRYPOINT /proj/saotrace/launch
