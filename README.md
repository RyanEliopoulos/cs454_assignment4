<h1> Data</h1>

The SQLite database contains additional information not used to construct the whoosh index.
The structure of the database was essentially a crude index whose purpose is made superfluous by Whoosh. 
The historical data was omitted since that information is independent of the user posts. 


<b>Whoosh schema</b>

title=TEXT(stored=True), <br>
content=TEXT(stored=True),<br>
author=TEXT(stored=True), <br>
permalink=STORED, <br>
timestamp=NUMERIC(stored=True))


<b> SQLITE schema </b>

Table: wsb_posts <br>

post_id TEXT NOT NULL PRIMARY KEY, <br>
post_title TEXT NOT NULL,<br>
post_content TEXT,<br>
author TEXT NOT NULL,<br>
author_fullname TEXT NOT NULL,<br>
permalink TEXT NOT NULL,<br>
url TEXT NOT NULL,<br>
timestamp REAL NOT NULL<br>
 

