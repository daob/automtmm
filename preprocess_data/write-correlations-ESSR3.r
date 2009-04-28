require(foreign)
require(Matrix)

base.path <- "H:/essround3/newexperiments"

#round.3.integrated <- read.spss( "C:\\Users\\esade\\Desktop\\ESSround3\\ESS3mergedwithoutpbdiff_1.sav",use.value.labels=F, to.data.frame=F)
round.3.integrated <- read.spss( "H:\\essround3\\ESS3mergedwithoutpbdiff_1.sav",use.value.labels=F, to.data.frame=F)


# The variables experimented upon in the main questionnaire:
experimental.vars.main <- c("IMSMETN",
                            "IMDFETN",
                            "IMPCNTR",
                            
                            "IMBGECO",
                            "IMUECLT",
                            "IMWBCNT",

                            "LRNNEW",
                            "ACCDNG",
                            "PLPRFTR",
                            
                            "DNGVAL",
                            "PPLLFCR",
                            "FLCLPLA" )

# all the sapplementary variables
experimental.vars.supq <- c("TESTB1", 
				    "TESTB2",
				    "TESTB3",
				    "TESTB4",
				    "TESTB5",
				    "TESTB6",
				    "TESTB7",
				    "TESTB8",
				    "TESTB9",
				    "TESTB10",
				    "TESTB11",
				    "TESTB12",
				    "TESTB13",
				    "TESTB14",
				    "TESTB15",
				    "TESTB16",
				    "TESTB17",
				    "TESTB18",
				    "TESTB19",
				    "TESTB20",
				    "TESTB21",
				    "TESTB22",
				    "TESTB23",
				    "TESTB24",
				    "TESTB25",
				    "TESTB26",
				    "TESTB27",
				    "TESTB28",
				    "TESTB29",
				    "TESTB30",
				    "TESTB31",
				    "TESTB32",
				    "TESTB33",
				    "TESTB34",
				    "TESTB35",
				    "TESTB36")

# define the value labels that are to be coded as missing (NA):
code.missing.labels    <- c("No answer",
                            "Don't know",
                            "Refusal",
                            "Not applicable"
                           )

round.3.mtmm <-  round.3.integrated[c(experimental.vars.main, experimental.vars.supq)]
round.3.mtmm <-  as.data.frame(round.3.mtmm)

#names(round.3.mtmm)

# Recode those values whose labels have been defined as missing to NA:
for( var in names(round.3.mtmm)) {
  code.missing.values <- na.omit(attr(round.3.mtmm[,var],"value.labels")[code.missing.labels] )
  round.3.mtmm[ round.3.mtmm[  ,var] %in% code.missing.values ,var] <- NA
}

country <-  as.factor( round.3.integrated['CNTRY'] [[1]] )
group   <-  round.3.integrated['SPLTADMB'] [[1]]

# recode to missing where the split-ballot condition is "not available".
group[group==9] <- NA
#table(group)

#recode the group for the supplementary questionnaires
group[group==4]<-1
group[group==5]<-2
group[group==6]<-3
#table(group)

#work on the date of the supplementary questionnaire
difference <- round.3.integrated['DIFFEREN'][[1]]
table(difference)
summary(difference)
difference[difference<=-1]<- -1
difference[difference==0]<- 0
difference[0<difference]<- 1
#this gives all the numbers for lisrel
table(group,country,difference)


#creation of all the matrices

for (C in levels(country)) { # The different countries
  print(C)
  dir.create( paste( base.path, C, sep="/" ) )
  
  for(i in seq(1, 10, by=3) ) { # The different experiments
    path <- paste( base.path, C, names(round.3.mtmm)[i], sep="/")
    dir.create( path )
    
    for(cur.group in 1:3) { # The different Split-Ballot groups
      # Select the right variables and country
      tempdata <- round.3.mtmm[ country == C  & group == cur.group & difference==0,
                                c( i:(i+2), (i+12):(i+14), (i+24):(i+26), (i+36):(i+38) )
                              ]
      if (NROW(tempdata) > 0) {
        S <- cov(tempdata, use="pairwise.complete.obs")
        M <- mean(tempdata, na.rm=T)

        S[upper.tri(S)] <- NA
        diag(S)[is.na(diag(S))] <- 1.0
        S[ lower.tri(S) & is.na(S) ] <- 0.0
        
        write.table( S, file= paste( path, "/", "sb-group-", cur.group, ".cov",  sep=""), row.names=F, col.names=F, na="" )
        write.table( M, file= paste( path, "/", "sb-group-", cur.group, ".mean", sep=""), row.names=F, col.names=F, na="0.0" )
      }
      else {
        print(paste("Could not do anything for country/experiment", path, ", group, ", cur.group ))
      }
    }
  }
}


