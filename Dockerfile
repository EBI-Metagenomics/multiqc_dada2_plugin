FROM quay.io/biocontainers/multiqc:1.24.1--pyhdfd78af_0
LABEL authors="metagenomics@ebi.ac.uk"
COPY src /opt/dada2/src
COPY pyproject.toml /opt/dada2/pyproject.toml
RUN pip install -e /opt/dada2
