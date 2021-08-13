#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# =========================================================================== #
# Project  : Drug Approval Analytics                                          #
# Version  : 0.1.0                                                            #
# File     : \src\operations\artifacts.py                                     #
# Language : Python 3.9.5                                                     #
# --------------------------------------------------------------------------  #
# Author   : John James                                                       #
# Company  : nov8.ai                                                          #
# Email    : john.james@nov8.ai                                               #
# URL      : https://github.com/john-james-sf/drug-approval-analytics         #
# --------------------------------------------------------------------------  #
# Created  : Saturday, July 31st 2021, 3:44:38 am                             #
# Modified : Thursday, August 12th 2021, 8:59:10 pm                           #
# Modifier : John James (john.james@nov8.ai)                                  #
# --------------------------------------------------------------------------- #
# License  : BSD 3-clause "New" or "Revised" License                          #
# Copyright: (c) 2021 nov8.ai                                                 #
# =========================================================================== #
# %%
"""Repository of Metadata."""
from abc import ABC, abstractmethod
from datetime import datetime
import logging

import pandas as pd

from ..database.connect import PGConnectionFactory
from ..database.access import PGDao
from ..config import DBCredentials
# --------------------------------------------------------------------------- #
logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
#                              ARTIFACTS                                      #
# --------------------------------------------------------------------------- #


class Artifact(ABC):

    def __init__(self, *args, **kwargs) -> None:
        self._connection_factory = PGConnectionFactory()
        self._dao = PGDao()
        self._schema = 'public'

    @abstractmethod
    def create(self, name: str, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def read(self, name: str = None, *args, **kwargs) -> \
            pd.DataFrame:
        pass

    @abstractmethod
    def update(self, name: str, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def delete(self, name: str, *args, **kwargs) -> None:
        pass


# --------------------------------------------------------------------------- #


class DataSource(Artifact):

    def __init__(self, credentials: DBCredentials,
                 autocommit: bool = False) -> None:
        super(DataSource, self).__init__(credentials=credentials,
                                         autocommit=autocommit)
        self._table = 'datasource'

    def create(self,
               name: str,
               source_type: str,
               version: int,
               webpage: str,
               link: str,
               link_type: str,
               frequency: int,
               lifecycle: int,
               creator: int,
               has_changed: bool,
               source_updated: datetime,
               created: datetime,
               created_by: str,
               title: str = None,
               description: str = None,
               coverage: str = None,
               maintainer: str = None,
               **kwargs) -> None:

        columns = ["name", "source_type", "version", "webpage",
                   "link", "link_type", "frequency", "lifecycle", "creator",
                   "has_changed", "source_updated", "created", "created_by",
                   "title", "description", "coverage", "maintainer"]

        values = [name, source_type, version, webpage,
                  link, link_type, frequency, lifecycle, creator,
                  has_changed, source_updated, created, created_by,
                  title, description, coverage, maintainer]

        for k, v in kwargs.items():
            columns.append(k)
            values.append(v)
        self._dao.create(table=self._table, columns=columns, values=values,
                         schema=self._schema)

    def read(self, name: str = None) -> pd.DataFrame:
        if name is not None:
            result = self._dao.read(table=self._table,
                                    where_key='name',
                                    where_value=name,
                                    schema=self._schema)
        else:
            result = self._dao.read(table=self._table,
                                    schema=self._schema)
        return result

    def update(self, name: str, version: int, uris: list,
               has_changed: bool, source_updated: datetime,
               updated: datetime, updated_by: str) -> None:

        self._dao.connect()
        self._dao.begin()
        self._dao.update(table=self._table, column='uris', value=uris,
                         where_key='name', where_value=name,
                         schema=self._schema)
        self._dao.update(table=self._table, column='has_changed',
                         value=has_changed,
                         where_key='name', where_value=name,
                         schema=self._schema)
        self._dao.update(table=self._table, column='source_updated',
                         value=source_updated,
                         where_key='name', where_value=name,
                         schema=self._schema)
        self._dao.update(table=self._table, column='updated',
                         value=updated,
                         where_key='name', where_value=name,
                         schema=self._schema)
        self._dao.update(table=self._table, column='updated_by',
                         value=updated_by,
                         where_key='name', where_value=name,
                         schema=self._schema)
        self._dao.commit()
        self._dao.close()

    def delete(self, name) -> None:
        self._dao.delete(table=self._table, where_key='name', where_value=name,
                         schema=self._schema)


# --------------------------------------------------------------------------- #
#                              EVENTS                                         #
# --------------------------------------------------------------------------- #
class Event(ABC):

    def __init__(self, credentials: DBCredentials, autocommit=True,
                 *args, **kwargs) -> None:
        self._credentials = credentials
        self._dao = PGDao(credentials=credentials, autocommit=autocommit)
        self._schema = 'public'

    @abstractmethod
    def create(self, name: str, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def read(self, name: str = None, *args, **kwargs) -> \
            pd.DataFrame:
        pass

    @abstractmethod
    def delete(self, id: int, *args, **kwargs) -> None:
        pass


# --------------------------------------------------------------------------- #
class DataSourceEvent(Event):

    def __init__(self, credentials: DBCredentials) -> None:
        super(DataSourceEvent, self).__init__(credentials=credentials)
        self._table = 'datasourceevent'

    def create(self, **kwargs) -> None:
        columns = [k for k in kwargs.keys()]
        values = [v for v in kwargs.values()]

        self._dao.create(table=self._table, columns=columns, values=values,
                         schema=self._schema)

    def read(self, name: str = None) -> pd.DataFrame:
        if name is None:
            df = self._dao.read(table=self._table)
        else:
            df = self._dao.read(table=self._table,
                                where_key="name", where_value=name)
        return df

    def delete(self, id: int = None) -> pd.DataFrame:
        self._dao.delete(table=self._table, where_key="id", where_value=id)
