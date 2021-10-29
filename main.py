"""

     post_id TEXT NOT NULL PRIMARY KEY,                     Stored not indexed
                            post_title TEXT NOT NULL,       indexed
                            post_content TEXT,              indexed
                            author TEXT NOT NULL,           indexed
                            author_fullname TEXT NOT NULL,  stored not indexed
                            permalink TEXT NOT NULL,        stored not indexed
                            url TEXT NOT NULL,              ignore this; don't need
                            timestamp REAL NOT NULL         stored but not indexed.




"""

from UserParser import UserParser


if __name__ == "__main__":
    userparser = UserParser()
    userparser.print_commands()

    while True:
        user_string = input()
        if user_string[:2] == '!#':  # Escape sequence
            userparser.parse_command(user_string)
        else:
            userparser.search(user_string)







