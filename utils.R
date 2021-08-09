utils::globalVariables(c("."))
#' Get Invitation ID
#'
#' \code{getInvitationId} gets invitation ids for a determined regex.
#' Currently, only the first 1000 items.
#'
#' @param client Client object
#' @param regex Character vector of length 1.
#'
#' @return A character vector of all invitations.
#'
#' @importFrom magrittr %>%
#'
#' @export
#'
getInvitationId <- function(client, regex) {
    invitations <- client$get_invitations(regex = regex) %>%
        vapply(., function(x) x$id, character(1))
    invitations
}
