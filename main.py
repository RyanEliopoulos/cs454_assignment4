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

from UserParser import UserParser
from IndexInterface import IndexInterface


if __name__ == "__main__":
    ...
    userparser = UserParser()
    userparser.print_commands()

    while True:
        user_string = input()
        if user_string[:2] == '!#':  # Special command
            userparser.parse_command(user_string)
        else:
            # print(f"Date begin is {userparser.date_begin}")
            # print(f"Date end is {userparser.date_end}")
            # print(f"mode is {userparser.mode}")

            userparser.search(user_string)





    # cnt = IndexInterface('./datastore.db')
    # cnt.testing_search('title:bezos OR dt:[20200122 to 20200123]')


# cnt.dt_search('20200112')  # year month day
# cnt.search('msft amzn', mode='AND')
# all_docs = cnt.ix.searcher().documents()
# cnt.testing_search('hello bezos')






