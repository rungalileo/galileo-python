/**
 * Finds an open Dependabot PR from a workflow_run event.
 * Iterates all associated PRs (not just the first) to handle
 * cases where multiple PRs are linked to a single workflow run.
 *
 * @param {object} options
 * @param {object} options.github - The octokit github client
 * @param {object} options.context - The actions context
 * @param {object} options.core - The actions core toolkit
 * @returns {Promise<{prNumber: number, pr: object} | null>}
 */
module.exports = async function getDependabotPr({ github, context, core }) {
  const workflowRun = context.payload.workflow_run;
  const prs = workflowRun.pull_requests || [];

  if (prs.length === 0) {
    core.info('No pull requests associated with this workflow run.');
    return null;
  }

  for (const candidate of prs) {
    const { data: pr } = await github.rest.pulls.get({
      owner: context.repo.owner,
      repo: context.repo.repo,
      pull_number: candidate.number
    });
    if (pr.user?.login === 'dependabot[bot]' && pr.state === 'open') {
      return { prNumber: candidate.number, pr };
    }
  }

  return null;
};
