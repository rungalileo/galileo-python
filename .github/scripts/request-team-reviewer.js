/**
 * Requests a review from a random member of a specified team.
 * Skips if a review has already been requested (idempotent).
 *
 * @param {object} options
 * @param {object} options.github - The octokit github client
 * @param {object} options.context - The actions context
 * @param {object} options.core - The actions core toolkit
 * @param {number} options.prNumber - The pull request number
 * @param {string} options.teamSlug - The team slug (e.g., "product", "platform", "ui")
 * @returns {Promise<void>}
 */
module.exports = async function requestProductReviewer({
  github,
  context,
  core,
  prNumber,
  teamSlug = 'product'
}) {
  const owner = context.repo.owner;
  const repo = context.repo.repo;

  // Get all members of the specified team (paginated)
  let teamMembers;
  try {
    const members = await github.paginate(github.rest.teams.listMembersInOrg, {
      org: 'rungalileo',
      team_slug: teamSlug,
      per_page: 100
    });
    teamMembers = members.map((m) => m.login);
  } catch (error) {
    core.setFailed(`Failed to fetch team members: ${error.message}`);
    return;
  }

  if (teamMembers.length === 0) {
    core.setFailed(`No members found in rungalileo/${teamSlug} team.`);
    return;
  }

  const teamMemberSet = new Set(teamMembers);

  // Skip if a team member already has a pending review request
  const { data: reviewRequests } =
    await github.rest.pulls.listRequestedReviewers({
      owner,
      repo,
      pull_number: prNumber
    });
  const hasPendingTeamReview = reviewRequests.users.some((u) =>
    teamMemberSet.has(u.login)
  );
  if (hasPendingTeamReview) {
    core.info(
      `PR #${prNumber} already has a pending rungalileo/${teamSlug} team review request - skipping.`
    );
    return;
  }

  // Skip if a team member has already submitted a review (paginated)
  const reviews = await github.paginate(github.rest.pulls.listReviews, {
    owner,
    repo,
    pull_number: prNumber,
    per_page: 100
  });
  const hasTeamReview = reviews.some(
    (r) => r.user?.login && teamMemberSet.has(r.user.login)
  );
  if (hasTeamReview) {
    core.info(
      `PR #${prNumber} already has a review from a rungalileo/${teamSlug} team member - skipping.`
    );
    return;
  }

  // Select a random team member
  const randomMember =
    teamMembers[Math.floor(Math.random() * teamMembers.length)];
  core.info(`Selected random reviewer: ${randomMember}`);

  // Request review from the selected member
  try {
    await github.rest.pulls.requestReviewers({
      owner,
      repo,
      pull_number: prNumber,
      reviewers: [randomMember]
    });
    core.info(
      `Successfully requested review from ${randomMember} (rungalileo/${teamSlug}) for PR #${prNumber}`
    );
  } catch (error) {
    core.setFailed(`Failed to request review: ${error.message}`);
  }
};
