# Contributing to our project

This file outlines how to contribute to this repository. We welcome any input, feedback, bug reports, and contributions via GitHub issues and Pull Requests.

### Fixing typos

Small typos or grammatical errors in documentation may be edited directly using
the GitHub web interface, so long as the changes are made in the _source_ file.

*  YES: you edit a roxygen comment in a `.R` file below `R/`.
*  NO: you edit an `.Rd` file below `man/`.

### Prerequisites

Before you make a substantial pull request, you should always file an issue and
make sure someone from the team agrees that it's a problem. If you've found a
bug, create an associated issue and illustrate the bug with a minimal 
reproducible example.

### Pull request process

*  We recommend that you create a Git branch for each pull request (PR).  
*  New R code should follow the tidyverse [style guide](http://style.tidyverse.org).
*  We use [roxygen2](https://cran.r-project.org/package=roxygen2), with
[Markdown syntax](https://cran.r-project.org/web/packages/roxygen2/vignettes/rd-formatting.html), 
for documenting R code.  
*  New Python code should use Black formatting, which can be applied by installing and running [Black](https://github.com/psf/black) on the local directory
*  We Python code should be documented according to the [PEP 257 standard](https://www.python.org/dev/peps/pep-0257/) for docstring conventions.

### Code of Conduct

Please note that this project is released with a [Contributor Code of
Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to
abide by its terms.

### Footnote

This file was inspired by the CONTRIBUTING.md file in the dplyr project, available here [dplyr CONTRIBUTING.md](https://github.com/tidyverse/dplyr/blob/master/.github/CONTRIBUTING.md).
