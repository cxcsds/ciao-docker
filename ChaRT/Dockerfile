FROM saotrace:2.0.5

LABEL maintainer="Ken Glotfelty <glotfeltyk@si.edu>" \
      description="ChaRT/debian:stable; this is *not* an official CXC product" \
      version="chart-2.0.5-4.17.0/debian:stable"

ARG CONDA_DIR=/opt/conda
ARG CIAOVER=4.17.0
ARG CALDBVER=4.12.0
ARG PYVER=3.12

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

# Install miniconda
ENV PATH $CONDA_DIR/bin:$PATH
RUN curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh -o /tmp/miniconda.sh && \
    /bin/bash /tmp/miniconda.sh -b -p $CONDA_DIR && \
    rm -rf /tmp/miniconda.sh && \
    conda install conda-build --yes 

# After installing CIAO 4.17 we delete a bunch of stuff that is not
# needed for ChaRT including
# - xspec spectral models
# - X11 stuff used by matplotlib
# - matplotlib, jupyter notbook stuff
# - boost library/headers (only used by mkosip, and huge!)
# - etc.

# Install CIAO

COPY ciao-4.18.0.dev-py312h90da0fc_0.conda ./linux-64/

RUN \
    conda index /workdir && \
    conda create -n ciao-${CIAOVER} -c file://`pwd`/ -c https://cxc.cfa.harvard.edu/conda/test \
       ciao=4.18.0.dev sherpa ciao-contrib file \
     &&\
    conda clean -tipy && \
    conda env config vars set CALDB=$CONDA_DIR/envs/ciao-${CIAOVER}/CALDB -n ciao-${CIAOVER} && \
    conda env config vars set CALDBCONFIG=$CONDA_DIR/envs/ciao-${CIAOVER}/CALDB/software/tools/caldb.config -n ciao-${CIAOVER} && \
    conda env config vars set CALDBALIAS=none -n ciao-${CIAOVER} && \
    conda remove -n ciao-${CIAOVER} --force -y xspec-modelsonly && \
    /bin/rm -rf .cache noarch linux-64 && \
    conda init bash && \
    /bin/rm -rf $CONDA_DIR/pkgs && \
    echo "conda activate ciao-${CIAOVER}" >> /workdir/.bashrc 

WORKDIR /workdir

# Now install ChaRT website files

# Website stuff
COPY index.html /proj/saotrace/
COPY cgi-bin /proj/saotrace/cgi-bin
COPY soft /proj/saotrace/soft
COPY htdocs/v2.1 /proj/saotrace/htdocs/v2.1
COPY htdocs  /proj/saotrace/htdocs
COPY launch /proj/saotrace

# Patched version of simulate_psf that uses SAOTrace
COPY simpsf.tar ./

RUN \
	tar xf simpsf.tar && \
    mv -vf simulate_psf $CONDA_DIR/envs/ciao-${CIAOVER}/bin/simulate_psf && \
    mv -vf simulate_psf.par $CONDA_DIR/envs/ciao-${CIAOVER}/param/simulate_psf.par && \
    mv -vf runtool.py $CONDA_DIR/envs/ciao-${CIAOVER}/lib/python${PYVER}/site-packages/ciao_contrib/runtool.py  && \
    mv -vf ./CALDB $CONDA_DIR/envs/ciao-${CIAOVER}/ 
  
ENTRYPOINT /proj/saotrace/launch
