FROM debian:stable

LABEL maintainer "Emilio Palumbo <emilio.palumbo@crg.eu>" \
      version "1.0" \
      description "Docker image for ggsashimi"

# install needed tools
RUN apt-get update --fix-missing -qq && \
        apt-get install -y -q \
    curl \
    locales \
    libncurses5-dev  \
    libncursesw5-dev \
    build-essential \
    pkg-config \
    zlib1g-dev \
    bzip2 \
    r-base \
    python \
    libcairo2-dev \
    && apt-get clean \
    && apt-get purge \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN apt-get update && \
	apt-get upgrade -y && \
	apt-get install -y wget vim bzip2 less

# install SAMtools
RUN curl -fksSL https://github.com/samtools/samtools/releases/download/1.3.1/samtools-1.3.1.tar.bz2 | tar xj && \
    cd samtools-1.3.1 && \
    make all all-htslib && make install install-htslib

## Install R packages for ggplot2
RUN R -e 'install.packages( c("ggplot2", "gridExtra", "data.table", "svglite"), repos="http://cloud.r-project.org/");'

RUN wget --quiet https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
	bash ~/miniconda.sh -b -p /opt/conda && \
	rm ~/miniconda.sh

ENV PATH /opt/conda/bin:$PATH

RUN conda update conda -y

RUN pip install pandas

# Copy ggsashimi in the docker image
ADD ggsashimi/sashimi-plot.py /
ADD visualize_junctions.py /
ADD ggsashimi/palette.txt /

RUN apt-get install -y gzip

