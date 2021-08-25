import pandas as pd

"""
        This script will automagically generate a nice little report for LinkedIn
        Data exports. Starting with just messages, since I'm particularly interested
        in how many messages per month / year I've gotten. But will later analysis
        some other data that is provided, such as:
        
        - Invitations
        - Contacts
        - Connections
        - Profile
        - Recommendations
"""

"""
    As of 8/25/2021, this is what the LinkedIn messages.csv export file looks like:
    CONVERSATION ID, CONVERSATION TITLE, FROM, SENDER PROFILE, URL, TO, DATE, SUBJECT, CONTENT, FOLDER

    (Note: it's actually tabbed based and not comma based, but commas are easier for displaying here)

    I want to filter by FROM on unique values, and generate a count of unique senders.
    Then I want to filter that down by month and year.
"""

# the fields we care about
fields = ["FROM", "DATE"]

# Messages.csv is the default export name for LinkedIn Messages
messagesDF = pd.read_csv("messages.csv", usecols=fields)

# Debug - what's df look like?
#print(messagesDF)

# Filter for unique senders
messagesDF = messagesDF.drop_duplicates(subset = ["FROM"])

# Debug - what's df look like?
#print(messagesDF)
#messagesDF.info()

# Convert the "DATE" column from a string(object) to a datetime,
# so we can use groupbys later
messagesDF["DATE"] = pd.to_datetime(messagesDF["DATE"])

#print(messagesDF.head())
#print(messagesDF)

#messagesDF.info()

#messagesDF["DATE"] = messagesDF["DATE"].astype('datetime64[ns]')

# Report should be something like:
# Message Count
# July, 2021: 200
# August, 2021: 300
# etc

# Group by months
# This seemed to cause errors, so just going to do it manually with a loop.
# Only ~500 rows at the moment so probably fine and just as fast as whatever
# pandas does under the hood.
#monthsDF = messagesDF["DATE"].groupby(pd.Grouper(freq="M"))
#print(monthsDF)

#monthsDF = messagesDF["DATE"].resample("M", how='sum')

# Dictionary for ezpz printing
mapDates = {}


# Might be cool to group by year as well
mapYearDates = {}


# Pandas dataframe for exporting back to CSV
exportedDF = pd.DataFrame(columns = ["YEAR", "MONTH", "COUNT"])

# Group it ourselves based on year and month.
for index, row in messagesDF.iterrows():
    #print(row["DATE"], row["FROM"])
    #print(str(row["DATE"]).split("-"))

    # Split the date, then we can group by YEAR_MONTH
    dateSplit = str(row["DATE"]).split("-")
    datePart = dateSplit[0] + "_" + dateSplit[1]

    # See if the given YEAR_MONTH is inside our map.
    if datePart in mapDates:
        mapDates[datePart] += 1

    else:
        mapDates[datePart] = 1

    # Also check the mapYearDates one too for YEAR : Count
    yearDatePart = dateSplit[0]
    if yearDatePart in mapYearDates:
        mapYearDates[yearDatePart] += 1
    else:
        mapYearDates[yearDatePart] = 1

# Generate pandas Dataframe to export back to CSV for later looking
for date in sorted(mapDates):
    dateSplit = date.split("_")

    exportedDF = exportedDF.append({'YEAR': dateSplit[0], 'MONTH': dateSplit[1], 'COUNT': mapDates[date]}, ignore_index=True)


# Now mapDates should have a nice count for us!
# Let's pretty print it and sort it too
print("YEAR_MONTH: COUNT")
for date in sorted(mapDates):
    print(date + ": " + str(mapDates[date]))

print("\n")

# Also print YEAR: Count too
print("YEAR: COUNT")
for year in sorted(mapYearDates):
    print(year + ": " + str(mapYearDates[year]))

# What's inside exportedDF?
# Looks good! Export it to CSV now.
#print(exportedDF)

exportedDF.to_csv('messages_analyzed.csv', sep=',')


