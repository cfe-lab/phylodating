suppressPackageStartupMessages(
  {
    library(ape, quietly = TRUE)
    library(optparse, quietly = TRUE)
    library(dplyr, quietly = TRUE)
    library(chemCal, quietly = TRUE)
    library(data.table, quietly = TRUE)
  }
)

DATE_FMT <- "%Y-%m-%d"

enquote <- function(x) paste0("\"", x, "\"")

# utility function
to.Date <- function(...) as.Date(..., origin = "1970-01-01")

get.child.lengths <- function(node) {
	sum(tree$edge.length[tree$edge[, 1] == node])
}

is.cherry <- function(node) {
	all(tree$edge[tree$edge[, 1] == node, 2] <= Ntip(tree))
}

# parse command line arguments
op <- OptionParser()
op <- add_option(op, "--runid", type = 'character')
op <- add_option(op, "--tree", type = 'character')
op <- add_option(op, "--info", type = 'character')
op <- add_option(op, "--rootedtree", type = 'character')
op <- add_option(op, "--data", type = 'character')
op <- add_option(op, "--stats", type = 'character')
args <- parse_args(op)

run.id <- args$runid
tree.file <- args$tree
info.file <- args$info
rooted.tree.file <- args$rootedtree
data.file <- args$data
stats.file <- args$stats

output.access <- file.access(
  dirname(c(rooted.tree.file, data.file, stats.file))
)

if (any(output.access) != 0) {
  stop(
    sprintf(
      "Cannot write: %s (either output directory missing or lack permission)",
      paste0(
        c("rooted tree file", "data file", "stats file")[output.access != 0],
        collapse = ", "
      )
    )
  )
}

# read tree and info
tryCatch(
  {tree <- read.tree(tree.file)},
  error = function(e) {
    stop(
      paste0(
        "Failed to read tree file. Tree file should be in newick format.\n",
        e
      )
    )
  }
)

if (is.null(tree)) {
  stop("Failed to read tree file. Tree file should be in newick format.")
}

tryCatch(
  {info <- fread(file = info.file, data.table = FALSE, colClasses = 'character')},
  error = function(e) {
    stop(
      paste0(
        "Failed to read info file. Info file should be in comma seperated value (CSV) format.\n",
        e
      )
    )
  }
)

if (!all(c("ID", "Date", "Query") %in% names(info))) {
  error.message <- sprintf(
    "Info file column names are incorrect (missing columns: %s)",
    paste0(
      c("ID", "Date", "Query")[! c("ID", "Date", "Query") %in% names(info)],
      collapse = ", "
    )
  )
  
	stop(error.message)
}

info <- select(info, ID, Date, Query)
info <- info[match(tree$tip.label, info$ID), ]

if (any(is.na(info))) {
  if (all(tree$tip.label %in% info$ID)) {
    paste.list <- enquote(info$ID[is.na(info$Date) | is.na(info$Query)])
    
    error.message <- sprintf(
      "Info file missing date or query data (for ID: %s)",
       paste0(
         paste.list,
         collapse = ", "
      )
    )
  } else {
    paste.list <- enquote(tree$tip.label[! tree$tip.label %in% info$ID])

    error.message <- sprintf(
      "Info file missing data (ID in tree file not found in info file: %s)",
      paste0(
        paste.list,
        collapse = ", "
      )
    )
  }
  
	stop(error.message)
}

info$Date <- as.numeric(as.Date(info$Date, format = DATE_FMT))
info$Query <- as.numeric(info$Query)

if (any(is.na(info$Query))) {
  stop("Query format of Query column of info file is incorrect (should be 0 for training or 1 for query)")
}

if (any(is.na(info$Date[info$Query == 0]))) {
	stop("Date format of Date column of info file is incorrect (should be yyyy-mm-dd)")
}

# remove zero length branches if they exist
if (any(tree$edge.length < 1e-7)) {
	warning("Tiny length branches detected. This could be caused by duplicate sequences.")
}

# root tree
dates <- info$Date
dates[info$Query == 1] <- NA

rooted.tree <- rtt(tree, dates, opt.tol = 1e-16)

# linear regression
info$Divergence <- node.depth.edgelength(rooted.tree)[1:Ntip(rooted.tree)]

model <- lm(Divergence ~ Date, data = info, subset = Query == 0)
null.model <- lm(Divergence ~ 1, data = info, subset = Query == 0)

est.date <- as.data.frame(do.call(
	rbind,
	lapply(info$Divergence, function(x)
		unlist(inverse.predict(model, x))
	)
))
root.date <- inverse.predict(model, 0)

# make output data frames
data <- data.frame(
	ID = info$ID,
	Date=info$Date,
	Query=info$Query,
	EstimatedDate = as.character(to.Date(est.date$Prediction), format = DATE_FMT),
	EstimatedDate95Low = as.character(to.Date(est.date$`Confidence Limits1`), format = DATE_FMT),
	EstimatedDate95High = as.character(to.Date(est.date$`Confidence Limits2`), format = DATE_FMT),
	stringsAsFactors = FALSE
) %>%
	arrange(desc(Query), Date) %>%
  mutate(Date = as.character(to.Date(Date), format = DATE_FMT))

stats <- data.frame(
	RunID = run.id,
	dAIC = AIC(null.model) - AIC(model),
	EstimatedRootDate = as.character(to.Date(root.date$Prediction), format = DATE_FMT),
	EstimatedRootDate95Low = as.character(to.Date(root.date$`Confidence Limits`[1]), format = DATE_FMT),
	EstimatedRootDate95High = as.character(to.Date(root.date$`Confidence Limits`[2]), format = DATE_FMT),
	EstimatedEvolutionaryRate = coef(model)[[2]],
	Fit = as.numeric(((AIC(null.model) - AIC(model)) > 10) &&
					 	(root.date$`Confidence Limits`[1] < min(info$Date))),
	stringsAsFactors = FALSE
)

# write output (rooted tree, data and stats)
write.tree(rooted.tree, rooted.tree.file)
write.csv(data, data.file, row.names = FALSE)
write.csv(stats, stats.file, row.names = FALSE)
