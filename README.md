
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

## Previous work

Some of the code is based on: https://github.com/kevinrue/openreview-r, and the
basilisk documenation: https://bioconductor.org/packages/release/bioc/html/basilisk.html.
