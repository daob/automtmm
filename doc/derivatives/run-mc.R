
#source("/Users/daob/Documents/lavaan/tests/health-multigroup-test.R")
#res <- monte.carlo(512)
#save(res2, file="mc.results-512.rdata")

display.pars <- function(year, group) {
	lyi <- unlist(lapply(res, function(r) r$results[year, group]))
	lyi.z <- ztransform(lyi)
	
	display.par <- function(p, m) {
		hist(p, freq=FALSE, main=m)
		lines(density(p))
		norm.test <- shapiro.test(p)	
		qqnorm(p, main=sprintf("%s\np-value for normality: %1.3f",m, norm.test$p))
		qqline(p)	
		norm.test$p
	}
	par(mfcol=c(2,2))
	nlam <- display.par(lyi, 'lambda')
	nlamz <- display.par(lyi.z, 'z-transform')
	c('norm.lam'=nlam, 'norm.lamz'=nlamz)
}

get.mean.sd <- function(year, group) {
	lyi <- unlist(lapply(res, function(r) r$results[year, group]))
	list('mean'=mean(lyi), 'sd'=sd(lyi))	
}

get.coverage <- function(year, group, true.val) {
	unlist(lapply(res, function(r) {
		lo <- r$results[year, sprintf("lower.z.%d", group)]
		up <- r$results[year, sprintf("upper.z.%d", group)]
		
		in.interval <- lo <= true.val && up >= true.val
		mean(in.interval)
	}))
}

ntest <- mapply(function(year)
	mapply(function(group) {
		pdf(sprintf("normplots/normality-yr%d-gp%d.pdf", year, group), 8, 8)
		p <- display.pars(year, group)
		dev.off()
		p
	}
, 'group'=1:6, SIMPLIFY=FALSE), 'year'=1:4, SIMPLIFY=TRUE)

# Some of the 
mapply(function(method) p.adjust(unlist(ntest), method=method) <.05, 
	c("holm", "hochberg", "hommel", "bonferroni", "BH", "BY",'fdr'))

mapply(function(method) any(p.adjust(unlist(ntest), method=method) <.05), 
	c("holm", "hochberg", "hommel", "bonferroni", "BH", "BY",'fdr'))
	
# ztransform appears to be a better approximation to the normal, low power though:
mean(mapply(function(x) x[2]>x[1],ntest))

bias <- function(year, group) {
	msd <- get.mean.sd(year, group)
	bias <-  msd$mean - ly.true[year, group]
	relbias <- 100 * bias/ly.true[year, group]
	
	bias.sd <- msd$sd - asymp.ses[year, group]
	relbias.sd <- 100 * bias.sd/asymp.ses[year, group]
	
	c('bias'=bias, 'relbias'=relbias, 
		'bias.sd'=bias.sd, 'relbias.sd'=relbias.sd)
}

allbias <- mapply(function(year)
	mapply(function(group) {
		round(bias(year, group),3)
	}
, 'group'=1:6, SIMPLIFY=FALSE), 'year'=1:4, SIMPLIFY=FALSE)

allcoverage <- mapply(function(year)
	mapply(function(group) {
		round(mean(get.coverage(year, group, ly.true[year,group])),3)*100
	}
, 'group'=1:6, SIMPLIFY=FALSE), 'year'=1:4, SIMPLIFY=FALSE)