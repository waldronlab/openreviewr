
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

## Using Python to Submit an OpenReview Support Request Form

The [OpenReview Support Request Form](https://openreview.net/group?id=OpenReview.net/Support)
is the form for requesting a new venue on OpenReview. You can submit this form
programmatically with `inst/scripts/post_request_form_note.py`.

### Requirements

* Python 3
* [openreview-py](https://pypi.org/project/openreview-py/)
* (Optional) virtualenv

### Create a config.ini file

Using `inst/scripts/example.ini`, create a `config.ini` and enter the
configurations associated with your venue.

### Create the additional submission options JSON file

Using `inst/scripts/pacific_first_additional_submission_options.json` or the
`atlantic_first_additional_submission_options.json` file, create your additional
submission options file. Note: You must change the registration URL in the JSON
to reflect the correct registration link on Hopin.

### Run the script

To run the script, you must use the email associated with your account in
OpenReview, your password, and the path to your `config.ini`.

    ```
    python3 post_request_form_note.py your.email@gmail.com your_password path/to/config.ini
    ```

When submission is successful, it returns the form note. You will also be able
to view it on OpenReview and receive an email that your request has been
received.
