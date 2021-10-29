from IndexInterface import IndexInterface


class UserParser(object):

    """
        Parses user input. Updates respective variables accompanying a valid escape sequence
        otherwise submits user query string to whoosh.
    """

    def __init__(self):
        # Establishing query interface
        self.qiface = IndexInterface('./datastore.db')
        # Query settings
        self.mode = 'AND'
        self.date_begin: str = '20050101'  # Default is January 2005. This preceeds all posts in the database
        self.date_end: str = '20300101'  # Default is 2030. Obviously beyond all posts in the database
        self.result_count: int = 10

    def print_commands(self):

        print('Enter queries to search the database.')
        print('The escape sequence #! can be used with the following commands to modify the query')
        print('!#mode and - The terms are ANDed in the query')
        print('!#mode or  - The terms are ORed in the query')
        print('!#date_begin  <YYYYMMDD> - Beginning of the desired date range')
        print('!#date_end <YYYYMMDD> - End of the desired date range')
        print('!#results <number> - number of query results to display')
        print('!#all - prints all documents from the database. Lists the total number.')
        print('!#quit')

    def parse_command(self, user_string: str):
        """ Raw string from the user input. Still includes the escape sequence """

        strlen = len(user_string)
        whitespace_list: list = [' ', '\n', '\r']
        command: str = ''
        parameter: str = ''
        for x in range(strlen):
            # Breaking at first sign of whitespace
            if user_string[x] in whitespace_list:
                command = user_string[2:x]
                parameter = user_string[x:].strip()
        # Checking if the command is a single word with no parameter
        if command == '':
            command = user_string[2:]
        self.execute_command(command, parameter)

    def execute_command(self, command: str, parameter: str):
        """
            Runs the command specified by the user.
        """

        valid_commands: dict = {
            'mode': self.update_mode,
            'date_begin': self.update_date_start,
            'date_end': self.update_date_end,
            'results': self.update_result_count,
            'all': self.print_all,
            'quit': self.quit
        }

        if command not in valid_commands:
            print(f"{command} is not a valid command.")
            self.print_commands()

        else:
            valid_commands[command](parameter)

    def update_mode(self, new_mode: str):
        if new_mode == 'or':
            self.mode = 'OR'
            print(f"Mode is now {self.mode}")
        elif new_mode == 'and':
            self.mode = 'AND'
            print(f"Mode is now {self.mode}")
        else:
            print(f"Enter 'or' or 'and', not {new_mode}")

    def update_date_start(self, parameter):
        self.date_begin = parameter
        print(f"Date begin is now {parameter}")

    def update_date_end(self, parameter):
        self.date_end = parameter
        print(f"Date end is now {parameter}")

    def update_result_count(self, parameter):
        try:
            self.result_count = int(parameter)
            print(f'Result count is now {parameter}')
        except ValueError:
            print(f'{parameter} is not a valid value')

    def quit(self, parameter):
        exit(0)

    def print_all(self, parameter):
        all_docs = self.qiface.ix.searcher().documents()
        counter = 0
        for doc in all_docs:
            counter += 1
            print(doc)
        print(f'Document total: {counter}')

    def search(self, search_string):
        self.qiface.search(search_string, self.result_count, self.mode, self.date_begin, self.date_end)


