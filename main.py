"""

     post_id TEXT NOT NULL PRIMARY KEY,                     Stored not indexed
                            post_title TEXT NOT NULL,       indexed
                            post_content TEXT,              indexed
                            author TEXT NOT NULL,           indexed
                            author_fullname TEXT NOT NULL,  stored not indexed
                            permalink TEXT NOT NULL,        stored not indexed
                            url TEXT NOT NULL,              ignore this; don't need
                            timestamp REAL NOT NULL         stored but not indexed.



    I don't need a junction table since with whoosh I can just use the search to find the appropriate posts.


    Posts span January 2020
"""

from Controller import Controller
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh.fields import *
from whoosh import index
import os
from DBInterface import DBInterface


# This stuff is for creating the index

# schema = Schema(title=TEXT(stored=True),
#                 content=TEXT(stored=True),
#                 author=TEXT(stored=True),
#                 permalink=STORED,
#                 timestamp=NUMERIC(stored=True))
#
# if not os.path.exists('indexdir'):
#     os.mkdir('indexdir')
#
#
# ix = index.create_in('indexdir', schema)
# writer = ix.writer()
#
# db = DBInterface('./datastore.db')
# ret = db.manual()
# if ret[0] != 0:
#     print(ret)
#     exit()
#
# rows = ret[1]['content']
#
# for row in rows:
#
#     writer.add_document(
#         title=row['post_title'],
#         content=row['post_content'],
#         author=row['author'],
#         permalink=row['permalink'],
#         timestamp=row['timestamp'],
#
#     )
#
# ret = writer.commit()
# print(ret)
#
#
# # Now for querying the index
# ix = open_dir('indexdir')
#
# with ix.searcher() as searcher:
#     parser = QueryParser("content", ix.schema)
#     myquery = parser.parse("microsoft")
#     results = searcher.search(myquery)
#
#     for value in results:
#         print(value)



cnt = Controller('./datastore.db')
cnt.search('title:bezos AND dt:[20200122 to 20200123]')
# cnt.dt_search('20200112')  # year month day


# for result in results:
#





