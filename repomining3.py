import requests
import csv
import time
import os

# Paste your GitHub Token, and Organization name to start the mining. I'm changing the token for the confidentiality
github_token = "ghp_dsknhkajhsfd6IuvoSWFLsajhdfoijsadfGprsdalhsajfjllkasjdflkjdsljfRK2wKUqX"
organization = "CS-CS415-Spring2024"

headers = {
    "Authorization": f"Bearer {github_token}",
    "Accept": "application/vnd.github.v3+json",
}


# Referred this method from stackoverflow. This method is used to mitigate the rate limits.
def safe_get(url, headers, params=None, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 403 and "X-RateLimit-Reset" in response.headers:
                reset_time = int(response.headers["X-RateLimit-Reset"])
                sleep_duration = reset_time - int(time.time()) + 5
                print(f"Rate limit hit. Sleeping for {sleep_duration}s...")
                time.sleep(sleep_duration)
                continue
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed (attempt {attempt + 1}): {e}")
            time.sleep(5)
    return []


def get_all_repositories():
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/orgs/{organization}/repos"
        params = {"per_page": 100, "page": page}
        data = safe_get(url, headers, params)
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos


def get_paginated_data(url):
    all_data = []
    page = 1
    while True:
        params = {"per_page": 100, "page": page}
        data = safe_get(url, headers, params)
        if not data:
            break
        all_data.extend(data)
        page += 1
    return all_data


# def anonymize_authors_by_team(author_map, repo_name, author_name):
#     team_number = int(repo_name.strip("t"))
#     team_key = f"S{team_number}"
#     if team_key not in author_map:
#         author_map[team_key] = {}
#     if author_name not in author_map[team_key]:
#         author_map[team_key][author_name] = (
#             f"{team_key}.{len(author_map[team_key]) + 1}"
#         )
#     return author_map[team_key][author_name]


def analyze_all_repos():
    repos = get_all_repositories()
    contribution_data = []
    author_map = {}
    total_pr_count = 0

    for repo in repos:
        repo_name = repo["name"]
        print(f"Fetching PRs from: {repo_name}")
        pr_url = f"https://api.github.com/repos/{organization}/{repo_name}/pulls"
        pull_requests = get_paginated_data(pr_url + "?state=all")

        for pr in pull_requests:
            pr_number = pr["number"]
            pr_title = pr["title"]
            pr_author = pr["user"]["login"]
            # anonymized_author = anonymize_authors_by_team(
            #     author_map, repo_name, pr_author
            # )
            pr_created_at = pr["created_at"]
            pr_closed_at = pr.get("closed_at", "N/A")
            pr_status = (
                "Merged"
                if pr.get("merged_at")
                else ("Rejected" if pr["state"] == "closed" else pr["state"])
            )

            comments_url = f"https://api.github.com/repos/{organization}/{repo_name}/issues/{pr_number}/comments"
            comments = get_paginated_data(comments_url)
            comment_bodies = (
                " | ".join([c["body"] for c in comments]) if comments else "No Comments"
            )

            commits_url = f"https://api.github.com/repos/{organization}/{repo_name}/pulls/{pr_number}/commits"
            commits = get_paginated_data(commits_url)

            files_url = f"https://api.github.com/repos/{organization}/{repo_name}/pulls/{pr_number}/files"
            files = get_paginated_data(files_url)
            total_additions = sum(f["additions"] for f in files)
            total_deletions = sum(f["deletions"] for f in files)

            contribution_data.append(
                [
                    repo_name,
                    pr_number,
                    pr_title,
                    pr_author,
                    pr_created_at,
                    pr_closed_at,
                    pr_status,
                    len(comments),
                    comment_bodies,
                    len(commits),
                    len(files),
                    total_additions,
                    total_deletions,
                ]
            )
            total_pr_count += 1

    with open(
        "all_repos_pull_request_contributions_Final.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "Repository",
                "PR Number",
                "PR Title",
                "Author",
                "PR Created At",
                "PR Closed At",
                "PR Status",
                "Total Comments",
                "Comment Bodies",
                "Total Commits",
                "Files Changed",
                "Lines Added",
                "Lines Deleted",
            ]
        )
        writer.writerows(contribution_data)

    print(f"\nTotal PRs analyzed: {total_pr_count}")
    print("Data saved to all_repos_pull_request_contributions_Final.csv")


if __name__ == "__main__":
    analyze_all_repos()
