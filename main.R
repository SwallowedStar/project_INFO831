donnees<- read.csv("restaurant.csv", header = TRUE)
restau_dataframe <- as.data.frame(donnees)
restau_dataframe<- replace(restau_dataframe, is.na(restau_dataframe), 0)
restau_dataframe<- na.omit(restau_dataframe)
#print(restau_dataframe)

rating<-restau_dataframe$rating
rating2<-as.numeric(rating)

rating2<- replace(rating2, is.na(rating2), 0)



nb_reviews<- restau_dataframe$nbreviews
nb_reviews2<-as.numeric(nb_reviews)
nb_reviews2<- replace(nb_reviews2, is.na(nb_reviews2), 0)


model<-lm(nb_reviews2~rating2,restau_dataframe)


summa<-summary(model)


plot(nb_reviews2~rating2)
print(summa)

