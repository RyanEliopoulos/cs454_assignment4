<h1> Data</h1>

The SQLite database contains additional information not used to construct the whoosh index.
The structure of the database was essentially a crude index whose purpose is made superfluous by Whoosh. 
The historical data was omitted since that information is independent of the user posts and hopefully can
be used to pre render images. Stock symbols were also omitted since those will likely be parsed
before submitting the query string to whoosh anyway in order to prepare the respective prerendered assets. <br><br>

For simplicity the data only includes posts made in the month of January 2020. This amounts to 6907 tuples.
<br><br>


<b>Whoosh schema</b> <br>
The program will attempt to open the directory "indexdir" and will create one if it doesn't exist.

title=TEXT(stored=True), <br>
content=TEXT(stored=True),<br>
author=TEXT(stored=True), <br>
permalink=STORED, <br>
dt=DATETIME(stored=True)) <br>

The first three fields represent the data of primary interest. A preview of the posts will be used on the results page. 
Author may be removed in the future pending determined value. <br>
The permalink will be used to reconstruct the URL linking to the OP. The preview will be hyperlinked<br>
The dt (datetime) field facilitates date range filtering.  Storing it might not be necessary but better safe than sorry.



<b> SQLITE schema </b> <br>
This is the information original pulled for assignment 1.

Table: wsb_posts <br>

post_id TEXT NOT NULL PRIMARY KEY, <br>
post_title TEXT NOT NULL,<br>
post_content TEXT,<br>
author TEXT NOT NULL,<br>
author_fullname TEXT NOT NULL,<br>
permalink TEXT NOT NULL,<br>
url TEXT NOT NULL,<br>
timestamp REAL NOT NULL<br>
 

<h1> Program</h1> <br>
The program operates within an interactive session. There are commands the user may issue to the program when preceeded
by the two-character escape sequence "!#".  

- !#mode <or, and>  
- !#date_begin \<yyyymmdd\>
- !#date_end \<yyyymmdd\>
- !#results \<integer\>  (updates the number of results displayed per query)
- !#all   (This prints all documents in the database and the count)
- !#quit

The default mode is "and". The default date ranges go from 2005 to 2030 just so the encompass all possible values.
User input is taken to be a standard query in the absence of the escape sequence. The results will be printed to screen.
