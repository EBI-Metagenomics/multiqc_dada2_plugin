#!/usr/bin/env python

""" MultiQC example plugin module """

from __future__ import print_function

import logging

from multiqc import config
from multiqc.base_module import BaseMultiqcModule


# Initialise the main MultiQC logger
log = logging.getLogger('multiqc')

class MultiqcModule(BaseMultiqcModule):
    PROPORTION_CHIMERIC = "proportion_chimeric"

    PROPORTION_CHIMERIC_THRESHOLD = 0.25

    def __init__(self):

        # Halt execution if we've disabled the plugin
        if config.kwargs.get('disable_plugin', True):
            return

        # Initialise the parent module Class object
        super(MultiqcModule, self).__init__(
            name = 'Dada2 Amplicon Pipeline QC',
            target = "dada2",
            anchor = 'dada2',
            href = 'https://github.com/ebi-metagenomics/amplicon-pipeline',
            info = " is a plugin to show dada2-related QC information from MGnify's amplicon analysis pipeline"
        )

        # Find and load any input files for this module
        # self.stats_files = []
        self.stats = {}
        for f in self.find_log_files('dada2/stats'):
            self.parse_stats(f)
            self.add_data_source(f)

        is_single_sample = len(self.stats) == 1

        if is_single_sample:
            self.chimeric_warning_single_run()
        else:
            self.chimeric_warning_multi_run()

        self.write_data_file(self.stats, 'dada2_general_stats.json')
        print(self.stats)
        self.qc_table()

    def parse_stats(self, f):
        sample_name = f['s_name'].split("_")[0]
        sample_name = self.clean_s_name(sample_name, f)
        this_sample_stats = {}
        for stats_line in f['f'].splitlines():
            stat_name, stat = stats_line.split("\t")  # e.g. total_reads, 1000
            this_sample_stats[stat_name] = stat

        self.stats[sample_name] = this_sample_stats

    def chimeric_warning_single_run(self):
        only_sample = list(self.stats.values())[0]
        proportion_chimeric = float(only_sample.get(self.PROPORTION_CHIMERIC, 0))
        chimeric_content = f"""
            {round(proportion_chimeric * 100)}% of reads were removed as chimeric, which is considered normal.
        """
        if proportion_chimeric >= self.PROPORTION_CHIMERIC_THRESHOLD:
            chimeric_content = f"""
            <div class="alert alert-warning" role="alert">
                <h4 class="alert-heading"> ⚠️ High number of chimeric reads </h4>
                A high proportion of the reads were removed as being chimeric, by dada2.
                <hr/>
                <h1 class="display-5">{round(proportion_chimeric * 100)}%</h1> of reads removed
            </div>
            """
        self.add_section(
            name="Chimeric reads",
            description="""
                Dada2 removes chimeric reads.
                If a lot of reads are flagged as chimeric and removed, it can indicate problems with the
                data such as incorrect primer removal.
                """,
            content=chimeric_content
        )

    def chimeric_warning_multi_run(self):
        proportions_chimeric = [float(stat[self.PROPORTION_CHIMERIC]) for stat in self.stats.values()]
        samples_chimeric_above_threshold = len([p for p in proportions_chimeric if p >= self.PROPORTION_CHIMERIC_THRESHOLD])

        fraction_of_samples_highly_chimeric = samples_chimeric_above_threshold / len(proportions_chimeric)

        chimeric_content = f"""
            {fraction_of_samples_highly_chimeric} of the samples had high proportion of chimeric reads, 
            which is considered normal. 
        """

        if fraction_of_samples_highly_chimeric >= 0.5:
            chimeric_content = f"""
            <div class="alert alert-warning" role="alert">
                <h4 class="alert-heading"> ⚠️ High number of samples had high chimeric read counts </h4>
                A high proportion of the samples had &#8805;{100*self.PROPORTION_CHIMERIC_THRESHOLD}&#37;
                of their reads removed as being chimeric, by dada2.
                <hr/>
                <h1 class="display-5">{round(fraction_of_samples_highly_chimeric * 100)}%</h1> of samples had high chimeric read counts
            </div>
            """
        self.add_section(
            name="Chimeric reads",
            description="""
                Dada2 removes chimeric reads.
                If a lot of reads are flagged as chimeric and removed, it can indicate problems with the
                data such as incorrect primer removal.
                If a lot of samples have read counts breaching this threshold, it can indicate problems with the entire study.
                """,
            content=chimeric_content
        )


    def qc_table(self):
        """
        Adds dada2 qc cols to general stats table
        """
        headers = {
            "initial_number_of_reads": {
                "title": "Initial reads",
                "description": "Count of reads before QC",
                "scale": "Blues",
            },
            "proportion_matched": {
                "title": "Proportion matched",
                "description": "Fraction of reads left after truncating",
                "min": 0,
                "max": 1,
                "scale": "YlGn",
            },
            "proportion_chimeric": {
                "title": "Proportion chimeric",
                "description": "Fraction of reads removed as chimeric",
                "min": 0,
                "max": 1,
                "scale": "OrRd",
            },
            "final_number_of_reads": {
                "title": "Final reads count",
                "description": "Count of reads after QC",
                "scale": "Blues",
            }
        }
        self.general_stats_addcols(self.stats, headers)