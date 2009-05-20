require(foreign)
require(Matrix)

base.path <- "G:/Database/ESS experiments/round2/matrices"

round.2.integrated <- read.spss( "G:\\Database\\ESS experiments\\round2\\ESSround2finalBON.sav",use.value.labels=F, to.data.frame=F)


# The variables experimented upon in the main questionnaire:
experimental.vars.main <- c("hwktwd1",
                            "hwkpwd1",
                            "hwkpwdp",
                            
                            "dckptrt",
                            "dctreql",
                            "dcdisc",

                   	    "vrtywrk",
                            "jbscr",
                            "hlthrwk",

                            "wmcpwrk",
                            "mnrsphm",
                            "mnrgtjb",
                            
                            "stfeco",
                            "stfgov",
                            "stfdem",

           			    "trstprl",
                            "trstlgl",
                            "trstplt")

# all the supplementary variables
experimental.vars.supq <- c("testa2", 
				    "testa3",
				    "testa4",

				    "testa5",
				    "testa6",
				    "testa7",

				    "testa19",
				    "testa20",
				    "testa21",

				    "testa8",
				    "testa9",
				    "testa10",

				    "testa11", 
				    "testa12", 
				    "testa13",
 
				    "testa25",
				    "testa26",
				    "testa27",

				    "testa15",
				    "testa16",
				    "testa17",

				    "testa28",
				    "testa29",
				    "testa30",

				    "testa32",
				    "testa33",
				    "testa34",

				    "testa22",
				    "testa23",
				    "testa24",

				    "testa35",
				    "testa36",
				    "testa37",

				    "testa38",
				    "testa39",
				    "testa40")

# define the value labels that are to be coded as missing (NA):
code.missing.labels    <- c("No answer",
                            "Don't know",
                            "Refusal",
                            "Not applicable"
                           )

round.2.mtmm <-  round.2.integrated[c(experimental.vars.main, experimental.vars.supq)]
round.2.mtmm <-  as.data.frame(round.2.mtmm)

#names(round.2.mtmm)

# Recode those values whose labels have been defined as missing to NA:
for(var in names(round.2.mtmm)) {
  code.missing.values <- na.omit(attr(round.2.mtmm[,var],"value.labels")[code.missing.labels] )
  round.2.mtmm[ round.2.mtmm[  ,var] %in% code.missing.values ,var] <- NA
}

country <-  as.factor( round.2.integrated['cntry'] [[1]] )

#split ballot group for the supplementary questionnaire
sbgroup   <-  round.2.integrated['spltadma'] [[1]]


# recode to missing where the split-ballot condition is "not available".
sbgroup[sbgroup==9] <- NA
#table(sbgroup)

#recode the group for the supplementary questionnaires
sbgroup[sbgroup==4]<-1
sbgroup[sbgroup==5]<-2
sbgroup[sbgroup==6]<-3

expt<- c("1hwk", "1hwk", "1hwk","2doc", "2doc", "2doc", "3job", "3job", "3job", "4women", 
"4women", "4women", "5satisf", "5satisf","5satisf", "6trustin", "6trustin","6trustin")

#creation of all the matrices

for (C in levels(country)) { # The different countries
  print(C)
  dir.create( paste( base.path, C, sep="/" ) )
  
  for(i in seq(1, 16, by=3) ) { # The different experiments
    path <- paste( base.path, C, expt[i], sep="/")
    dir.create( path )
    
    for(cur.sbgroup in 1:3) { # The different Split-Ballot groups
    #creation matrices for the 3 gps even if use only 2
      tempdata <- round.2.mtmm[ country == C  &  sbgroup == cur.sbgroup,
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


