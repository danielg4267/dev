#############################
#
# Daniel Gonzalez
# CS5200 Summer 2022
# Practicum II: Part I
#
# Runs in ~12 minutes on my computer.
#
#############################

########################################################
#
#                 SQL Setup
#
########################################################


#Initial Setup - Connect to DB, enable foreign keys, drop any potentially existing tables
library(RSQLite)
library(XML)
#I check if some strings are integers later on. Sometimes they are not, and this gives a warning
#Best turn it off for 30000 articles...
options(warn=-1) 
pubmed_db <- dbConnect(SQLite(), 'pubmed.db')
result <- dbSendQuery(pubmed_db, 'PRAGMA foreign_keys = ON;')
dbClearResult(result)
result <- dbSendQuery(pubmed_db, 'DROP TABLE IF EXISTS articlelanguage')
dbClearResult(result)
result <- dbSendQuery(pubmed_db, 'DROP TABLE IF EXISTS authorship')
dbClearResult(result)
result <- dbSendQuery(pubmed_db, 'DROP TABLE IF EXISTS author')
dbClearResult(result)
result <- dbSendQuery(pubmed_db, 'DROP TABLE IF EXISTS article')
dbClearResult(result)
result <- dbSendQuery(pubmed_db, 'DROP TABLE IF EXISTS journalissue')
dbClearResult(result)
result <- dbSendQuery(pubmed_db, 'DROP TABLE IF EXISTS journal')
dbClearResult(result)
result <- dbSendQuery(pubmed_db, 'DROP TABLE IF EXISTS language')
dbClearResult(result)

#Queries to set up each table

#A simple lookup table for languages, langid is a synthetic key
language <- "CREATE TABLE language(
              langid INTEGER PRIMARY KEY AUTOINCREMENT,
              lang CHAR(3) UNIQUE NOT NULL
              );"

#aid is a synthetic primary key
#valid will act as a boolean, INT instead of 'Y' 'N' like in the XML file
#names/initials are saved as they are. There is no other way to identify
#an author, so the combination of the three should be unique, even though
#it is entirely possible that two people have the same name in real life.
author <- "CREATE TABLE author(
              aid INTEGER PRIMARY KEY AUTOINCREMENT,
              valid INT,
              lastName VARCHAR(32) DEFAULT 'UNKNOWN' NOT NULL,
              foreName VARCHAR(32) DEFAULT 'UNKNOWN' NOT NULL,
              initials VARCHAR(8) DEFAULT 'UNKNOWN' NOT NULL
              CHECK(0 <= valid AND valid <= 1),
              UNIQUE(lastName, foreName, initials)
              );"

#jid is a synthetic key
#issn should always exist in the database, and is given a default 'unknown' value
#issnType should also be 'unknown' for cases it does not exist, rather than NULL
#title is text because they can be extremely long
#isoabbr is VARCHAR(64) as there is no real standard on how long/short it should be

#I believe ISSN to be a defining feature in which journal one is looking at, along with
#its title (as some journals don't have an ISSN). I think it is entirely possible 
#that two journals have the same name, and while this might not be the case in this XML file,
#it is a real life example of something that could happen. In addition, I think being able to 
#distinguish between publishing an article in a journal's online version vs its print version
#is necessary, especially since they have very different values for many attributes computed in parts 2 and 3,
#and if needed you can easily compute what you need by grouping by title instead of
#jid. Therefore, the combination of issn and isoabbr (title can be very long, slow to check, isoabbr
#is just as unique but shorter) should be made unique as the distinguishing feature of a journal,
#not simply its title.
journal <- "CREATE TABLE journal(
              jid INTEGER PRIMARY KEY AUTOINCREMENT,
              issn CHAR(9) DEFAULT '0000-0000' NOT NULL,
              issnType VARCHAR(16) DEFAULT 'UNKNOWN' NOT NULL,
              title TEXT NOT NULL,
              isoabbr VARCHAR(64) NOT NULL,
              UNIQUE(issn, isoabbr)
              );"


#issueid is a synthetic key
#jid references the journal that the issue is a part of
#pubDate is simply a date(I go into more detail about this in the helper function section)
#citedMedium should always be included, even if unknown, since it is so common
# The defining characteristic of a journal issue is the journal it is published in,
# and the issue *date* that it was released. Volume and Issue are inconsistent values,
# with numbers ranging anywhere for 1 to 250+, sometimes not existing, sometimes not having 
# numbers for values, sometimes only having one or the other. I assumed them to be part of
# a journal's internal identification system of what issue it was, ie rather than saying
# "Our September 2020 release", something like "Our 3-4.5 PT 6 Release". So volume and
# issue are saved as characters. If needed, one could cast them to integer and if it
# is one, it can be used correctly, otherwise it will be 0, which is what I would've done to 
# begin with anyway, had they been more consistent values.
journalissue <- "CREATE TABLE journalissue(
              issueid INTEGER PRIMARY KEY AUTOINCREMENT,
              jid INT NOT NULL,
              volume VARCHAR(8) DEFAULT 'NULL' NOT NULL,
              issue VARCHAR(8) DEFAULT 'NULL' NOT NULL,
              pubDate DATE DEFAULT '0000-00-00' NOT NULL,
              citedMedium VARCHAR(16) DEFAULT 'UNKNOWN' NOT NULL,
              FOREIGN KEY (jid) REFERENCES journal(jid)
              UNIQUE(jid, pubDate)
              );"

#pmid is the id from the XML file for each article
#journal references journal ISSUE that this was published in, not the journal itself
#title can be very long and is saved as TEXT
#aulist_complete is a boolean, 0 for false, 1 for true, NULL for n/a. It is 
#taken from each article's "AuthorList CompleteYN" value
article <- "CREATE TABLE article(
              pmid INT NOT NULL,
              journal INT NOT NULL,
              title TEXT DEFAULT 'UNKNOWN' NOT NULL,
              aulist_complete INT,
              PRIMARY KEY(pmid),
              FOREIGN KEY (journal) REFERENCES journalissue(issueid)
              CHECK (0 <= aulist_complete AND aulist_complete <= 1)
              );"

#This table is to facilitate a many-to-many relationship
#while keeping the schema normalized. It is essentially each
#article's author list. pmid references the article, aid references the author.
authorship <- "CREATE TABLE authorship(
              pmid INT NOT NULL,
              aid INT DEFAULT 0 NOT NULL,
              PRIMARY KEY(pmid, aid),
              FOREIGN KEY (pmid) REFERENCES article(pmid),
              FOREIGN KEY (aid) REFERENCES author(aid)
              );"

#Articles can have multiple languages, and so similar to above, this is
#to facilitate a many-to-many relationship, this time with article pmid
#and language langid.
articlelanguage <- "CREATE TABLE articlelanguage(
                    pmid INT NOT NULL,
                    langid INT DEFAULT 0 NOT NULL,
                    PRIMARY KEY(pmid, langid),
                    FOREIGN KEY(pmid) REFERENCES article(pmid),
                    FOREIGN KEY(langid) REFERENCES language(langid)
                    );"


#Send each query to create the tables
result <- dbSendQuery(pubmed_db, language)
dbClearResult(result)
result <- dbSendQuery(pubmed_db, author)
dbClearResult(result)
result <- dbSendQuery(pubmed_db, journal)
dbClearResult(result)
result <-dbSendQuery(pubmed_db, journalissue)
dbClearResult(result)
result <- dbSendQuery(pubmed_db, article)
dbClearResult(result)
result <- dbSendQuery(pubmed_db, authorship)
dbClearResult(result)
result <- dbSendQuery(pubmed_db, articlelanguage)
dbClearResult(result)


########################################################
#
#                 XML Preparation
#
########################################################

#Parse file, get root and size of tree
xmlDoc <- xmlParse("./pubmed-tfm-xml/pubmed22n0001-tf.xml") 
xmlTree <- xmlRoot(xmlDoc)
numArticles <- xmlSize(xmlTree)

#Dataframes to be used intermediately before writing to the SQL database
#They all follow the SQL schema very closely
language.df <- data.frame(langid = integer(),
                       lang = character())


author.df <- data.frame(aid = integer(),
                        valid = integer(),
                        lastName = character(),
                        foreName = character(),
                        initials = character()
                        )

authorship.df <- data.frame(pmid = integer(),
                         aid = integer())

journal.df <- data.frame(
                      jid = integer(),
                      issn = character(),
                      issnType = character(),
                      title = character(),
                      isoabbr = character())

journalissue.df <- data.frame(issueid = integer(),
                              jid = integer(),
                           volume = character(),
                           issue = character(),
                           pubDate = character(),
                           citedMedium = character())

articlelanguage.df <- data.frame(pmid = integer(),
                                langid = integer())

article.df <- data.frame(pmid = integer(),
                      journal = integer(),
                      title = character(),
                      aulist_complete = integer())

#These three environment variables will be used as hashtables for quick lookups
#to determine if an author, journal, or issue has already been added to the dataframe
#without having to iterate through the entire dataframes above. Doing so with language
#is also a choice, but there aren't nearly as many languages in this XML file (or the world)
#as there are authors or journals.
authorHash <- new.env(hash=TRUE)
journalHash <- new.env(hash=TRUE)
journalIssueHash <- new.env(hash=TRUE)

########################################################
#
#                 HELPER FUNCTIONS
#
########################################################

#Takes a Journal node, checks by combination of issn and isoabbr if it is in the dataframe,
#adds it if not, then returns the jid.
processJournal <- function(journalNode){
  
  #Check if it has an ISSN
  issn <- xpathSApply(journalNode, "./ISSN", xmlValue)
  issnType <- "NULL"
  if(length(issn) == 0){
    issn <- "0000-0000"
  }
  else{
    issnType <- xmlGetAttr(journalNode[[1]], "IssnType")
  }
  #Every journal has one, and it's not as lengthy as the title can be, but just as informative and unique
  #This element makes a good value to hash with (along with the ISSN as the combo may differ!)
  isoabbr <- xpathSApply(journalNode, "./ISOAbbreviation", xmlValue)
  journal <- paste(issn, isoabbr, sep="")
  jid <- journalHash[[journal]]
  
  #Add to the dataframe and the hash
  if(is.null(jid)){
    jid <- nrow(journal.df) + 1
    title <- xpathSApply(journalNode, "./Title", xmlValue)
    journal.df[jid,] <<- list(jid, issn, issnType, title, isoabbr)
    journalHash[[journal]] <<- jid
    
  }
  
  return(jid)
}

# Each journal issue has at least a year. Some have a month OR quarter (season).
# Some also have a day. In order to save as much data as possible, quarters
# will be converted to a month, and unknown months/days will be stored as 00 values.
# This way they can all be saved as the normal date format, 0000-00-00, regardless of 
# how much or how little data they have.
convertDate <- function(dateNode){
  
  #Default value for a date
  year <- "0000"
  month <- "00"
  day <- "00"
  defaults <- c(year, month, day)
  #will be filled with values to check and replace defaults
  date.lst <- list()

  #Check if it's a medline date first, it is split by spaces
  medLineDate <- xpathSApply(dateNode, "./MedlineDate", xmlValue)
  if(length(medLineDate) > 0){
    date.lst <- strsplit(medLineDate, " ")[[1]]
  }
  else{
    #date list is all xmlNode values Year, Month/Season, Day
    numNodes <- xmlSize(dateNode)
    for(i in 1:numNodes){
      date.lst <- c(date.lst, xmlValue(dateNode[[i]]))
    }
  }
  
  #Many are in a range, eg 'Mar-Apr'. This splits along the dash, removes potential whitespace 
  #and chooses the first in the range
  for(i in 1:length(date.lst)){
    date.lst[[i]] <- gsub(" ", "", strsplit(date.lst[[i]], "-")[[1]][1], fixed = TRUE)
  }
  #Make sure we have 3 potential dates to evaluate
  while(length(date.lst) < length(defaults)){
    date.lst <- c(date.lst, defaults[[length(date.lst) + 1]])
  }
  
  #PROCESS YEAR
  #It's a number and it is 4 digits long (2 digit years are too ambiguous!)
  if( !(is.na(as.integer(date.lst[[1]])) | nchar(date.lst[[1]]) != 4) ){
    year <- date.lst[[1]]
  }
  #PROCESS MONTH/SEASON
  #it is either a month 'Mmm' or a season
  if(is.na(as.integer(date.lst[[2]]))){
    
    month.str <- switch(date.lst[[2]],
                        "Summer" = "Jul",
                        "Fall" = "Oct",
                        "Winter" = "Jan",
                        "Spring" = "Apr",
                        date.lst[[2]])
    month.str <- paste(toupper(substring(month.str, 1, 1)),
                       tolower(substring(month.str, 2, nchar(month.str))),
                       sep = "")
    
    
    temp <- sprintf("%02d", match(month.str, month.abb))
    if(temp != "NA"){month <- temp}
  }
  #it is a number like '04' for April, and it's within a valid range
  else if ( !(as.integer(date.lst[[2]]) < 1 | 12 < as.integer(date.lst[[2]])) ){
    month <- sprintf("%02d", as.integer(date.lst[[2]]))
  }
  
  #PROCESS DAY
  #it is a number
  if( !is.na(as.integer(date.lst[[3]])) ){
    day <- sprintf("%02d", as.integer(date.lst[[3]]))
  }
  date <- paste(year, month, day, sep="-")
  return(date)
  
}



#Takes everything in the Journal tag, creates a JournalIssue
#tuple that references the right entry in the Journal dataframe,
#and returns the issueid (not jid!) for use in adding an article.
processJournalIssue <- function(journalNode){
  
  #get an issn (whether it exists already or not)
  jid <- processJournal(journalNode)
  issn <- journal.df[jid,]$issn
  pubDate <- convertDate(xpathSApply(journalNode, "./JournalIssue/PubDate")[[1]])
  #Combination of ISSN and date hash to get an issueid
  j.issue <- paste(issn, pubDate, sep="")
  issueid <- journalIssueHash[[j.issue]]
  
  #Get the values in the node, add it to the dataframe and add issueid to the hashtable
  if(is.null(issueid)){
    issueid <- nrow(journalissue.df) + 1
    volume <- xpathSApply(journalNode, "./JournalIssue/Volume", xmlValue)
    issue <- xpathSApply(journalNode, "./JournalIssue/Issue", xmlValue)
    #Did not exist, default values
    if(length(volume) == 0){
      volume <- "NULL"
    }
    if(length(issue) == 0){
      issue <- "NULL"
    }
    citedMedium <- xpathSApply(journalNode, "./JournalIssue/@CitedMedium")
    journalissue.df[issueid,] <<- list(issueid, jid, volume, issue, pubDate, citedMedium)
    journalIssueHash[[j.issue]] <<- issueid
    
  }
  return(issueid)
  
}

#Takes the value from language and checks if it exists
#in the dataframe before adding it. Returns the id of the language
processLanguage <- function(languageString){
  
  #already exists, should only return 1 since this conditional prevents duplicates
  if(any(language.df$lang == languageString)){
    return(language.df[language.df$lang==languageString,]$langid)
  }
  #add to dataframe
  else{
    row <- nrow(language.df) + 1
    language.df[row,]$langid <<- row
    #make sure it's 3 characters!
    language.df[row,]$lang <<- tolower(substr(languageString, 1, 3))
    return(row)
  }
}

#Takes the node for one author, checks if it exists, then adds
#it to the dataframe. Returns the row number it is in.
processAuthor <- function(authorNode){
  
  #Some authors only have parts of a name - this ensures
  #they have default values and this doesn't go out of bounds
  author.names <- c("UNKNOWN", "UNKNOWN", "UNKN")
  names <- xmlSize(authorNode)
  for(i in 1:names){
    author.names[i] <- xmlValue(authorNode[[i]])
  }
  
  
  #a tuple that should be unique to each author
  #order is always the same in an XML file
  lastname <- author.names[[1]]
  forename <- author.names[[2]]
  initials <- author.names[[3]]
  
  #Full name/initials is used to hash since it should be unique
  author.str <- paste(lastname, forename, initials, sep="")
  aid <- authorHash[[author.str]]

  #Get the other values, add to the dataframe and hashtable
  if(is.null(aid)){
    aid <- nrow(author.df) + 1
    validyn.str <- xmlGetAttr(authorNode, "ValidYN")
    validyn <- switch(validyn.str,
                      "Y" = 1,
                      "N" = 0,
                      NA)
    author <- list(aid, validyn, lastname, forename, initials)
    author.df[aid,] <<- author
    authorHash[[author.str]] <<- aid 
  }
  
  return(aid)
  
}

#Iterates through the authors in an AuthorList node, 
#processes them with the processAuthor function, then 
#adds the author with the pmid provided to the authorship
#table.
processAuthorList <- function(pmid, authorlistNode){
  
  
  #Get each author
  for(i in 1:xmlSize(authorlistNode)){
    aid <- processAuthor(authorlistNode[[i]])
    
    #No repeats!
    if(any(authorship.df[authorship.df$pmid==pmid,]$aid == aid)){
      next
    }
    
    #Add it to the list!
    authorship.df[nrow(authorship.df) + 1,] <<- c(pmid, aid)
  }
  
}

########################################################
#
#       Iterate Through xmlTree and Add Articles
#
########################################################

#For-loop to iterate through every node, and uses the helper functions
#to get every referenced value from other dataframes.
for(i in 1:numArticles){
  
  node <- xmlTree[[i]]
  
  #Default values (0 for lang will be added as a sentinel later)
  lang <- 0
  aulist_complete <- NA
  
  journalNode <- xpathSApply(node, "./Article/Journal")
  if(length(journalNode) == 0){
    next #Don't care about articles that aren't in journals
  }
  
  journal <- processJournalIssue(journalNode[[1]])
  pmid <- as.integer(xmlGetAttr(node, "PMID")) 
  title <- xpathSApply(node, "./Article/ArticleTitle", xmlValue)
  
  #Some articles don't have an authorlist, check that it does before
  #processing it
  authorListNode <- xpathSApply(node, "./Article/AuthorList")
  if(length(authorListNode) > 0){
    completeyn <- xmlGetAttr(authorListNode[[1]], "CompleteYN")
    aulist_complete <- switch(completeyn,
                         "Y" = 1,
                         "N" = 0,
                         NA)
    processAuthorList(pmid, authorListNode[[1]])
  }
  
  #Some articles don't have a language, check before processing
  languages <- xpathSApply(node, "./Article/Language", xmlValue)
  if(length(languages) > 0){
    #articles can have multiple languages 
    for(j in 1:length(languages)){
      lang <- processLanguage(languages[[j]])
      articlelanguage.df[nrow(articlelanguage.df) + 1,] <- c(pmid, lang)
    }
  }

  #Add to dataframe
  article <- list(pmid, journal, title, aulist_complete)
  article.df[nrow(article.df)+1,] <- article

}

########################################################
#
#               Writing to SQL Database
#
########################################################

#A very clear null value for language, if it wasn't included
language.sentinel <- "INSERT INTO language 
                                  (langid, lang)
                                VALUES
                                  (0, 'NUL')"

result <- dbSendQuery(pubmed_db, language.sentinel)
dbClearResult(result)

#Bulk write the dataframes into the SQL database
dbWriteTable(conn=pubmed_db, name="language", value=language.df, overwrite=FALSE, append=TRUE, row.names=FALSE)
dbWriteTable(conn=pubmed_db, name="author", value=author.df, overwrite=FALSE, append=TRUE, row.names=FALSE)
dbWriteTable(conn=pubmed_db, name="journal", value=journal.df, overwrite=FALSE, append=TRUE, row.names=FALSE)
dbWriteTable(conn=pubmed_db, name="journalissue", value=journalissue.df, overwrite=FALSE, append=TRUE, row.names=FALSE)
dbWriteTable(conn=pubmed_db, name="article", value=article.df, overwrite=FALSE, append=TRUE, row.names=FALSE)
dbWriteTable(conn=pubmed_db, name="authorship", value=authorship.df, overwrite=FALSE, append=TRUE, row.names=FALSE)
dbWriteTable(conn=pubmed_db, name="articlelanguage", value=articlelanguage.df, overwrite=FALSE, append=TRUE, row.names=FALSE)

#We're done!
dbDisconnect(pubmed_db)