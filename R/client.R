#' Get OpenReview Client
#'
#' \code{getClient} starts a client for openreview. The code is based on:
#' \url{https://github.com/kevinrue/openreview-r/blob/main/dev/test.R} and
#' following the instructions in the documentation of the \code{basilisk}
#' package.
#'
#' Since user credentials are confidential, it's recommended to get the values
#' from environment variables rather than directly typing in the console or
#' script. \link{Sys.getenv} can be useful to get the credential values from
#' environment variables.
#'
#' @param username A character vector of length 1.
#' @param password A character vector of length 1.
#'
#' @return
#' An instance of the openreview client. Class: 'openreview.openreview.Client',
#' 'python.builtin.object'
#'
#' @export
#'
#' @examples
#'
#' \dontrun{
#' username = Sys.getenv("OPENREVIEW_USERNAME")
#' password = Sys.getenv("OPENREVIEW_PASSWORD")
#' client = getClient(username = username, password = password)
#' invitations = getInvitationId(client = client, regex = "Microbiome-VIF.org/.*")
#' invitations
#' }
#'
getClient <- function(username, password) {
    proc <- basilisk::basiliskStart(openreviewEnvironment)
    on.exit(basilisk::basiliskStop(proc))

    startClient <- basilisk::basiliskRun(proc, function(arg1, arg2) {

        openreview <- reticulate::import("openreview")
        output <- openreview$Client(baseurl = "https://api.openreview.net",
                                    username = arg1, password = arg2)
        output
    }, arg1 = username, arg2 = password)
    startClient
}
