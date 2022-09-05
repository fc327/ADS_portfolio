#Final Project
#Clayton Monroe, Farahin Choudhury, Leigh Sausville, Patrick Bush, Destiny McDaniel

library(tidyverse)
library(ggplot2)
library(lubridate)

#Import Datasets
library(readxl)
May2019 <- read_excel("201905-citibike-tripdata.xlsx")
June2019 <- read_excel("201906-citibike-tripdata.xlsx")
July2019 <- read_excel("201907-citibike-tripdata.xlsx")
May2020 <- read_excel("202005-citibike-tripdata.xlsx")
June2020 <- read_excel("202006-citibike-tripdata.xlsx")
July2020 <- read_excel("202007-citibike-tripdata.xlsx")

#Convert to Tibble for Easier Data Cleaning
May2019 <- as_tibble(May2019)
June2019 <- as_tibble(June2019)
July2019 <- as_tibble(July2019)
May2020 <- as_tibble(May2020)
June2020 <- as_tibble(June2020)
July2020 <- as_tibble(July2020)

#Breaking Down Time Column
May2019$month <- month(May2019$starttime)
May2019$day <- day(May2019$starttime)
May2019$hour <- hour(May2019$starttime)

June2019$month <- month(June2019$starttime)
June2019$day <- day(June2019$starttime)
June2019$hour <- hour(June2019$starttime)
July2019$month <- month(July2019$starttime)
July2019$day <- day(July2019$starttime)
July2019$hour <- hour(July2019$starttime)
May2020$month <- month(May2020$starttime)
May2020$day <- day(May2020$starttime)
May2020$hour <- hour(May2020$starttime)
June2020$month <- month(June2020$starttime)
June2020$day <- day(June2020$starttime)
June2020$hour <- hour(June2020$starttime)
July2020$month <- month(July2020$starttime)
July2020$day <- day(July2020$starttime)
July2020$hour <- hour(July2020$starttime)

#Converting Trip Duration from Seconds to Minutes
May2019$tripduration <- May2019$tripduration/60
June2019$tripduration <- June2019$tripduration/60
July2019$tripduration <- July2019$tripduration/60
May2020$tripduration <- May2020$tripduration/60
June2020$tripduration <- June2020$tripduration/60
July2020$tripduration <- July2020$tripduration/60

#Bind Data Frames for Cumulative Statistics
Trips2019 <- rbind(May2019,June2019,July2019)
Trips2020 <- rbind(May2020,June2020,July2020)
AllTrips <- rbind(May2019,June2019,July2019,May2020,June2020,July2020)

#Analyzing Trips by Start Time in 2019 vs 2020; bargraphs
Trips2019$hour <- as.numeric(Trips2019$hour)
ggplot(Trips2019) + geom_bar(aes(x=hour))

Trips2020$hour <- as_numeric(Trips2020$hour)
ggplot(Trips2020) + geom_bar(aes(x=hour, bins=24))

#fix for time of day issue

dummydf <- tibble(Trips2019$month,Trips2019$day,Trips2019$hour)
colnames(dummydf) <- c("month", "day", "hour")
dummydf <- subset(dummydf, hour!="0")
ggplot(dummydf) + geom_bar(aes(x=hour))

#Paired T-Test

duration <- tibble(Trips2019$tripduration, Trips2020$tripduration)
colnames(duration) <- c("Trips2019","Trips2020")
(mean(duration$Trips2019))  #18.21656
(mean(duration$Trips2020))  #28.50186
t.test(duration$Trips2019,duration$Trips2020,mu=0, alt="two.sided",paired=T, conf.level=0.95)

#Analyzing User Type 
Trips2019$usertype <- as_factor(Trips2019$usertype) #Converting usertype to factor
Trips2020$usertype <- as_factor(Trips2020$usertype)

length(which(Trips2019$usertype=="Subscriber")) #2,630,915
length(which(Trips2019$usertype=="Customer")) #514,810
2630915 + 514810 #3,145,725
2330915/3145725 #74.1%
ridership2019 <- data.frame(
  group=c("Subscribers","Customers"),
  value=c(.741,.259))
ggplot(ridership2019, aes(x="", y=value, fill=group)) + geom_bar(stat="identity", width=1,color="white") + coord_polar("y", start=0) + theme_void()

length(which(Trips2020$usertype=="Subscriber")) #2,205,402
length(which(Trips2020$usertype=="Customer")) #940,323
2205402 + 940323 #3,145,725
2205402/3145725 #70.1%
ridership2020 <- data.frame(
  group=c("Subscribers","Customers"),
  value=c(.701,.299))
ggplot(ridership2020, aes(x="", y=value, fill=group)) + geom_bar(stat="identity", width=1,color="white") + coord_polar("y", start=0) + theme_void()


#Prepping for Regression
##Correcting Birth Year Issue

birthyears <- as_tibble(Trips2020)
unique(birthyears$`birth year`)
as.numeric(birthyears$`birth year`)
as.factor(birthyears$`birth year`)
birthyears <- filter(birthyears, birthyears$`birth year` > 1930 & birthyears$`birth year`!= 1969)
length(which(birthyears$`birth year`==1968))
length(which(birthyears$`birth year`==1969))
birthyears2019 <- as_tibble(Trips2020)
birthyears2019 <- filter(birthyears2019, birthyears2019$`birth year`> 1930 & birthyears2019$`birth year` != 1969)

#Plotting Trips By Birth Year
ggplot(birthyears) + geom_bar(aes(x=birthyears$`birth year')) + xlab("Birth Year") + ylab("Trips") + ggtitle("Trips by Birth Year 2020") +theme_bw()
ggplot(birthyears2019) + geom_bar(aes(x=birthyears2019$`birth year`)) + xlab("Birth Year") + ylab("Trips") + ggtitle("Trips by Birth Year 2019") + theme(bw)

#Filtering Out Bad Start Time Data
Trips2019 <- as_tibble(Trips2019)
Trips2020 <- as_tibble(Trips2020)

timeofday2019 <- Trips2019
timeofday2020 <- Trips2020

timeofday2019 <- filter(timeofday2019, timeofday2019$hour > 0)
timeofday2020 <- filter(timeofday2020, timeofday2020$hour > 0)

timeofday2019$hour <- as.factor(timeofday2019$hour)
timeofday2020$hour <- as.factor(timeofday2020$hour)

#Plotting Start Time Data
options(scipen = 999) #removing scientific notation from y-axis
ggplot(timeofday2019) + geom_bar(aes(x=timeofday2019$hour, fill="pink")) + xlab("Starting Hour") + ylab ("# of Trips") + ggtitle("2019") + theme_bw()
ggplot(timeofday2020) + geom_bar(aes(x=timeofday2020$hour, fill="pink")) + xlab("Starting Hour") + ylab ("# of Trips") + ggtitle("2020") + theme_bw()


#maps
library(ggmap)
register_google(key="AIzaSyArmXApqhrGh44IhowQoUub6XohkZc0qfE")


#ggmap(get_map("New York, NY", zoom=11)) + geom_point(mapping=aes()


#Changing Station Names to Factor
Trips2019$`end station name` <- as.factor(Trips2019$`end station name`)


Destinations2019 <- Trips2019 %>%
  group_by(Trips2019$`end station name`) %>%
  tally


Destinations2019 <- Destinations2019[order(-Destinations2019$n),]


#BaseMap
qmap("Union Square Holiday Market", zoom=11)
nyc_map <- get_map("Union Square Holiday Market", zoom=13)
ggmap(nyc_map)

#Calling Stations to Get Their Lat/Lon using view()
PershingSquareNorth2019 <- filter(Trips2019, Trips2019$`end station name`=="Pershing Square North")
#Lon -73.97771   #Lat 40.75187

WestStChambersSt2019 <- filter(Trips2019, Trips2019$`end station name`=="West St & Chambers St")
#Lon -74.01322 #Lat 40.71755

E17Broadway2019 <- filter(Trips2019, Trips2019$`end station name`=="E 17 St & Broadway")
#Lon  -73.99009 #Lat 40.73705

Dest12AveW402019 <- filter(Trips2019, Trips2019$`end station name`=="12 Ave & W 40 St")
#Long -74.00278 #Lat 40.76088

BroadwayE222019 <- filter(Trips2019, Trips2019$`end station name`=="Broadway & E 22 St")
# -73.98955 # 40.74034

BroadwayE14thSt2019 <- filter(Trips2019, Trips2019$`end station name`=="Broadway & E 14 St")
# -73.99074 # 40.73455

EighthAve2019 <- filter(Trips2019, Trips2019$`end station name`=="8 Ave & W 31 St")
# -73.99468 # 40.75059

BroadwayW602019 <- filter(Trips2019, Trips2019$`end station name`=="Broadway & W 60 St")
# -73.98192 # 40.76916

Christopher2019 <- filter(Trips2019, Trips2019$`end station name`=="Christopher St & Greenwich St")
# -74.00711  # 40.73292

West20112019 <- filter(Trips2019, Trips2019$`end station name`=="W 20 St & 11 Ave")
# -74.00776 # 40.74674

HotLon2019 <- c(-73.97771,-74.01322,-73.99009,-74.00278,-73.98955,-73.99074,-73.99468,-73.98192,-74.00711,-74.00776)

HotLat2019 <- c(40.75187,40.71755,40.73705,40.76088,40.74034,40.73455,40.75059,40.76916,40.73292,40.74674)
Names2019 <- c("Pershing Square North","West St & Chambers St","E 17 St & Broadway", "12 Ave & W 40 St", "Broadway & E 22 St","Broadway & E 14 St","8 Ave & W 31 St","Broadway & W 60 St","Christopher St & Greenwich St", "W 20 St & 11 Ave")

geotest <- data.frame(Names2019,HotLon2019,HotLat2019)

ggmap(nyc_map) + geom_point(data=geotest, aes(x=HotLon2019,y=HotLat2019),size=1.5)

#2020 Map
Trips2020$`end station name` <- as.factor(Trips2020$`end station name`)


Destinations2020 <- Trips2020 %>%
  group_by(Trips2020$`end station name`) %>%
  tally

Destinations2020 <- Destinations2020[order(-Destinations2020$n),]

TwelthAve2020 <- filter(Trips2020, Trips2020$`end station name`=="12 Ave & W 40 St")
# -74.00278 # 40.76088
WestChambers2020 <- filter(Trips2020, Trips2020$`end station name`=="West St & Chambers St")
# -74.01322 # 40.71755
FirstAve2020 <- filter(Trips2020, Trips2020$`end station name`=="1 Ave & E 68 St")
# -73.95818 40.76501
BroadwayW602020 <- filter(Trips2020, Trips2020$`end station name`=="Broadway & W 60 St")
 # -73.98192 # 40.76916
Pier40 <- filter(Trips2020, Trips2020$`end station name`=="Pier 40 - Hudson River Park")
# -74.0113 # 40.72771
Christopher2020 <- filter(Trips2020, Trips2020$`end station name`=="Christopher St & Greenwich St")
# -74.00711  # 40.73292
CentralPark <- filter(Trips2020, Trips2020$`end station name`=="Central Park S & 6 Ave")
# -73.97634 # 40.76591
South5 <- filter(Trips2020, Trips2020$`end station name`=="S 5 Pl & S 5 St")
# -73.96088 #40.71045
West2020 <- filter(Trips2020, Trips2020$`end station name`=="West St & Liberty St")
# -74.01485 #40.71144
East13 <- filter(Trips2020, Trips2020$`end station name`=="E 13 St & Avenue A")
#-73.98068 #40.72967
Names2020 <- c("12 Ave & W 40 St","West St & Chambers St","1 Ave & E 68 St","Broadway & W 60 St","Pier 40 - Hudson River Park","Christopher St & Greenwich St","Central Park S & 6 Ave","S 5 Pl & S 5 St","West St & Liberty St","E 13 St & Avenue A")
HotLon2020 <- c(-74.00278,-74.01322,-73.95818,-73.98192,-74.0113,-74.00711,-73.97634,-73.96088,-74.01485,-73.98068)
HotLat2020 <- c(40.76088,40.71755,40.76501,40.76916,40.72771,40.73292,40.76591,40.71045,40.71144,40.72967)
geotest2 <- data.frame(Names2020,HotLon2020,HotLat2020)
ggmap(nyc_map) + geom_point(data=geotest2, aes(x=HotLon2020,y=HotLat2020),size=1.5)



#Building Trip Duration by Month Viz
MonthlyDurationMeans <- c(mean(May2019$tripduration),mean(June2019$tripduration),mean(July2019$tripduration),mean(May2020$tripduration), mean(June2020$tripduration),mean(July2020$tripduration))
MonthlyDurationMeans
monthsxaxis <- factor(c("May 2019", "June 2019", "July 2019","May 2020","June 2020","July 2020"))
x2 <- data.frame(monthsxaxis,MonthlyDurationMeans)
x2

ggplot(x2, aes(x=monthsxaxis, y=MonthlyDurationMeans)) + geom_col(color = "black", fill="pink") + xlab("Month") + ylab("Avg Trip in Minutes") + scale_x_discrete(limits = c("May 2019", "June 2019", "July 2019","May 2020","June 2020","July 2020"))
