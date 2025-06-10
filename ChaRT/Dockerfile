FROM saotrace:2.0.5

LABEL maintainer="Ken Glotfelty <glotfeltyk@si.edu>" \
      description="ChaRT/debian:stable; this is *not* an official CXC product" \
      version="chart-2.0.5-4.17.0/debian:stable"

ARG CONDA_DIR=/opt/conda

# For ChaRT
EXPOSE 8888

RUN mkdir -p /proj/saotrace && chmod 777 /opt /proj/saotrace

# The SAOTrace docker image creates the saotrace user w/ /workdir as the homedir
USER saotrace
WORKDIR /workdir

# Install CIAO-4.17

ADD ./ciao-4.17.0.yml ./

# Install miniconda
ENV PATH $CONDA_DIR/bin:$PATH
RUN curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh -o /tmp/miniconda.sh && \
    /bin/bash /tmp/miniconda.sh -b -p $CONDA_DIR && \
    rm -rf /tmp/miniconda.sh

# After installing CIAO 4.17 we delete a bunch of stuff that is not 
# needed for ChaRT including
# - xspec spectral models
# - X11 stuff used by matplotlib
# - matplotlib, jupyter notbook stuff
# - boost library/headers (only used by mkosip, and huge!)
# - etc.

RUN \
    conda env create -n ciao-4.17.0 --file ./ciao-4.17.0.yml &&\
    conda install -y -n ciao-4.17.0 file --freeze-installed && \
    conda clean -tipy && \
    conda env config vars set CALDB=$CONDA_DIR/envs/ciao-4.17.0/CALDB -n ciao-4.17.0 && \
    conda env config vars set CALDBCONFIG=$CONDA_DIR/envs/ciao-4.17.0/CALDB/software/tools/caldb.config -n ciao-4.17.0 && \
    conda env config vars set CALDBALIAS=none -n ciao-4.17.0 && \    
	cd $CONDA_DIR/envs/ciao-4.17.0/ && \
    /bin/rm -rf spectral test include docs && \
    (cd data && /bin/ls *.fits | grep -v wtsimres | xargs -I@ /bin/rm @) && \
    conda remove -n ciao-4.17.0 boost-cpp qt-main \
    xorg-kbproto xorg-libice xorg-libsm xorg-libx11 \
    xorg-libxau xorg-libxdmcp xorg-libxext \
    xorg-libxrender xorg-renderproto xorg-xextproto xorg-xproto \
    jupyter notebook pyqt pyqt5-sip \
    jupyter-lsp jupyter_client jupyter_console \
    jupyter_core jupyter_events jupyter_server jupyter_server_terminals \
    jupyterlab jupyterlab_pygments jupyterlab_server jupyterlab_widgets \
    --force -y && \
    /bin/rm -rf $CONDA_DIR/pkgs && \
    conda init bash && \
    echo "conda activate ciao-4.17.0" >> /workdir/.bashrc 

WORKDIR /workdir

# Now install ChaRT website files

# Add minimal CALDB w/ just pixlib CALDB files (needs w/ dmcoords)
ADD chandra_caldb_pixlib-4.12.0.tar ./

# Website stuff
ADD index.html /proj/saotrace/
ADD cgi-bin /proj/saotrace/cgi-bin
ADD soft /proj/saotrace/soft
ADD htdocs/v2.1 /proj/saotrace/htdocs/v2.1
ADD htdocs  /proj/saotrace/htdocs
ADD launch /proj/saotrace

# Patched version of simulate_psf that uses SAOTrace
ADD simpsf.tar ./

RUN cd /workdir && \
    cp -f simulate_psf $CONDA_DIR/envs/ciao-4.17.0/bin/simulate_psf && \
    cp -f simulate_psf.par $CONDA_DIR/envs/ciao-4.17.0/param/simulate_psf.par && \
    cp -f runtool.py $CONDA_DIR/envs/ciao-4.17.0/lib/python3.11/site-packages/ciao_contrib/runtool.py  && \
    cp -r ./CALDB $CONDA_DIR/envs/ciao-4.17.0/ 

ENTRYPOINT /proj/saotrace/launch
