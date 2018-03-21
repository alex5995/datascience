ecommerce_data <- read.csv("~/dataviz_lab/ecommerce/project/preprocessing/ecommerce_data.csv")

ecommerce_data$Revenue = ecommerce_data$Quantity*ecommerce_data$UnitPrice

nodi <- ecommerce_data[ecommerce_data$Country!="United Kingdom",]
nodi <- aggregate(nodi$Revenue, by=list(nodi$Country), FUN=sum)
names(nodi) <- c("Id", "Revenue")
nodi$Label <- nodi$Id

ecommerce_data <- ecommerce_data[ecommerce_data$Country!="United Kingdom",]
agg <- aggregate(ecommerce_data$Quantity, by=list(ecommerce_data$Country, ecommerce_data$StockCode), FUN=sum)

write.csv(nodi, file="~/dataviz_lab/ecommerce/project/preprocessing/nodi.csv", row.names=FALSE)
write.csv(agg, file="~/dataviz_lab/ecommerce/project/preprocessing/agg.csv")
