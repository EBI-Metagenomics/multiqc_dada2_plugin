# [MultiQC](https://multiqc.info) plugin for Dada2 (in [MGnify's Amplicon Pipeline](https://www.github.com/ebi-metagenomics/amplicon-pipeline))

This is a plugin for MultiQC, that adds QC sections to a MultiQC report for data output by the
[MGnify Amplicon Pipeline](https://www.github.com/ebi-metagenomics/amplicon-pipeline).

## Development requirements
`git`, `pixi.sh`.


## Installation
1. Git clone this repo.
2. `pixi install`

(Or set up a python environment, and use `pip install -e .`)

## Example use with demo data
`pixi run example_single`

This runs `multiqc example_data/single_run`, with the module in `src/data2_plugin`.
It also opens `multiqc_report.html`.

For a multi-run study:
`pixi run example_study`

## Integration via Docker
Build the docker image, based on the biocontainers version of multiqc:
`pixi run build_docker`

Run the docker image:
`pixi run run_docker`
(Which runs multiqc, with the module, in docker, on the example data.)
i.e. it runs `docker run --platform linux/amd64 -v $(PWD)/example_data:/data -v $(PWD)/reports:/reports quay.io/microbiome-informatics/multiqc-with-dada2 multiqc /data --outdir /reports`

