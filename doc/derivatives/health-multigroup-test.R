library(foreign)
library(lavaan)
library(Matrix)
library(mvtnorm)

setwd('~/Documents/lavaan/tests/')

# Load the derivative matrix function:
source('../lavaan/R/delta.R')

# Load Yves' experimental matrix functions:
source('../lavaan/R/dup.R')


load('genhealth.rdata')

# Quasi-simplex model for 4 waves (Wiley & Wiley)
model <- '
    Lhlt.2007 =~  1*hlt.2007
    Lhlt.2008 =~  1*hlt.2008
    Lhlt.2009 =~  1*hlt.2009
    Lhlt.2010 =~  1*hlt.2010

    Lhlt.2010 ~~ Lhlt.2010 
    Lhlt.2009 ~~ Lhlt.2009 
    Lhlt.2008 ~~ Lhlt.2008 
    Lhlt.2007 ~~ Lhlt.2007

    Lhlt.2008 ~ Lhlt.2007
    Lhlt.2009 ~ Lhlt.2008 
    Lhlt.2010 ~ Lhlt.2009

    hlt.2007 ~~ ev*hlt.2007
    hlt.2008 ~~ ev*hlt.2008
    hlt.2009 ~~ ev*hlt.2009
    hlt.2010 ~~ ev*hlt.2010
'

fit <- lavaan(model, data=genhealth, group='oplcat')
m <- LISREL.matrices(fit@Model)
Dy <- D(Sigma.y(fit@Model))
De <- D(Sigma.eta(fit@Model))
LYs <- solve(Dy) %*% m$LY %*% De
ly.true <- columnify(diag(LYs))

time.taken <- (system.time(vs <- vcov.standardized(fit, vidx.mg)))['elapsed']
asymp.ses <- columnify(sqrt(diag(vs)[1:24]))
	

vidx <- c(8:11, 4:1, 5:7)
# Put vcov in the right order (same as before but repeated over groups)
vidx.mg <- as.vector(mapply(
	function(ig) vidx + (ig-1)*11, 
	1:fit@Model@ngroups
))

# Show the estimates column-wise by group and sort on group name
columnify <- function(x) {
	x <- matrix(x, length(x)/fit@Model@ngroups)
	colnames(x) <- fit@Sample@group.label
	x[, sort(colnames(x))]	
}

nobs <- unlist(fit@Sample@nobs)
nsim <- 15


vcov.standardized <- function(fit, vidx)  {	
	# Duplicate equality constrained elements
	K <- fit@Model@eq.constraints.K
	V <- K %*% vcov(fit) %*% t(K)
	
	# Put the matrix in the correct order
	V <- V[vidx, vidx]

	# Get the derivatives wrt parameters
	ds <- d.theta.s(fit@Model, beta=FALSE)
	
	# Stack derivs wrt lambda and beta row-wise
	G <- ds$lambda.s
	
	# The Delta method:	
	G %*% V %*% t(G)
}

estimate.model <- function(data) {
	fit <- lavaan(model, data=data, group='oplcat')
	# Matrices of standard deviations
	Dy <- D(Sigma.y(fit@Model))
	De <- D(Sigma.eta(fit@Model))
	
	# Calculate standardized estimates (corresponds to `standardized' output of
	#   summary).
	m <- LISREL.matrices(fit@Model)
	
	LYs <- solve(Dy) %*% m$LY %*% De
	#BEs <- solve(De) %*% m$BE.0 %*% De
	
	ly <- diag(LYs)
	
	time.taken <- (system.time(vs <- vcov.standardized(fit, vidx.mg)))['elapsed']
	ses <- sqrt(diag(vs))
	
	V <- vs[1:24, 1:24]
	CI <- get.confint.ztransform(ly, V)
	lower.z <- columnify(CI[1, ])
	upper.z <- columnify(CI[2, ])	

	list('time.taken' = time.taken,
		'results' = data.frame(
			'ly' = columnify(ly),	
			'se' = columnify(ses[1:24]),
			'lower.z' = lower.z,
			'upper.z' = upper.z
		)
	)
}

generate.data <- function(fit, nobs) {
	dat <- Reduce(rbind, 
				  mapply(function(S, oplcat, n) {
						  	Y <- as.data.frame(rmvnorm(n, rep(0,4), S))	
						  	names(Y) <- fit@Sample@ov.names
						  	Y$oplcat <- oplcat
						  	Y
						  },
				  		 S = fit@Fit@Sigma.hat, 
				  		 oplcat  = as.numeric(fit@Sample@group.label),
				  		 n = nobs,
				  		 SIMPLIFY = FALSE
				  )
	)
	dat
}

#print("Monte Carlo...")
#print(system.time(
#	mc.results <- replicate(nsim, estimate.model(generate.data(fit, nobs)))
#))
NCLUS <- 8
monte.carlo <- function(nsim) {
	library(snow)
	stopifnot(as.integer(nsim/NCLUS) == nsim/NCLUS)
	
	cl <- makeCluster(NCLUS)
	print("Time taken to load the input:")
	print(system.time(clusterEvalQ(cl,
	    source("/Users/daob/Documents/lavaan/tests/health-multigroup-test.R"))))
	
	print("Time taken to do the Monte Carlo:")
	print(system.time(r <- clusterApply(cl, 1:nsim,
				function(is) estimate.model(generate.data(fit, nobs))
	)))
	
	stopCluster(cl)	
	
	r
}
