Database Access

1. Install PostgreSQL.
2. In Log Analysis Project directory, unzip newsdata.zip
3. In terminal, change directory to root folder of Log Analysis.
4. Run "psql -d news -f newsdata.sql" to load data.
5. To access data, run "psql -d news"

Running Log Analysis script
1. In terminal, change directory to root folder of Log Analysis.
2. Run "python logsanalysis.py"

Results
1. top_three: This function will return the top 3 article titles in descending order and views.
2. author_popularity: This function will return the top authors in descending order and the the views of articles written by the author.
3. errors: This function will return request leads errors over 1%. ('404 NOT FOUND')/('404 NOT FOUND + 200 OK') grouped by day.
