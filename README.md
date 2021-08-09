
# openreviewr

<!-- badges: start -->
<!-- badges: end -->

Openreviewer is an R wrapper package for the [openreview python client](https://openreview-py.readthedocs.io/en/latest/index.html).

## Installation

``` r
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
BiocManager::install("waldronlab/openreviewr", dependencies = TRUE, build_vignettes = FALSE)
```

## Example

As a guest user (no username and password required):

``` r
library(openreviewr)

# Create Client
client <- getClient(username = NULL, password = NULL)

# Use the client to retrieve invitation ids from the Microbiome-VIF
invitations <- client$get_invitations(regex = "Microbiome-VIF.org/.*")
invitations_ids <- vapply(invitations, function(x) x$id, character(1))
head(invitations_ids)
#> [1] "Microbiome-VIF.org/2021/Forum/Round1/-/Recruit_Reviewers"                 
#> [2] "Microbiome-VIF.org/2021/Forum/Round1/Reviewers/-/Assignment_Configuration"
#> [3] "Microbiome-VIF.org/2021/Forum/Round1/-/Submission"
```

<sup>Created on 2021-08-09 by the [reprex package](https://reprex.tidyverse.org) (v2.0.1)</sup>

## Previous work

Some of the code is based on: https://github.com/kevinrue/openreview-r, and the
basilisk documenation: https://bioconductor.org/packages/release/bioc/html/basilisk.html.
