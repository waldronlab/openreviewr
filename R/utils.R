utils::globalVariables(c("."))
#' Get Invitation IDs
#'
#' \code{getInvitationIds} gets invitation ids for a determined regex.
#' Currently, only the first 1000 items.
#'
#' @param client Client object
#' @param regex Character vector of length 1.
#' @param expired Boolean If TRUE, includes expired invitations. Default FALSE.
#'
#' @return A character vector of all invitations.
#'
#' @importFrom magrittr %>%
#'
#' @export
#'
getInvitationIds <- function(client, regex, expired = FALSE) {
    invitations <- client$get_invitations(regex = regex, expired = expired) %>%
        vapply(., function(x) x$id, character(1))
    invitations
}

#' Get Submissions
#'
#' \code{getSubmissions} gets submissions for an invitation id.
#' Currently, only the first 1000 items.
#'
#' @param client Client object
#' @param invitation Character vector of length 1.
#'
#' @return A character vector of all submissions for the invitation id.
#'
#' @export
#'
getSubmissions <- function(client, invitation) {
    submissions <- client$get_notes(invitation = invitation)
}
