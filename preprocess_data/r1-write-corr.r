require(foreign)
require(Matrix)

base.path <- "G:/Database/ESS experiments/round1/matrices"

round.1.integrated <- read.spss( "G:\\Database\\ESS experiments\\round1\\ESSround1finalBONoutliers.sav",use.value.labels=F, to.data.frame=F)


# The variables experimented upon in the main questionnaire:
experimental.vars.main <- c("tvtot",
                            "rdtot",
                            "nwsptot",
                            
                            "polcmpl",
                            "polactiv",
                            "poldcs",

                   	    "stfeco",
                            "stfgov",
                            "stfdem",

                            "ppltrst",
                            "pplfair",
                            "pplhlp",
                            
                            "trstprl",
                            "trstlgl",
                            "trstplc",

           			    "ginveco",
                            "gincdif",
                            "needtru")

# all the supplementary variables
experimental.vars.supq <- c("test1", 
				    "test2",
				    "test3",
				    "test4",
				    "test5",
				    "test6",
				    "test7",
				    "test8",
				    "test9",
				    "test10",
				    "test11",
				    "test12",
				    "test13", 
				    "test14", 
				    "test15", 
				    "test16",
				    "test17",
				    "test18",
				    "test19",
				    "test20",
				    "test21",
				    "test22",
				    "test23",
				    "test24",
				    "test25",
				    "test26",
				    "test27",
				    "test28",
				    "test29",
				    "test30",
				    "test31",
				    "test32",
				    "test33",
				    "test34",
				    "test35",
				    "test36")

# define the value labels that are to be coded as missing (NA):
code.missing.labels    <- c("No answer",
                            "Don't know",
                            "Refusal",
                            "Not applicable"
                           )

round.1.mtmm <-  round.1.integrated[c(experimental.vars.main, experimental.vars.supq)]
round.1.mtmm <-  as.data.frame(round.1.mtmm)

#names(round.1.mtmm)

# Recode those values whose labels have been defined as missing to NA:
for(var in names(round.1.mtmm)) {
  code.missing.values <- na.omit(attr(round.1.mtmm[,var],"value.labels")[code.missing.labels] )
  round.1.mtmm[ round.1.mtmm[  ,var] %in% code.missing.values ,var] <- NA
}

country <-  as.factor( round.1.integrated['cntry'] [[1]] )

#split ballot group for the supplementary questionnaire
sbgroup   <-  round.1.integrated['spltadm'] [[1]]


# recode to missing where the split-ballot condition is "not available".
sbgroup[sbgroup==99] <- NA
#table(sbgroup)

#recode the group for the supplementary questionnaires
#case with 2 groups
sbgroup[sbgroup==9]<-1
sbgroup[sbgroup==10]<-2
#case with 6 groups, but we consider them as only 2
sbgroup[sbgroup==3|sbgroup==4|sbgroup==5|sbgroup==11|sbgroup==12|sbgroup==13]<-1
sbgroup[sbgroup==6|sbgroup==7|sbgroup==8|sbgroup==14|sbgroup==15|sbgroup==16]<-2
#case without sb-gp
sbgroup[sbgroup==21|sbgroup==22]<-1
#table(sbgroup)

expt<-c("media", "media","media", "poleff", "poleff","poleff", "satisf", "satisf", "satisf", 
"soctrust", "soctrust","soctrust", "trustin", "trustin","trustin", "polor", "polor", "polor")


#creation of all the matrices

for (C in levels(country)) { # The different countries
  print(C)
  dir.create( paste( base.path, C, sep="/" ) )
  
  for(i in seq(1, 16, by=3) ) { # The different experiments
    path <- paste( base.path, C, expt[i], sep="/")
    dir.create( path )
    
    for(cur.sbgroup in 1:2) { # The different Split-Ballot groups
      tempdata <- round.1.mtmm[ country == C  &  sbgroup == cur.sbgroup,
                                c( i:(i+2), (i+18):(i+20), (i+36):(i+38) )
                              ]
	#print(names(tempdata))
      if (NROW(tempdata) > 0) {
        S <- cov(tempdata, use="pairwise.complete.obs")
        M <- mean(tempdata, na.rm=T)

        S[upper.tri(S)] <- NA
        diag(S)[is.na(diag(S))] <- 1.0
        S[ lower.tri(S) & is.na(S) ] <- 0.0
        
        write.table( S, file= paste( path, "/", "sb-group-", cur.sbgroup, ".cov",  sep=""), row.names=F, col.names=F, na="" )
        write.table( M, file= paste( path, "/", "sb-group-", cur.sbgroup, ".mean", sep=""), row.names=F, col.names=F, na="0.0" )
      }
      else {
        print(paste("Could not do anything" ))
      }
    }
  }
}


