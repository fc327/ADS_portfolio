#hotel reviews project 

# we have more than half a million observations in this data set 
# all hotels are located in Europe and the coordinates are hard-coded 
# reviews are from 2015-2018

library(ggplot2)
library(ggtext)
library(ggmap)
library(arules)
library(arulesViz)
library(cluster)
library(tidyverse)
library(dplyr)
library(sqldf)
library(stats)
library(e1071)
library(rpart)
library(wordcloud)
library(quanteda)
library(lattice)
library(corpus)

# register_google(key= "AIzaSyCupTRDySQasDgiOx5bp9zCSmjd1S3dVUk", write = TRUE)

#working directory set to Desktop --> setwd("~/Desktop")
hotelreviews <- read.csv(file = "~/Desktop/HotelReviews.csv")
navalues <- which(!complete.cases(hotelreviews))
fullhotelreviews <- hotelreviews[-navalues,]
length(which(!complete.cases(fullhotelreviews)))

#colnames(hotelreviews)
#changing some of the column names 

fullhotelreviews$Hotel_Name <- as.factor(fullhotelreviews$Hotel_Name)
fullhotelreviews$Tags <- as.factor(fullhotelreviews$Tags)

mean(fullhotelreviews[1:100,13]) # takes the average of the 1st 100 values in the 13th column, which is the Reviewer_Score
mean(fullhotelreviews$Reviewer_Score, na.rm = TRUE)

summary(fullhotelreviews$Review_Total_Negative_Word_Counts) #descriptive stats on negative reviews
summary(fullhotelreviews$Review_Total_Positive_Word_Counts) #descriptive stats on positive reviews

fullhotelreviews$lat <- as.factor(fullhotelreviews$lat)
fullhotelreviews$lng <- as.factor(fullhotelreviews$lng)

# using the str_count command to count the number of words in each review
# \\w+ matches non-word characters
str_count(fullhotelreviews$Negative_Review[1], '\\w+')
str_count(fullhotelreviews$Positive_Review[1], '\\w+')

str_count(fullhotelreviews$Tags[1], '\\w+') # this counts the number of elements in each set of tags 

# exploring the data
length(unique(fullhotelreviews$Hotel_Name)) #1493 different properties
unique(fullhotelreviews$Reviewer_Nationality) #227 total different countries/nationalities 
summary(fullhotelreviews$Reviewer_Score) # description of scores by reviewer
summary(fullhotelreviews$Average_Score) # description of average scores (per hotel)
max(fullhotelreviews$Average_Score) #avg per property
min(fullhotelreviews$Average_Score) # avg per property 


unique(fullhotelreviews$Hotel_Name)
unique(fullhotelreviews[fullhotelreviews$Average_Score >6.5,]) # find records where the average score is greater than 6.5
fullhotelreviews$Reviewer_Nationality <- tolower(fullhotelreviews$Reviewer_Nationality) # to use with ggplot/ggmap
#prop.table(table(hotelreviews$Hotel_Name))

# how many total reviews per hotel? 
length(unique(fullhotelreviews$Total_Number_of_Reviews))
length(which(fullhotelreviews$Negative_Review == "No Negative")) # records where there is no negative review provided from the reviewer
length(which(fullhotelreviews$Positive_Review == "No Positive")) # records where there is no positive reivew provided from the reviewer

# examples of different hotels 
#addresses were found via their indexes in the dataset: "hotelreviews$Hotel_Address[100]", etc
length(which(fullhotelreviews$Hotel_Address == "1 2 Serjeant s Inn Fleet Street City of London London EC4Y 1LL United Kingdom"))
length(which(fullhotelreviews$Hotel_Address == "1 15 Templeton Place Earl s Court Kensington and Chelsea London SW5 9NB United Kingdom"))
length(which(fullhotelreviews$Hotel_Address == "1 Addington Street Lambeth London SE1 7RY United Kingdom"))
length(which(fullhotelreviews$Hotel_Address == "1 Inverness Terrace Westminster Borough London W2 3JP United Kingdom"))

length(which(fullhotelreviews$Hotel_Name == "The Drayton Court Hotel"))
length(which(fullhotelreviews$Hotel_Name == "Thistle Kensington Gardens"))
length(which(fullhotelreviews$Hotel_Name == "Zenit Borrell"))

# location of most popular hotel (by name and address)
# location of least popular hotel (by name and address)
# key words for positive/negative words in 'Tags' column 

# tags associated with most popular hotel (based on average score)
unique(sort(fullhotelreviews$Average_Score))
fullhotelreviews[fullhotelreviews$Average_Score == 9.8,]

# tags associated with least popular hotel (based on average score)
min(fullhotelreviews$Average_Score) 
fullhotelreviews[fullhotelreviews$Average_Score == 5.2,]

max(fullhotelreviews$Reviewer_Score)
min(fullhotelreviews$Reviewer_Score)

max(sqldf("select Reviewer_Score from fullhotelreviews where Hotel_Name = 'Hotel Arena'"))
min(sqldf("select Reviewer_Score from fullhotelreviews where Hotel_Name = 'Hotel Arena'"))


hist(fullhotelreviews$Average_Score)
hist(fullhotelreviews$Reviewer_Score)
mean(fullhotelreviews$Review_Total_Negative_Word_Counts)
mean(fullhotelreviews$Review_Total_Positive_Word_Counts)

#ggplot should be used to map out the hotel locations

fullhotelreviews %>%
  ggplot(aes(Hotel_Name, Total_Number_of_Reviews_Reviewer_Has_Given)) +
  geom_point(alpha = 0.5, aes(size = Reviewer_Score, color = Reviewer_Score)) +
  theme_bw() +
  labs(title="Hotel Ratings")

fullhotelreviews %>%
  ggplot(aes(Reviewer_Score, Average_Score)) + 
  geom_point(aes(color = Total_Number_of_Reviews , size = Average_Score),
             alpha = 0.5)

fullhotelreviews %>%
  ggplot(aes(Hotel_Name, Reviewer_Score, fill = Reviewer_Score)) + 
  geom_bar(alpha = 0.5) +
  labs(x = "Hotels", y = "Ratings", title = "Hotels in Europe")

length(fullhotelreviews$Reviewer_Nationality == "United States")

# association rule mining with ratings data (Reviewer_Score)
summary(fullhotelreviews)

mean(fullhotelreviews$Reviewer_Score)
mean(fullhotelreviews$Average_Score)
mean(fullhotelreviews$Review_Total_Negative_Word_Counts)
mean(fullhotelreviews$Review_Total_Positive_Word_Counts)

fullhotelreviews$Reviewer_Score <- cut(fullhotelreviews$Reviewer_Score, breaks = c(0,2,4,6,8,10),
                   labels = c("terrible", "below average", "average",
                              "above average", "exceptional"),
                   right = FALSE)

hoteltransactions <- as(fullhotelreviews, "transactions")
#transactionInfo(hoteltransactions)[["transactionID"]] <- tid_hotels

rules <- apriori(hoteltransactions, parameter = list(supp = 0.005, conf = 0.8))
options(digits = 3)
inspect(rules[100:105])
rules <- sort(rules, by = "confidence", decreasing = TRUE)

plot(fullhotelreviews$Average_Score, fullhotelreviews$Reviewer_Score)
plot(rules[1:10], method = "graph", engine = "interactive", shading = NA)


