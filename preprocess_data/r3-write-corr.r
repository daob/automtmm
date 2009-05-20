require(foreign)
require(Matrix)

base.path <- "/home/daob/work/ess/data/round-3/experiments"

#main        <- read.spss("ESS3e02.por",     use.value.labels=F, to.data.frame=F)
#interviewer <- read.spss("ESS3INTe01.por",  use.value.labels=F, to.data.frame=F)
#mtmm        <- read.spss("ESS3MTMMe01.por", use.value.labels=F, to.data.frame=F)

round.3.integrated <- read.spss( "ESS3v2ROMTMM.sav",     use.value.labels=F, to.data.frame=F)

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

# all the variables starting with the name "TEST" will be added to the data:
experimental.vars.supq <- names(lluis)[grep("^TEST",names(lluis))]

# define the value labels that are to be coded as missing (NA):
code.missing.labels    <- c("No answer",
                            "Don't know",
                            "Refusal",
                            "Not applicable"
                           )

round.3.mtmm <-  round.3.integrated[c(experimental.vars.main, experimental.vars.supq)]
round.3.mtmm <-  as.data.frame(round.3.mtmm)

# Recode those values whose labels have been defined as missing to NA:
for( var in names(round.3.mtmm)) {
  code.missing.values <- na.omit(attr(round.3.mtmm[,var],"value.labels")[code.missing.labels] )
  round.3.mtmm[ round.3.mtmm[  ,var] %in% code.missing.values ,var] <- NA
}

country <-  as.factor( round.3.integrated['CNTRY'] [[1]] )
group   <-  round.3.integrated['SPLTADMB'] [[1]]
# recode to missing where the split-ballot condition is "not available".
# This is the case for Hungary, where no experiments were done,
#   and a sporadic few (21) of the other cases: 100 * (21/37043) = 0.06 percent
group[group==9] <- NA




for (C in levels(country)) { # The different countries
  print(C)
  dir.create( paste( base.path, C, sep="/" ) )
  
  for(i in seq(1, 10, by=3) ) { # The different experiments
    path <- paste( base.path, C, names(round.3.mtmm)[i], sep="/")
    dir.create( path )
    
    for(cur.group in 1:3) { # The different Split-Ballot groups
      # Select the right variables and country
      tempdata <- round.3.mtmm[ country == C  & group == cur.group,
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
