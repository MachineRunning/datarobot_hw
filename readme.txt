Overview:
So the python script "extract_google_predictions.py" is 
fairly straight forward.

Login, select the prediction API and the trained models 
associated with the project.

Read out-of-sample data from a csv file and sample it 
(saving the indices) and write out the predictions to a csv file.
--------------------------------------------------------
Some of the hardcoded inputs:
Authentication requires two things: an OAuth service 
email account and a P12 key (.p12 file).


The choice of API is hard coded for "prediction API v1.6"
 but until this point the script could be used for any google API.
 
Then the script just follows the "Overview" above.

*****************************************************
Datasets:
Out of sample data was hourly electrical data from 2014.
--------------------------------------------------------
1st data set: Two years of hourly data (Jan-2012 to Dec-2013) 
consisting of: "campusLoad","dayNumber","matchHour","temps","dewpt","wkendFlag","holidayDummy","monthDummy"

campusLoad: integer ranging from ~30k to ~70k [kWh] measured from the campus power plant Abbott 
dayNumber: 1,2,3, ... , 365   day of year from 1 to 365
matchHour 0,1,2, ... , 23    hour in 24 hour clock
temps: hourly temperatures reported from KCMI (Savoy Willard Airport) 
dewpt: hourly dew point reported from KCMI (Savoy Willard Airport) 
wkendFlag: 0 - weekday, 1 - weekend
holidayDummy: 0,1,2,3 significant campus holidays
monthDummy: 0,1,2, ... , 11 included because GMDH identified a small monthly dependence

--------------------------------------------------------
2nd data set: only hour=15 (~3pm selected) of 1st data set
--------------------------------------------------------
The 3rd data set is the same data as the 1st except with different variables.
3rd data set: "campusLoad","temps","dewpt","wkendFlag","holidayDummy","monthDummy" 
+48 lagged vectors each of (“campusLoad”,“cooling degree hour”,”heating degree hour”)
by 48 lagged vectors I mean campusLoad was lagged up to 48 hours and each lag was 
used as model input, cooling degree hour and heating degree hour were also lagged 48 hours each.

cooling degree hour - if hourly_temp>55: cdh=temp-55
heating degree hour - if hourly_temp=<55: hdh=55-temp

--------------------------------------------------------

4th data set: synthetic linear model (from R)
first a line is created using y.start=4x-7 for x=1:1000
then y.start is perturbed using sampling from a Guassian distribution
y=y.start + rnorm(1000 draws, sd=500)

so the input csv is y,x where x is from 1:1000