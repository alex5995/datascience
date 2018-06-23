#importo i 3 dataset
feat <- read.csv("~/decision_models/retail-data-analytics/Features data set.csv")
sales <- read.csv("~/decision_models/retail-data-analytics/sales data-set.csv")
stores <- read.csv("~/decision_models/retail-data-analytics/stores data-set.csv")

#aggrego sales perchè ho le info su tutti i dipartimenti e io vorrei solo quelle aggregate per store
sales.ok <- aggregate(sales$Weekly_Sales, by = list(sales$Store, sales$Date, sales$IsHoliday), FUN="sum")
names(sales.ok) <- c("Store", "Date", "IsHoliday", "Weekly_Sales")

#mergio i dateset
d <- merge(sales.ok, feat, by = c("Store", "Date", "IsHoliday"))
d <- merge(d, stores, by = "Store")

#trasformo le date da factor al formato "date"
d$Date <- as.Date(d$Date, "%d/%m/%Y")

#creo un vettore con le info esclusivamente sulle date e sulle vacanze
hol <- unique(d[,c("Date","IsHoliday")])

#inizializzo dei vettori
d$BeforeHoliday <- FALSE
d$AfterHoliday <- FALSE

#vado a riempieri correttamenti i vettori "BeforeHoliday" e "AfterHoliday"
for (i in 1:nrow(hol)){
  x <- hol[i,] #preso l'i-sima data
  before <- x[1] - 7 #settimana prima
  after <- x[1] + 7 #settimana dopo
  if (length(unique(d$Date == before))==2){ #eseguo solo se ho selezionato almeno una riga
    d[d$Date == before,]$BeforeHoliday <- rep(x[2], sum(d$Date == before)) #imposto a TRUE le oss. selezionate per la colonna before
  }
  if (length(unique(d$Date == after))==2){ #eseguo solo se ho selezionato almeno una riga
    d[d$Date == after,]$AfterHoliday <- rep(x[2], sum(d$Date == after)) #imposto a TRUE le oss. selezionate per la colonna after
  }
}

sum(d$BeforeHoliday == TRUE) == sum(d$IsHoliday == TRUE) #tutto ok
sum(d$AfterHoliday == TRUE) == sum(d$IsHoliday == TRUE) #tutto ok

d$IsHoliday <- as.character(d$IsHoliday) #uniformo la colonna al dataset
d$BeforeHoliday <- as.character(d$BeforeHoliday) #uniformo la colonna al dataset
d$AfterHoliday <- as.character(d$AfterHoliday) #uniformo la colonna al dataset

rm(after, before, feat, sales, sales.ok, stores, x, i, hol)

#-------------------------------------------------
#-------------------------------------------------
#-------------------------------------------------

d1 <- d[d$Date > "2011-11-10",] #considero solo gli anni con gli sconti

d1$Weekly_Sales <- d1$Weekly_Sales/d1$Size #divido i ricavi per la dimensione dello store
for (col in c("MarkDown1","MarkDown2","MarkDown3","MarkDown4","MarkDown5")){
  d1[,col] <- d1[,col]/d1$Size #divido gli sconti per la dimensione dello store
}
d1$MMD <- apply(d1[,7:11], MARGIN = 1, function(u) sum(u, na.rm=T)) #calcolo lo sconto totale
d1$Weekly_Sales <- d1$Weekly_Sales+d1$MMD #calcolo i ricavi lordi
d1$rapp <- d1$MMD/d1$Weekly_Sales #calcolo il rapporto tra sconti e vendite (vorrò questo rapporto il più basso possibile)

size <- d1$Size

d1$Season <- "Autunno"
d1$Season[d1$Date > "2011-12-21"] <- "Inverno"
d1$Season[d1$Date > "2012-03-21"] <- "Primavera"
d1$Season[d1$Date > "2012-06-21"] <- "Estate"
d1$Season[d1$Date > "2012-09-21"] <- "Autunno"

d1$Autunno <- F; d1$Autunno[d1$Season=="Autunno"] <- T; d1$Autunno <- as.character(d1$Autunno)
d1$Winter <- F; d1$Winter[d1$Season=="Inverno"] <- T; d1$Winter <- as.character(d1$Winter)
d1$Estate <- F; d1$Estate[d1$Season=="Estate"] <- T; d1$Estate <- as.character(d1$Estate)
d1$Primavera <- F; d1$Primavera[d1$Season=="Primavera"] <- T; d1$Primavera <- as.character(d1$Primavera)

#elimino le variabili che non mi servono
d1$Store = NULL
d1$Date = NULL
#d1$Size = NULL
#d1$Type = NULL

#alberi di regressione
library(rpart)
library(rpart.plot)
library(caret)

#ricodifico le variabili factor per caret
d2 <- d1
d2$BeforeHoliday <- ifelse(d2$BeforeHoliday=="TRUE", 1, 0)
d2$IsHoliday <- ifelse(d2$IsHoliday=="TRUE", 1, 0)
d2$AfterHoliday <- ifelse(d2$AfterHoliday=="TRUE", 1, 0)

#tuno il modello con risposta "weekly_sales"
set.seed(123)
Ctrl <- trainControl(method = "cv" , number=10)
rpartTune <- train(Weekly_Sales ~ IsHoliday + BeforeHoliday + AfterHoliday + Temperature +
                     Fuel_Price + CPI + Unemployment + Season, data = d2, method = "rpart", 
                   tuneLength = 15, trControl = Ctrl)
rpartTune
varImp(rpartTune) #teniamo solo le variabili "CPI" e "Unemployment"

#creo l'albero con il parametro cp più sensato
set.seed(123)
my.tree <- rpart(Weekly_Sales ~ CPI + Unemployment, data = d1, cp=0.01)
windows();rpart.plot(my.tree, type = 4, extra = 101, cex=0.7)
#tuno il modello con risposta "rapp"
set.seed(123)
rpartTune2 <- train(rapp ~ IsHoliday + BeforeHoliday + AfterHoliday + Temperature + Season,
                   data = d2, method = "rpart", 
                   tuneLength = 15, trControl = Ctrl)
rpartTune2

#creo l'albero con il parametro cp più sensato
set.seed(123)
my.tree2 <- rpart(rapp ~ IsHoliday + BeforeHoliday + AfterHoliday + Temperature + Winter,
                  data = d1, cp=0.01)
windows();rpart.plot(my.tree2, type = 4, extra = 101, cex=0.8)

#per ogni foglia creo una nn
my.pred <- round(predict(my.tree2), 4)
my.res <- rep(0,8)
my.num <- rep(0,8)
i <- 0
j <- 1
my.pred.ok <- rep(0, nrow(d1))
my.nns <- list()
ctrl = trainControl(method="cv", number=5)
for (el in unique(my.pred)){
  i <- i+1
  my.data <- d1[my.pred == el,]
  set.seed(123)
  nnetFit <- train(my.data[,c("Type","Size","Unemployment","CPI")],
                             my.data$rapp,
                             method = "nnet", 
                             tuneLength = 5,
                             preProcess = "range", trControl=ctrl,
                             trace = FALSE,
                             maxit = 100)
  my.nns[[i]] <- nnetFit
  my.res[i] <- getTrainPerf(nnetFit)[2]
  my.num[i] <- nrow(my.data)
  my.pred.ok[j:(j+nrow(my.data)-1)] <- predict(nnetFit, my.data, "raw")
  j <- j + nrow(my.data)
}
foglie <- unique(my.pred)
cbind(unique(my.pred), my.res, my.num)[order(unique(my.pred)),] #non è il massimo, ma questo è
sum(as.data.frame(my.res)*my.num)/sum(my.num)
plot(d1$rapp, my.pred.ok) #infatti

#tratto CPI e Unemployment come serie storiche
d <- d[order(d$Date),]

cpi <- aggregate(d$CPI, by=list(d$Date), FUN=mean) #aggrego per settimana facendo la media
emp <- aggregate(d$Unemployment, by=list(d$Date), FUN=mean) #aggrego per settimana facendo la media


ts.plot(ts(cpi$x))
ts.plot(ts(emp$x))


library(forecast)
arima_cpi <- auto.arima(cpi$x) #stimo il miglior modello arima per cpi
arima_emp <- auto.arima(emp$x) #stimo il miglior modello arima per emp

cpi_forecast <- forecast(arima_cpi, h=4) #prevedo i valori di cpi per le prossime 4 settimane
plot(cpi_forecast, xlab="Week", ylab="CPI") 

emp_forecast <- forecast(arima_emp, h=4) #prevedo i valori di emp per le prossime 4 settimane
plot(emp_forecast, xlab="Week", ylab="Unemployment")

rm(arima_cpi, arima_emp, cpi, Ctrl, ctrl, d, d2, emp, rpartTune, rpartTune2, col, size, my.data, my.res, nnetFit, el, i, j, my.num, my.pred, my.pred.ok)
save.image("~/decision_models/tree_work.RData")

#albero decisionale
library(yaml)
library(radiant)
library(radiant.model)
tree = yaml.load_file(input = "markdown_tree.yaml")
#load("~/decision_models/tree_work.RData")

before <- "FALSE"
is <- "FALSE"
after <- "FALSE"
seas <- "Autunno"
#seed <- c(222,122,212,221)
#set.seed(seed[4])
#my_temp <- sample(d1$Temperature[d1$Season==seas], 1)
my_temp <- 45
inv <- ifelse(seas=="Inverno", "TRUE", "FALSE")
size <- 151315
type <- "A"
elast <- 0.095
mark <- 0.2
aument <- round(1/(1-mark), 3)-1
my_cpi <- as.data.frame(cpi_forecast)[1,1]
my_emp <- as.data.frame(emp_forecast)[1,1]

tree$variables$size <- size
tree$variables$sales <- round(predict(my.tree, newdata = data.frame(CPI=my_cpi, Unemployment=my_emp)), 3)

temp_47 <- (47 - my_temp)/sd(d1$Temperature[d1$Season==seas])
prob_47 <- pnorm(temp_47)
temp_50 <- (50 - my_temp)/sd(d1$Temperature[d1$Season==seas])
prob_50 <- pnorm(temp_50)
prob_between <- prob_50 - prob_47

tree$variables$prob_t_47 <- round(prob_47, 3)
tree$variables$prob_t_between <- round(prob_between, 3)

foglia <- round(predict(my.tree2, newdata = data.frame(Temperature=40, BeforeHoliday=before, IsHoliday=is, AfterHoliday=after, Winter=inv)), 4)
my.nn <- my.nns[[which(foglie == foglia)]]
tree$variables$ratio_less_47 <- round(predict(my.nn, data.frame(Size=size, Type=type, Unemployment=my_emp, CPI = my_cpi), "raw"), 4)

foglia <- round(predict(my.tree2, newdata = data.frame(Temperature=48, BeforeHoliday=before, IsHoliday=is, AfterHoliday=after, Winter=inv)), 4)
my.nn <- my.nns[[which(foglie == foglia)]]
tree$variables$ratio_between <- round(predict(my.nn, data.frame(Size=size, Type=type, Unemployment=my_emp, CPI = my_cpi), "raw"), 4)

foglia <- round(predict(my.tree2, newdata = data.frame(Temperature=55, BeforeHoliday=before, IsHoliday=is, AfterHoliday=after, Winter=inv)), 4)
my.nn <- my.nns[[which(foglie == foglia)]]
tree$variables$ratio_more_50 <- round(predict(my.nn, data.frame(Size=size, Type=type, Unemployment=my_emp, CPI = my_cpi), "raw"), 4)

tree$variables$epsi <- elast
tree$variables$aum <- aument

result = dtree(yl = tree)
plot(result, final = T);round(data.frame(sales=tree$variables$sales*tree$variables$size, temp=my_temp ,ratio_47=tree$variables$ratio_less_47, ratio_between=tree$variables$ratio_between, ratio_50=tree$variables$ratio_more_50),3)

windows();sensitivity(
  result, 
  vars = "epsi 0.05 0.15 0.01;", 
  decs = c("apply_markdowns", "not_apply_markdowns"), 
  custom = FALSE)
