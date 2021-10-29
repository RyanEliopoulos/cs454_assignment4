
from DBInterface import DBInterface
from whoosh.index import open_dir

from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import qparser

from whoosh.fields import *
from whoosh import index
from whoosh.query import And
from whoosh.query import Or
from whoosh.query import Term

import os
import datetime


class IndexInterface(object):
    """
        Creates the index directory if it does not already exist upon init.
    """

    def __init__(self, db_path: str, indexdir: str = 'indexdir'):
        self.db_interface = DBInterface(db_path)
        self.indexdir = indexdir
        if os.path.exists(indexdir):
            self.ix = open_dir(indexdir)
        else:
            self.ix = self._create_index(indexdir)

    def _create_index(self, indexdir: str):
        """
            Transfers the data from sqlite database datastore.db into
            the whoosh index.

        :return:  Index object
        """
        schema = Schema(title=TEXT(stored=True),
                        content=TEXT(stored=True),
                        author=TEXT(stored=True),
                        permalink=STORED,
                        dt=DATETIME(stored=True))

        if not os.path.exists(indexdir):
            os.mkdir(indexdir)
        ix = index.create_in(indexdir, schema)
        self.ix = ix
        writer = ix.writer()

        # Transferring data from sqlite db to whoosh
        db = DBInterface('./datastore.db')
        ret = db.pull_table('wsb_posts')
        if ret[0] != 0:
            print(f'Error creating index: {ret}')
            exit()

        rows = ret[1]['content']
        for row in rows:
            dtime = datetime.datetime.fromtimestamp(row['timestamp'])
            writer.add_document(
                title=row['post_title'],
                content=row['post_content'],
                author=row['author'],
                permalink=row['permalink'],
                dt=dtime
            )
        writer.commit()
        return ix

    def search(self,
               search_string: str,
               result_count: int,
               mode: str,
               begin_date: str,
               end_date: str):
        """ searches the content, title, and author fields using the given search_string
            These results are ANDed with the date range to allow temporal filtering.
        """
        ix = self.ix
        with ix.searcher() as searcher:
            if mode == 'AND':
                parsegroup = qparser.AndGroup
            elif mode == 'OR':
                parsegroup = qparser.OrGroup

            # parsing the search string
            parser = MultifieldParser(["content", "title", "author"], ix.schema,
                                      group=parsegroup)  # Marking 'default' search field
            myquery = parser.parse(search_string)

            # Parsing the date
            datequery = parser.parse(f'dt:[{begin_date} to {end_date}]')

            joined_query = And([myquery, datequery])
            results = searcher.search(joined_query, limit=result_count)
            for x in range(result_count):
                try:
                    print(results[x])
                except IndexError:  # Out of results
                    return

    def testing_search(self, search_string: str, result_count: int = 10, mode: str = 'AND'):
        """ searches the content, title, and author fields"""
        ix = self.ix
        with ix.searcher() as searcher:
            if mode == 'AND':
                parsegroup = qparser.AndGroup
            elif mode == 'OR':
                parsegroup = qparser.OrGroup
            parser = MultifieldParser(["content", "title", "author"], ix.schema,
                                      group=parsegroup)  # Marking 'default' search field
            myquery = parser.parse(search_string)
            results = searcher.search(myquery)
            for x in range(result_count):
                try:
                    print(results[x])
                except IndexError:  # Out of results
                    return



    # def dt_search(self, date_string: str, result_count: int = 10):
    #     """
    #         Searches the datetime field  (posting date)
    #     """
    #     ix = self.ix
    #     with ix.searcher() as searcher:
    #         parser = MultifieldParser(["dt"], ix.schema)  # Marking 'default' search field
    #         myquery = parser.parse(date_string)
    #         results = searcher.search(myquery)
    #         for x in range(result_count):
    #             try:
    #                 print(results[x])
    #             except IndexError:  # Out of results
    #                 return
    #
    # def combined_search(self, date_string: str, search_string: str, result_count: int = 10):
    #     ix = self.ix
    #     with ix.searcher() as searcher:
    #         parser = MultifieldParser(["dt"], ix.schema)  # Marking 'default' search field
    #         myquery = parser.parse(date_string)
    #         results = searcher.search(myquery)
    #         for x in range(result_count):
    #             try:
    #                 print(results[x])
    #             except IndexError:  # Out of results
    #                 return