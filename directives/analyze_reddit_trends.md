# Directive: Analyze Reddit Trends

## Goal
Fetch and analyze the most recent posts from specified subreddits to identify high-engagement content.

## Inputs
- Subreddits: `r/n8n`, `r/automation`
- Limit: 100 recent posts per subreddit
- Top K: 5 posts per subreddit

## Tools
- `execution/fetch_reddit_posts.py`

## Output
- A list of the top 5 posts for each subreddit based on engagement score (upvotes + comments).
- Each entry should include: Title, URL, Score, Comments, Date.
