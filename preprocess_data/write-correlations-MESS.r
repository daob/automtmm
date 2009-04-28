require(foreign)
require(Matrix)

base.path <- "G:/mixedmode/analyses/Mess/NLmedia"

mess.integrated <- read.spss( "G:\\mixedmode\\data\\LESS_MTMM\\LESS_MTMM_reduit_mergevarVraioutliersMore.sav",use.value.labels=F, to.data.frame=F)
#names(mess.integrated)

# The variables experimented upon the method 1
vars.method1           <- c("M11",
                            "M13",
                            "M15",
                            
                            "ST11",
                            "ST12",
                            "ST13",

                            "S11",
                            "S12",
                            "S13",

				    "P11",
                            "P12",
                            "P13",

                            "PT11",
                            "PT12",
                            "PT13",

                            "LR11",
                            "LR12",
                            "LR13" )


# The variables experimented upon the method 2
vars.method2           <- c("M21",
                            "M23",
                            "M25",
                            
                            "ST21",
                            "ST22",
                            "ST23",

                            "S21",
                            "S22",
                            "S23",

				    "P22",#attention!!!
                            "P23",#ordre different
                            "P21",

                            "PT21",
                            "PT22",
                            "PT23",

                            "LR21",
                            "LR22",
                            "LR23" )

# The variables experimented upon the method 3
vars.method3           <- c("M31",
                            "M33",
                            "M35",
                            
                            "ST31",
                            "ST32",
                            "ST33",

                            "S31",
                            "S32",
                            "S33",

				    "P31",
                            "P32",
                            "P33",

                            "PT31",
                            "PT32",
                            "PT33",

                            "LR31",
                            "LR32",
                            "LR33" )

# define the value labels that are to be coded as missing (NA):
code.missing.labels    <- c("No answer",
                            "Don't know",
                            "Refusal",
                            "Not applicable"
                           )

mess.mtmm <-  mess.integrated[c(vars.method1, vars.method2, vars.method3)]
mess.mtmm <-  as.data.frame(mess.mtmm)

#names(mess.mtmm)

# Recode those values whose labels have been defined as missing to NA:
for(var in names(mess.mtmm)) {
  code.missing.values <- na.omit(attr(mess.mtmm[,var],"value.labels")[code.missing.labels] )
  mess.mtmm[ mess.mtmm[  ,var] %in% code.missing.values ,var] <- NA
}

#split ballot group for the supplementary questionnaire
sbgroup   <-  mess.integrated['ARANDOM'] [[1]]
#pr nbobservations ds lisrel progr
#table(sbgroup)

# recode to missing where the split-ballot condition is "not available".
#sbgroup[sbgroup==9] <- NA
#table(sbgroup)


#creation of all the matrices
  
for(i in seq(1, 16, by=3) ) { # The different experiments
  path <- paste( base.path, names(mess.mtmm)[i], sep="/")
  dir.create( path )
    
  for(cur.sbgroup in 1:9) { # The different Split-Ballot groups
  # on cree les matrices pr les 9 groupes meme si ap ya que celles de 3 gp qui servent

      tempdata <- mess.mtmm[ sbgroup == cur.sbgroup,
                                c( i:(i+2), (i+18):(i+20), (i+36):(i+38) )
                              ]
	#print(names(tempdata))
      if (NROW(tempdata) > 0) {
        S <- cov(tempdata, use="pairwise.complete.obs")
        M <- mean(tempdata, na.rm=T)

        S[upper.tri(S)] <- NA
        diag(S)[is.na(diag(S))] <- 1.0
        S[ lower.tri(S) & is.na(S) ] <- 0.0
        
#faut du cur.gp ds le nom aussi !!!!
        write.table( S, file= paste( path, "/", "sbgroup-", cur.sbgroup, ".cov",  sep=""), row.names=F, col.names=F, na="" )
        write.table( M, file= paste( path, "/", "sbgroup-", cur.sbgroup, ".mean", sep=""), row.names=F, col.names=F, na="0.0" )
      }
      else {
        print(paste("Could not do anything" ))
      }
    }
print("end!!")
}


