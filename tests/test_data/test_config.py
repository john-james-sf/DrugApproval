#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#==============================================================================#
# Project  : Predict-FDA                                                       #
# Version  : 0.1.0                                                             #
# File     : \test_aact.py                                                     #
# Language : Python 3.9.5                                                      #
# -----------------------------------------------------------------------------#
# Author   : John James                                                        #
# Company  : nov8.ai                                                           #
# Email    : john.james@nov8.ai                                                #
# URL      : https://github.com/john-james-sf/predict-fda                      #
# -----------------------------------------------------------------------------#
# Created  : Saturday, June 26th 2021, 1:48:44 pm                              #
# Modified : Friday, July 2nd 2021, 11:40:58 am                                #
# Modifier : John James (john.james@nov8.ai)                                   #
# -----------------------------------------------------------------------------#
# License  : BSD 3-clause "New" or "Revised" License                           #
# Copyright: (c) 2021 nov8.ai                                                  #
#==============================================================================#
import pytest
from configs.config import Config

@pytest.mark.config
class ConfigTests:

    def test_config_datasource(self):        
        config = Config()
        credentials = config.get('aact_credentials')
        assert isinstance(credentials, dict)
        assert credentials['database'] == 'AACT'
        assert credentials['user'] == 'postgres'
        assert credentials['host'] == 'localhost'
        assert credentials['port'] == '5432'

    def test_config_get_options(self):
        config = Config()
        website=config.get('aact', 'website')
        assert website == "https://aact.ctti-clinicaltrials.org/snapshots", "Options doesn't work"

        




