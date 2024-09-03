#!/usr/bin/env python
""" MultiQC

We can add any custom Python functions here and call them
using the setuptools plugin hooks.
"""

from __future__ import print_function
import logging

from multiqc import config

# Initialise the main MultiQC logger
log = logging.getLogger('multiqc')


# Add default config options for the things that are used by dada2 plugin

def dada2_plugin_execution_start():
    """ Code to execute after the config files and
    command line flags have been parsed.

    This setuptools hook is the earliest that will be able
    to use custom command line flags.
    """

    # Halt execution if we've disabled the plugin
    if config.kwargs.get('disable_plugin', True):
        return None

    # Add to the main MultiQC config object.
    # User config files have already been loaded at this point
    #   so we check whether the value is already set. This is to avoid
    #   clobbering values that have been customised by users.

    if 'dada2/stats' not in config.sp:
        print("Using default path to dada2 stats")
        config.update_dict( config.sp, { 'dada2/stats': { 'fn': '*_dada2_stats.tsv' } } )
