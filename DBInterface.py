import sqlite3


class DBInterface:

    def __init__(self, db_path: str):
        # Establishing database connection
        self.db_path: str = db_path
        self.db_connection: sqlite3.Connection = sqlite3.connect(self.db_path, 10)
        self.db_connection.row_factory = sqlite3.Row  # Allows accessing column by name
        self.db_cursor: sqlite3.Cursor = self.db_connection.cursor()
        # Mandating foreign key constraint enforcement
        self._execute_query('PRAGMA foreign_keys = 1')

    def _execute_query(self,
                       sql_string: str,
                       parameters: tuple = None) -> tuple[int, dict]:
        """ Wrapper for cursor.execute """
        try:
            if parameters is None:
                self.db_cursor.execute(sql_string)
            else:
                self.db_cursor.execute(sql_string, parameters)
            return 0, {'success_mesage': 'Successfully executed query'}
        except sqlite3.Error as e:
            return -1, {'error_message': str(e)}

    def manual(self):
        """
            Debug fnx for manually manipulating the databse
        """
        sqlstring = """
                        SELECT * FROM
                        wsb_posts
                   """

        ret = self._execute_query(sqlstring)
        if ret[0] != 0:
            print("Problem running manual control")
            print(ret)
            exit(1)

        results = self.db_cursor.fetchall()
        return 0, {'content': results}

        # self.db_connection.commit()

    def pull_table(self, table: str) -> tuple[int, dict]:
        sqlstring: str = f""" SELECT * FROM  {table}"""
        ret = self._execute_query(sqlstring)
        if ret[0] != 0:
            return ret
        results: list = self.db_cursor.fetchall()
        return 0, {'content': results}

    def seed_db(self) -> tuple[int, dict]:
        """ Responsible for initializing the database according to the desired schema.
            Will drop existing tables for fresh restart.
        """
        # Resetting existing db
        db_tables = [
            'historical_data',
            'wsb_posts',
            'symbol_post_junction',
            'stock_symbols',  # e.g. AAPL, TSLA
        ]
        for table in db_tables:
            sqlstring = f""" DROP TABLE IF EXISTS {table}"""
            ret = self._execute_query(sqlstring)
            if ret[0] != 0:
                print(f'Error dropping SQL table {table}')
                print(ret)
                exit(1)

        sqlstring = """ CREATE TABLE stock_symbols ( stock_symbol TEXT NOT NULL PRIMARY KEY,
                                                     corp_name TEXT NOT NULL )
                    """
        ret = self._execute_query(sqlstring)
        if ret[0] != 0:
            # Error
            return ret
        # Date is a UNIX timestamp
        sqlstring = """ CREATE TABLE historical_data (
                            stock_symbol TEXT NOT NULL,
                            date INTEGER NOT NULL,
                            open REAL NOT NULL,
                            close REAL NOT NULL,
                            high REAL NOT NULL,
                            low REAL NOT NULL,
                            volume INTEGER,
                            FOREIGN KEY(stock_symbol) REFERENCES stock_symbols(stock_symbol)
                        )
                    """
        ret = self._execute_query(sqlstring)
        if ret[0] != 0:
            return ret

        # The URL can be an image, an article on some other website,
        # or a self referential string of the complete URL.
        """
        
            Author fullname is the reddit-encoded value.
            Author is as would appear on the website.   
        
        """
        sqlstring = """ CREATE TABLE wsb_posts (
                            post_id TEXT NOT NULL PRIMARY KEY,
                            post_title TEXT NOT NULL,
                            post_content TEXT,
                            author TEXT NOT NULL,
                            author_fullname TEXT NOT NULL,
                            permalink TEXT NOT NULL,
                            url TEXT NOT NULL,
                            timestamp REAL NOT NULL
                        )
                    """
        ret = self._execute_query(sqlstring)
        if ret[0] != 0:
            return ret
        sqlstring = """ CREATE TABLE symbol_post_junction (
                            post_id TEXT NOT NULL,
                            stock_symbol TEXT NOT NULL,
                            PRIMARY KEY (post_id, stock_symbol),
                            FOREIGN KEY(post_id) REFERENCES wsb_posts,
                            FOREIGN KEY(stock_symbol) REFERENCES stock_symbols
                            )
                    """
        ret = self._execute_query(sqlstring)
        if ret[0] != 0:
            return ret

        self.db_connection.commit()
        return 0, {'success_message': 'Successfully seeded db'}

    def insert_symbol(self,
                      stock_symbol: str,
                      corp_name: str) -> tuple[int, dict]:
        sqlstring = """ INSERT INTO stock_symbols
                        VALUES (?, ?)
                    """
        ret = self._execute_query(sqlstring,
                                  (stock_symbol, corp_name))
        if ret[0] == 0:
            self.db_connection.commit()
        return ret

    def populate_data(self,
                      stock_symbol: str,
                      date: float,
                      open_price: float,
                      close_price: float,
                      high_price: float,
                      low_price: float,
                      volume: int) -> tuple[int, dict]:
        """ Inserts historical data rows for the given stock symbol """

        sqlstring: str = """ INSERT INTO historical_data
                             VALUES (?, ?, ?, ?, ?, ?, ?)
                         """
        ret = self._execute_query(sqlstring, (stock_symbol,
                                              date,
                                              open_price,
                                              close_price,
                                              high_price,
                                              low_price,
                                              volume))
        if ret[0] == 0:
            self.db_connection.commit()
        return ret

    def naked_symbols(self) -> tuple[int, dict]:
        """ Returns stock symbols for which no data exists in the historical_data table """
        sqlstring = """ SELECT * FROM stock_symbols ss
                        WHERE ss.stock_symbol not in (SELECT stock_symbol FROM historical_data)
                    """
        ret = self._execute_query(sqlstring)
        if ret[0] != 0:
            return ret
        results: list = self.db_cursor.fetchall()
        symbol_list: list = []
        for row in results:
            symbol_list.append(row['stock_symbol'])
        return 0, {'content': symbol_list}

    def symbol_list(self) -> tuple[int, dict]:
        """ Returns the list of stock symbols """

        sqlstring: str = """ SELECT * FROM stock_symbols
                         """
        ret = self._execute_query(sqlstring)
        if ret[0] != 0:
            return ret
        results: list = self.db_cursor.fetchall()
        symbol_list: list = []
        for row in results:
            symbol_list.append(row['stock_symbol'])
        return 0, {'content': symbol_list}

    def prune_symbol(self, symbol: str) -> tuple[int, dict]:
        """ Removes all information pertaining to the given stock from the database.

            Database schema requires this order:

        """
        # Database schema requires this order
        #   1) symbol_post_junction
        #   2) historical data
        #   3) stock_symbols

        sqlstring: str = """ DELETE FROM symbol_post_junction
                             WHERE stock_symbol = (?)
                         """

        ret = self._execute_query(sqlstring, (symbol,))
        if ret[0] != 0:
            return ret

        # historical data
        sqlstring = """ DELETE FROM historical_data
                        WHERE stock_symbol = (?)
                    """
        ret = self._execute_query(sqlstring, (symbol,))
        if ret[0] != 0:
            return ret

        # stock_symbols
        sqlstring: str = """ DELETE FROM stock_symbols
                             WHERE stock_symbol = (?)
                         """
        ret = self._execute_query(sqlstring, (symbol,))
        if ret[0] == 0:
            self.db_connection.commit()
        return ret

    def insert_post(self, post: dict) -> tuple[int, dict]:
        """


        post: {
            'id': <>,
            'title': <>,
            'selftext': <>,
            'author': <>,
            'author_fullname': <>,
            'permalink': <>,
            'url': <>
        }
        :param post:
        :return:
        """

        # Staging info for db insertion
        post_id: str = post['id']
        post_title: str = post['title']
        post_content: str = post['selftext']
        author: str = post['author']
        author_fullname: str = post['author_fullname']
        permalink: str = post['permalink']
        url: str = post['url']
        timestamp: float = post['timestamp']
        sqlstring: str = """ INSERT INTO wsb_posts
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """
        ret = self._execute_query(sqlstring, (post_id,
                                              post_title,
                                              post_content,
                                              author,
                                              author_fullname,
                                              permalink,
                                              url,
                                              timestamp))
        if ret[0] != 0:
            return ret

        included_symbols: list = post['included_symbols']
        for symbol in included_symbols:
            sqlstring = """ INSERT INTO symbol_post_junction
                            VALUES (?, ?)
                        """
            ret = self._execute_query(sqlstring, (post_id,
                                                  symbol))
            if ret[0] != 0:
                return -1, {'error_message': f'Failed to update symbol for post {post_id} {post_title}: {ret[1]}'}
        # Successfully added all post elements to the database
        self.db_connection.commit()
        return 0, {'success_message': f'Post {post_id} successfully commited to the database'}

    def pshiftCreate(self):
        """
            UNUSED. This route schema was abandoned.

        :return:
        """
        sqlstring: str = """ CREATE TABLE pshift_posts (
                                post_id TEXT NOT NULL PRIMARY KEY,
                                stock_symbol TEXT NOT NULL,
                                title TEXT NOT NULL ,
                                selftext TEXT NOT NULL)
                            """
        ret = self._execute_query(sqlstring,)

        if ret[0] != 0:
            print(f'Error trying to create pshift table: ${ret}')

        self.db_connection.commit()
        return ret

    def pshiftInsert(self,
                     id: str,
                     title: str,
                     selftext: str,
                     stock_symbol: str):
        """
            UNUSED. This route schema was abandoned.
        """

        sqlstring: str = """ INSERT INTO pshift_posts
                             VALUES (?, ?, ?, ?)
                         """
        ret = self._execute_query(sqlstring, (id,
                                              title,
                                              selftext,
                                              stock_symbol))
        if ret[0] != 0:
            print(f'Encountered error inserting into pshift table: ${ret}')
        self.db_connection.commit()
        return ret

