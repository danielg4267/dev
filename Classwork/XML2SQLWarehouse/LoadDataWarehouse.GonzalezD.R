#############################
#
# Daniel Gonzalez
# CS5200 Summer 2022
# Practicum II: Part II
#
#############################


########################################################
#
#             Initial Setup (Author Facts)
#
########################################################


library(RMySQL)
library(RSQLite)

#Feel free to change these to whatever is needed on your local machine, I use these values throughout the script.
db_user <- 'root'
db_name <- ''
db_password <- ''
db_host <- 'localhost'
db_port <- 3306

#Connect to the original pubmed database created with SQLite
#as well as the MySQL database that will house the authorFacts table and schema.
pubmed_db <- dbConnect(SQLite(), 'pubmed.db')
authorfact_db <- dbConnect(MySQL(), user=db_user, password=db_password, dbname=db_name, host=db_host, port=db_port)
result <- dbSendQuery(authorfact_db, "SET GLOBAL local_infile = true")
dbClearResult(result)
result <- dbSendQuery(authorfact_db, "DROP DATABASE IF EXISTS authorfact_db;")
dbClearResult(result)
result <- dbSendQuery(authorfact_db, "CREATE DATABASE authorfact_db;")
dbClearResult(result)
result <- dbSendQuery(authorfact_db, "USE authorfact_db;")
dbClearResult(result)
result <- dbSendQuery(authorfact_db, "DROP TABLE IF EXISTS authorFacts;")
dbClearResult(result)
result <- dbSendQuery(authorfact_db, "DROP TABLE IF EXISTS journalDim;")
dbClearResult(result)
result <- dbSendQuery(authorfact_db, "DROP TABLE IF EXISTS timeDim;")
dbClearResult(result)
result <- dbSendQuery(authorfact_db, "DROP TABLE IF EXISTS langDim;")
dbClearResult(result)



########################################################
#
#     Create Data Warehouse Schema (Author Facts)
#
########################################################

########################################################
#
#     My star schema contains the authorFacts table,
#     and then additionally you can slice the data
#     by the dimension tables, so number of articles
#     published by journal, by time (month/year/quarter),
#     and by language. I thought that these were logical
#     in imagining some kind of interactive analytic 
#     query program. I also included the number of issues
#     for each journal in the journal dimension table, 
#     as a way to search "number of articles
#     an author published in journals with X amount of 
#     issues".
#
#     The number of coauthors any author has remains the
#     same regardless of how you slice the data, because
#     the value is the number of unique coAuthors across ALL 
#     articles, not number of coauthors per journal or per year 
#     (which, if summed together, would lead to a crazy amount of 
#     repeats and inaccurate numbers). So those only depend on the
#     aid - not very normalized, but it is a star schema!
#     
#     I also did not clean up dates with 00 for month or quarter,
#     because I think the decision on whether to count an issue
#     that was published for the whole year in a query for a specific
#     quarter should be decided in the select statement (ie if you want
#     the number of articles published in quarter 4, SHOULD you include
#     an article that has no quarter date? That should be up to the analyst
#     performing a select query.).
#
########################################################

#Nearly identical to the journal table, but with an extra attribute
#because I thought it'd be useful and interesting. :)
journalDim <- "CREATE TABLE journalDim(
                jid INT,
                issn CHAR(9) NOT NULL,
                title TEXT NOT NULL,
                isoabbr VARCHAR(64) NOT NULL,
                numIssues INT NOT NULL,
                PRIMARY KEY(jid),
                UNIQUE(issn, isoabbr));"

#Time is the only table that doesn't already sort of exist in the 
#original database. This will be a lookup table of all the distinct
#dates in the original database (though of course it could be filled
#with every month/year/quarter from '75 to the present day, if you wanted).
timeDim <- "CREATE TABLE timeDim(
              tid INT,
              month INT NOT NULL,
              year INT NOT NULL,
              quarter INT NOT NULL,
              PRIMARY KEY(tid),
              UNIQUE(month, year));"

#Identical to the original language table, since it is just a lookup table.
langDim <- "CREATE TABLE langDim(
              langid INT,
              lang CHAR(3) NOT NULL,
              PRIMARY KEY(langid),
              UNIQUE(lang));"


#Like all fact tables, the foreign keys and the subject's original primary key
#all together make up the primary key of the fact table, while the rest are
#just facts.
authorFacts <- "CREATE TABLE authorFacts(
                  jid INT,
                  tid INT,
                  langid INT,
                  aid INT,
                  name VARCHAR(64) NOT NULL,
                  numPublications INT NOT NULL,
                  numCoAuthors INT NOT NULL,
                  PRIMARY KEY(jid, tid, langid, aid),
                  FOREIGN KEY(jid) REFERENCES journalDim(jid),
                  FOREIGN KEY(tid) REFERENCES timeDim(tid),
                  FOREIGN KEY(langid) REFERENCES langDim(langid));"


#Send queries to create the tables!
result <- dbSendQuery(authorfact_db, journalDim)
dbClearResult(result)
result <- dbSendQuery(authorfact_db, timeDim)
dbClearResult(result)
result <- dbSendQuery(authorfact_db, langDim)
dbClearResult(result)
result <- dbSendQuery(authorfact_db, authorFacts)
dbClearResult(result)

########################################################
#
#       Fill the Dimension Tables (Author Facts)
#
########################################################

#A relatively simple query that gets all the journals and counts the number of instances
#it has in the journal issues table to get that extra attribute.
journalQuery <- "SELECT journal.jid, issn, title, isoabbr, COUNT(*) AS numIssues FROM journal
                  INNER JOIN journalissue
                  ON (journal.jid = journalissue.jid)
                  GROUP BY journal.jid"
journalDim.df <- dbGetQuery(pubmed_db, journalQuery)

#Bulk write the data to the dimension table
dbWriteTable(conn=authorfact_db, name="journaldim", value=journalDim.df, overwrite=FALSE, append=TRUE, row.names=FALSE)


#This obtains distinct year/month combos (since August 1975 is a different month than
# August 1976). It also calculates the quarter based on the month, sort of going backwards
# from what I did in Part I of this project.
timeQuery <- "SELECT year, month,
(CASE
  WHEN month BETWEEN 1 AND 3
  THEN 1
  WHEN month BETWEEN 4 AND 6
  THEN 2
  WHEN month BETWEEN 7 AND 9
  THEN 3
  WHEN month BETWEEN 10 AND 12
  THEN 4
  ELSE 0
  END)
AS quarter
FROM
(SELECT DISTINCT 
CAST(substr(pubDate, 1, 4) AS INTEGER) AS year, 
CAST(substr(pubDate, 6, 2) AS INTEGER) AS month
FROM journalissue)"

timeDim.df <- dbGetQuery(pubmed_db, timeQuery)
#Create the tid column using rownames, since they are unique values
tid <- rownames(timeDim.df)
timeDim.df <- cbind(tid, timeDim.df)
dbWriteTable(conn=authorfact_db, name="timedim", value=timeDim.df, overwrite=FALSE, append=TRUE, row.names=FALSE)

#Again, identical to the language table.
langQuery <- "SELECT * FROM language"
langDim.df <- dbGetQuery(pubmed_db, langQuery)
dbWriteTable(conn=authorfact_db, name="langdim", value=langDim.df, overwrite=FALSE, append=TRUE, row.names=FALSE)



########################################################
#
#           Computing the Facts (Author Facts)
#
########################################################


#This will be filled with data calculated for each author.
#At this time, they cannot reference tid since that is something
#I calculated outside of the database, but getting the month and year
#will help to do the job later.
authors.df <- data.frame(jid = integer(),
                             langid = integer(),
                             year = integer(),
                             month = integer(),
                             aid = integer(),
                             name = character(),
                             numArticles = integer(),
                             numCoAuthors = integer())



# I will break this down into its subqueries. The first one, coAuthor(aid, numCoAuthors)
# calculates the number of coauthors each author has across ALL articles. This is data
# that cannot be sliced by any of the dimensions, since an author should have the same 
# number of unique coauthors across all articles regardless of whether you're slicing by
# journal or time or language - this is just a precomputed value that will repeat, so it's separate 
# from the rest. It does this by doing an inner join on the authorship table with itself, 
# then counts the unique coauthors it finds for each author.
# The second subquery articleCount(aid, pubDate...) gets the rest of the data that will
# be sliced by the dimension tables, counting the instances of each author that appears
# grouped by all the keys of the dimension tables - since that is how these values are
# calculated and made. 
# Lastly, these two tables are joined together by matching author, and the fact table is
# made. All that will be left is to get a matching tid.
query <- "WITH coAuthor(aid, numCoAuthors) AS
    (SELECT a1.aid, COUNT(DISTINCT a2.aid) FROM authorship AS a1
      INNER JOIN authorship AS a2
      ON (a1.aid != a2.aid AND a1.pmid = a2.pmid)
      GROUP BY a1.aid),
articleCount(aid, pubDate, jid, langid, numPublications, lastName, foreName) AS (
    SELECT author.aid, 
    substr(pubDate, 1, 7) AS pdate, 
    jid, 
    language.langid, 
    COUNT(*) AS numPublications, 
    lastName, foreName
    FROM authorship
    INNER JOIN article
    ON authorship.pmid = article.pmid
    INNER JOIN author
    ON authorship.aid = author.aid
    INNER JOIN journalissue
    ON journalissue.issueid = article.journal
    INNER JOIN articleLanguage
    ON article.pmid = articleLanguage.pmid
    INNER JOIN language
    ON language.langid = articleLanguage.langid
    GROUP BY author.aid, pdate, jid, language.langid)
SELECT jid, 
      langid, 
      CAST(substr(pubDate, 1, 4) AS INT) AS year, 
      CAST(substr(pubDate, 6, 2) AS INT) AS month, 
      articleCount.aid, 
      lastName || ', ' || foreName AS name, 
      numPublications, 
      numCoAuthors 
FROM coAuthor 
INNER JOIN articleCount
ON coAuthor.aid = articleCount.aid"

authors.df <- dbGetQuery(pubmed_db, query)
#Essentially join authors.df with the timeDim.df on year/month, which should be a unique pairing
#in the time dataframe. This will get the tid that corresponds to each date (and there is no need to 
#recalculate quarter!).
temp <- merge(authors.df, timeDim.df, by=c("year", "month"))

#Select the necessary columns from the two joined dataframes, bulk write into the database.
authorFacts.df <- temp[,c("jid", "tid", "langid", "aid", "name", "numPublications", "numCoAuthors")]
dbWriteTable(conn=authorfact_db, name="authorfacts", value=authorFacts.df, overwrite=FALSE, append=TRUE, row.names=FALSE)

#Could potentially do the next part in the same database, but I chose not to as I am cautious with the integrity
#of all the data. Two different schemas, two different databases. Therefore, we're done with this!
dbDisconnect(authorfact_db)

########################################################
#
#               Initial Setup (Journal Facts)
#
########################################################

#Same setup as authorFacts
journalfact_db <- dbConnect(MySQL(), user=db_user, password=db_password, dbname=db_name, host=db_host, port=db_port)
result <- dbSendQuery(journalfact_db, "SET GLOBAL local_infile = true")
dbClearResult(result)
result <- dbSendQuery(journalfact_db, "DROP DATABASE IF EXISTS journalfact_db;")
dbClearResult(result)
result <- dbSendQuery(journalfact_db, "CREATE DATABASE journalfact_db;")
dbClearResult(result)
result <- dbSendQuery(journalfact_db, "USE journalfact_db;")
dbClearResult(result)
result <- dbSendQuery(journalfact_db, "DROP TABLE IF EXISTS journalFacts;")
dbClearResult(result)
result <- dbSendQuery(journalfact_db, "DROP TABLE IF EXISTS timeDim;")
dbClearResult(result)


########################################################
#
#     Create Data Warehouse Schema (Journal Facts)
#
########################################################

########################################################
#
#     This star schema is much simpler - it can only
#     be sliced by time. Obviously there will be many
#     repeat values for number of articles per ___, as
#     journal 1 may have published something 10 times in 
#     the same year, and obviously the total number of articles
#     they published within that year does not change, only 
#     month and maybe quarter. The way these values are set up,
#     summing all the months of one quarter will add up to the 
#     number of articles per quarter, and summing all the values
#     per quarter will get the value per year, etc. There really
#     is no need to sum any of the values unless you're looking for
#     something specific like number of articles published in "August and
#     December" - all the calculations have been done.
#
#     In addition, I did not clean up dates like 1975-00-00,
#     because I think analysis of those depends upon the user
#     of the data. I think the best way to make use of those
#     is to treat them as a "wild card" of sorts. For example,
#     number of articles published in quarter 4 of 1975 should
#     include all dates with quarter 4 1975, but it should also 
#     include dates with quarter 0 of 1975, since that was the only
#     issue of a journal published that year. This is something that should
#     be stated in the select statement, though. Doing it this way
#     will allow an analyst to decide whether or not to include it,
#     if they so choose. I think this decision grants the most
#     flexibility of dates.
#
########################################################

#Identical to the timeDim table in authorfact_db
timeDim <- "CREATE TABLE timeDim(
              tid INT,
              month INT NOT NULL,
              year INT NOT NULL,
              quarter INT NOT NULL,
              PRIMARY KEY(tid),
              UNIQUE(month, year));"

journalFacts <- "CREATE TABLE journalFacts(
              jid INT,
              tid INT,
              title TEXT NOT NULL,
              issn CHAR(9) NOT NULL,
              isoabbr VARCHAR(64) NOT NULL,
              numArticlesPerMonth INT NOT NULL,
              numArticlesPerQuarter INT NOT NULL,
              numArticlesPerYear INT NOT NULL,
              PRIMARY KEY(jid, tid),
              FOREIGN KEY(tid) REFERENCES timedim(tid));"

result <- dbSendQuery(journalfact_db, timeDim)
dbClearResult(result)
result <- dbSendQuery(journalfact_db, journalFacts)
dbClearResult(result)


########################################################
#
#       Fill the Dimension Tables (Journal Facts)
#
########################################################


#Only one dimension table, and it is the exact same as the 
#one in the author fact database. But I run the query again,
#for the sake of consistency and integrity of data for a different
#database.
timeQuery <- "SELECT year, month,
(CASE
  WHEN month BETWEEN 1 AND 3
  THEN 1
  WHEN month BETWEEN 4 AND 6
  THEN 2
  WHEN month BETWEEN 7 AND 9
  THEN 3
  WHEN month BETWEEN 10 AND 12
  THEN 4
  ELSE 0
  END)
AS quarter
FROM
(SELECT DISTINCT 
CAST(substr(pubDate, 1, 4) AS INTEGER) AS year, 
CAST(substr(pubDate, 6, 2) AS INTEGER) AS month
FROM journalissue)"

timeDim.df <- dbGetQuery(pubmed_db, timeQuery)
tid <- rownames(timeDim.df)
timeDim.df <- cbind(tid, timeDim.df)
dbWriteTable(conn=journalfact_db, name="timedim", value=timeDim.df, overwrite=FALSE, append=TRUE, row.names=FALSE)

########################################################
#
#         Computing the Facts (Journal Facts)
#
########################################################


#I will again break this into subqueries. The first one, monthly(jid, title...) joins
#with journalissue and article, then groups by the journal and month, aggregating with a
#COUNT(*). The second, quarterly(jid, quarter...) does the same, but gets calculates the quarter
#instead of using the month. Both of these are paired with year, since quarter 4 1975 is not the same
#as quarter 4 1976. The last, yearly(jid, year...) does the same but does it by year. Finally, all three
#of these are joined by jid *in addition* to the date, to make sure that each date has the correct article counts
#and the correct quarter, month, and year.
journalQuery <- "WITH monthly(jid, title, issn, isoabbr, month, numArticlesPerMonth) AS (
SELECT journal.jid, 
journal.title, 
issn, 
isoabbr, 
substr(pubDate, 1, 7) AS month, 
COUNT(*) AS numArticlesPerMonth 
FROM journalissue
INNER JOIN article
ON article.journal = journalissue.issueid
INNER JOIN journal
ON journal.jid = journalissue.jid
GROUP BY journal.jid, month
),
quarterly(jid, quarter, _date, numArticlesPerQuarter) AS
  (SELECT journal.jid, 
  (CASE
    WHEN CAST(substr(pubDate, 6, 2) AS INT) BETWEEN 1 AND 3
      THEN substr(pubDate, 1, 5) || '01'
    WHEN CAST(substr(pubDate, 6, 2) AS INT) BETWEEN 4 AND 6
      THEN substr(pubDate, 1, 5) || '02'
    WHEN CAST(substr(pubDate, 6, 2) AS INT) BETWEEN 7 AND 9
      THEN substr(pubDate, 1, 5) || '03'
    WHEN CAST(substr(pubDate, 6, 2) AS INT) BETWEEN 10 AND 12
      THEN substr(pubDate, 1, 5) || '04'
    ELSE substr(pubDate, 1, 5) || '00'
    END) AS quarter, 
    substr(pubDate, 1, 7) AS _date,
    COUNT(*) AS numArticlesPerQuarter 
  FROM journalissue
  INNER JOIN article
  ON article.journal = journalissue.issueid
  INNER JOIN journal
  ON journal.jid = journalissue.jid
  GROUP BY journal.jid, quarter),
yearly(jid, year, _date, numArticlesPerYear) AS (
  SELECT journal.jid, 
  substr(pubDate, 1, 4) AS year, 
  substr(pubDate, 1, 7) AS _date, 
  COUNT(*) AS numArticlesPerYear 
  FROM
  journalissue
  INNER JOIN article
  ON article.journal = journalissue.issueid
  INNER JOIN journal
  ON journal.jid = journalissue.jid
  GROUP BY journal.jid, year
)
SELECT monthly.jid, 
CAST(substr(month, 6, 2) AS INT) AS month, 
CAST(substr(year, 1, 4) AS INT) AS year, 
CAST(substr(quarter, 6, 2) AS INT) AS quarter, 
title, 
issn, 
isoabbr,
numArticlesPerMonth, 
numArticlesPerQuarter, 
numArticlesPerYear
FROM monthly 
INNER JOIN quarterly
ON monthly.jid = quarterly.jid AND monthly.month = quarterly._date
INNER JOIN yearly
ON quarterly.jid = yearly.jid AND quarterly._date = yearly._date"

#Send the query, will create one big dataframe like authors.df did
journals.df <- dbGetQuery(pubmed_db, journalQuery)

#Same as the authorFacts, I need to identify the tid and then select the necessary columns.
temp <- merge(journals.df, timeDim.df, by=c("month", "year", "quarter"))
journalFact.df <- temp[,c("jid", "tid", "title", "issn", "isoabbr", "numArticlesPerMonth", "numArticlesPerQuarter", "numArticlesPerYear")]
dbWriteTable(conn=journalfact_db, name="journalfacts", value=journalFact.df, overwrite=FALSE, append=TRUE, row.names=FALSE)

#Done with both!
dbDisconnect(journalfact_db)
dbDisconnect(pubmed_db)
