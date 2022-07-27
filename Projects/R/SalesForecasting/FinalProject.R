# Assignment: Final Project
# Name: Zoucha,Michael
# Date: 2021-10-03

## Load the necessary packages
library(readxl)
library(dplyr)
library(stringr)
library(rlang)
library(tidyverse) 
library(grid)      
library(gridExtra) 
library(ggpubr)    
library(patchwork)
library(pivot)

## STEP 1: GATHER AND ANALYZE SALES DATA FOR FUTURE SALES NUMBER PREDICTIONS


## Load data frames with all data for data frame combinations for final data frame
## All CSV files exists in Final Project Data folder
salesorderdetail_df <- read.csv("Final Project Data/SalesOrderDetail.csv")

salesorderheader_df <- read.csv("Final Project Data/SalesOrderHeader.csv")

salesterritory_df <- read.csv("Final Project Data/SalesTerritory.csv")

specialoffer_df <- read.csv("Final Project Data/SpecialOffer.csv")

productdetails_df <- read.csv("Final Project Data/ProductDetails.csv")

productcategory_df <- read.csv("Final Project Data/ProductCategory.csv")

productsubcategory_df <- read.csv("Final Project Data/ProductSubcategory.csv")


## Parse down to necessary data using select function
salesorderdetail_df <- select(salesorderdetail_df, SalesOrderID, OrderQty, 
                              SpecialOfferID, UnitPrice, LineTotal, ProductID)

salesorderheader_df <- select(salesorderheader_df, TerritoryID, SalesOrderID, 
                              OrderDate)

salesterritory_df <- select(salesterritory_df, Name, CountryRegionCode, Group, 
                            TerritoryID)

specialoffer_df <- select(specialoffer_df, SpecialOfferID, Description, Type, 
                          Category)

productdetails_df <- select(productdetails_df, ProductID, Name, ProductNumber, 
                           Color, StandardCost, ListPrice, ProductSubcategoryID)

productcategory_df <- select(productcategory_df, ProductCategoryID, Name)

productsubcategory_df <- select(productsubcategory_df, ProductSubcategoryID, 
                                Name, ProductCategoryID)


## Combine Product Data Frames, rename columns appropriately
product_merged_df <- merge(productdetails_df, productsubcategory_df, 
                           by = "ProductSubcategoryID", all.x = TRUE) %>%
                     merge(., productcategory_df, 
                           by = "ProductCategoryID", all.x = TRUE)

#Rename Merged Columns
product_merged_df <- rename(product_merged_df, Subcategory = Name.y, 
                            Category = Name)


## Combine sales data frames and product_merged_df for final data frame
final_merged_df <- merge(salesorderdetail_df, product_merged_df, 
                         by = "ProductID", all.x = TRUE) %>%
                   merge(., salesorderheader_df, 
                         by = "SalesOrderID", all.x = TRUE) %>%
                   merge(., specialoffer_df, 
                         by = "SpecialOfferID", all.x = TRUE) %>%
                   merge(., salesterritory_df, 
                         by = "TerritoryID", all.x = TRUE)

## Rename merged columns
final_merged_df <- rename(final_merged_df, ProductName = Name.x, ProductCategory = Category.x, 
                          DiscountDescription = Description, DiscountType = Type, 
                          DiscountCategory = Category.y, TerritoryName = Name, TerritoryGroup = Group)


## Remove unneeded data frames
remove(salesorderdetail_df, salesorderheader_df, salesterritory_df, specialoffer_df, 
       productdetails_df, productcategory_df, productsubcategory_df, product_merged_df)


## Add calculated columns
## Year Column using substring
## Month Column using substring
## Total profit per line item
## Profit per item sold, per line item
final_merged_df <- dplyr::mutate(final_merged_df, 
                                 year = substring(OrderDate,7,10)) %>%
                   dplyr::mutate(., month = substring(OrderDate,0,2)) %>%
                   dplyr::mutate(., totalprofit = LineTotal - (OrderQty * StandardCost)) %>%
                   dplyr::mutate(., itemprofit = (LineTotal - (OrderQty * StandardCost)) / OrderQty)

str(final_merged_df)

## Exploratory Data Analysis

## History of number of items sold for each ProductID for each year
products_by_year<- dplyr::group_by(final_merged_df, year, ProductID) %>% 
  dplyr::summarize(number_sold = sum(OrderQty))

## History of number of items sold for each ProductID for each year
products_by_year_month <- dplyr::group_by(final_merged_df, year, month, ProductID) %>% 
  dplyr::summarize(number_sold = sum(OrderQty))

## History of number of items sold for each ProductCategory for each year - include bar graph
product_cat_by_year <- dplyr::group_by(final_merged_df, year, ProductCategory) %>% 
  dplyr::summarize(number_sold = sum(OrderQty))

## History of number of items sold for each ProductCategory for each year
product_cat_by_year_month <- dplyr::group_by(final_merged_df, year, month, ProductCategory) %>% 
  dplyr::summarize(number_sold = sum(OrderQty))

## History of number of items sold for each ProductSubCategory for each year - include bar graph
product_subcat_by_year <- dplyr::group_by(final_merged_df, year, Subcategory, ProductCategory) %>% 
  dplyr::summarize(number_sold = sum(OrderQty))

## History of number of items sold for each ProductSubCategory for each year
product_subcat_by_year_month <- dplyr::group_by(final_merged_df, year, month, Subcategory) %>% 
  dplyr::summarize(number_sold = sum(OrderQty))


cat_by_year_plot <- ggplot2::ggplot(product_cat_by_year, aes(x=year, y=number_sold, fill =ProductCategory)) + 
                ggplot2::geom_bar(stat="identity", position=position_dodge()) + 
                ggplot2::ggtitle("Number Items Sold per Year by Category") + 
                ggplot2::xlab("Year") + 
                ggplot2::ylab("Number Sold")

bikes_plot <- ggplot2::ggplot(filter(product_subcat_by_year, ProductCategory == "Bikes"), aes(x=year, y=number_sold, fill=Subcategory)) +
                ggplot2::geom_bar(stat="identity", position=position_dodge()) +
                ggplot2::ggtitle("Number Items Sold per Year by Subcategory") +
                ggplot2::xlab("Year") +
                ggplot2::ylab("Number Sold") +
                facet_grid(.~ProductCategory)

components_plot <- ggplot2::ggplot(filter(product_subcat_by_year, ProductCategory == "Components"), aes(x=year, y=number_sold, fill=Subcategory)) +
                ggplot2::geom_bar(stat="identity", position=position_dodge()) +
                ggplot2::ggtitle("Number Items Sold per Year by Subcategory") +
                ggplot2::xlab("Year") +
                ggplot2::ylab("Number Sold") +
                facet_grid(.~ProductCategory)

accessories_plot <- ggplot2::ggplot(filter(product_subcat_by_year, ProductCategory == "Accessories"), aes(x=year, y=number_sold, fill=Subcategory)) +
                ggplot2::geom_bar(stat="identity", position=position_dodge()) +
                ggplot2::ggtitle("Number Items Sold per Year by Subcategory") +
                ggplot2::xlab("Year") +
                ggplot2::ylab("Number Sold") +
                facet_grid(.~ProductCategory)

clothing_plot <- ggplot2::ggplot(filter(product_subcat_by_year, ProductCategory == "Clothing"), aes(x=year, y=number_sold, fill=Subcategory)) +
                ggplot2::geom_bar(stat="identity", position=position_dodge()) +
                ggplot2::ggtitle("Number Items Sold per Year by Subcategory") +
                ggplot2::xlab("Year") +
                ggplot2::ylab("Number Sold") +
                facet_grid(.~ProductCategory)

grid.newpage()

pushViewport(viewport(layout = grid.layout(2,2)))

print(bikes_plot, vp = viewport(layout.pos.row = 1, layout.pos.col =  1))

print(components_plot, vp = viewport(layout.pos.row = 1, layout.pos.col =  2))

print(accessories_plot, vp = viewport(layout.pos.row = 2, layout.pos.col =  1))

print(clothing_plot, vp = viewport(layout.pos.row = 2, layout.pos.col =  2))


pivot_table_1 <- spread(filter(product_subcat_by_year, ProductCategory == "Bikes"), key = year, value = number_sold)

filter(product_subcat_by_year, ProductCategory == "Bikes")
## STEP 2: CREATE PREDICTION MODEL FOR QUANTITY SOLD PER ITEM, PER MONTH, PER YEAR
## STEP 3: COMPARE TO CURRENT INVENTORY / INVENTORY MAX/MINS 