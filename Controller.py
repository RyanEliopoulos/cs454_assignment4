
from DBInterface import DBInterface
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.searching import Results

from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser

from whoosh.fields import *
from whoosh import index
import os
import datetime


class Controller(object):
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

    def search(self, search_string: str, result_count: int = 10):
        """ searches the content, title, and author fields"""
        ix = self.ix
        with ix.searcher() as searcher:
            parser = MultifieldParser(["content", "title", "author"], ix.schema)  # Marking 'default' search field
            myquery = parser.parse(search_string)
            results = searcher.search(myquery)
            for x in range(result_count):
                try:
                    print(results[x])
                except IndexError:  # Out of results
                    return

    def dt_search(self, date_string: str, result_count: int = 10):
        """
            Searches the datetime field  (posting date)
        """
        ix = self.ix
        with ix.searcher() as searcher:
            parser = MultifieldParser(["dt"], ix.schema)  # Marking 'default' search field
            myquery = parser.parse(date_string)
            results = searcher.search(myquery)
            for x in range(result_count):
                try:
                    print(results[x])
                except IndexError:  # Out of results
                    return