import os
import requests
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/execution.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def fetch_and_score_posts(subreddit_name, limit=100, top_k=5):
    logging.info(f"Fetching recent posts from r/{subreddit_name} using public API...")
    
    # Reddit's public API endpoint
    url = f"https://www.reddit.com/r/{subreddit_name}/new.json?limit={limit}"
    
    # User-Agent schema
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            logging.error(f"Failed to fetch data from r/{subreddit_name}. Status Code: {response.status_code}")
            return []

        data = response.json()
        children = data.get("data", {}).get("children", [])
        logging.info(f"Retrieved {len(children)} posts from r/{subreddit_name}.")
        
        posts = []
        for child in children:
            post = child.get("data", {})
            
            # Extract relevant fields
            title = post.get("title", "")
            url = post.get("url", "")
            score = post.get("score", 0)
            num_comments = post.get("num_comments", 0)
            created_utc = post.get("created_utc", 0)
            
            # Extract thumbnail
            thumbnail = post.get("thumbnail", "")
            if thumbnail in ["self", "default", "nsfw", ""] or not thumbnail.startswith("http"):
                thumbnail = None
                
            # Try to get higher res preview if available
            preview = post.get("preview", {})
            if "images" in preview:
                try:
                    source_url = preview["images"][0]["source"]["url"]
                    # Reddit encodes & as &amp; in JSON, need to fix it
                    thumbnail = source_url.replace("&amp;", "&")
                except (KeyError, IndexError):
                    pass

            # Calculate simple engagement score
            engagement_score = score + num_comments
            
            posts.append({
                "title": title,
                "url": url,
                "thumbnail": thumbnail,
                "score": score,
                "comments": num_comments,
                "engagement": engagement_score,
                "created_utc": datetime.fromtimestamp(created_utc).strftime('%Y-%m-%d %H:%M:%S')
            })
            
        # Sort by engagement score descending
        posts.sort(key=lambda x: x["engagement"], reverse=True)
        
        # Return top K
        return posts[:top_k]
        
    except Exception as e:
        logging.exception(f"Exception fetching from r/{subreddit_name}: {e}")
        return []

def main():
    logging.info("--- Starting Reddit Scraper Execution ---")
    subreddits = ["n8n", "automation"]
    
    # Dictionary to store all results for intermediate file
    all_results = {}

    for sub in subreddits:
        top_posts = fetch_and_score_posts(sub)
        all_results[sub] = top_posts

        logging.info(f"--- Top 5 Posts in r/{sub} (by Engagement) ---")
        if not top_posts:
            logging.warning(f"No posts found for r/{sub} or error occurred.")
            continue
            
        for i, post in enumerate(top_posts, 1):
            msg = (
                f"\n{i}. {post['title']}\n"
                f"   Url: {post['url']}\n"
                f"   Engagement: {post['engagement']} (Score: {post['score']}, Comments: {post['comments']})\n"
                f"   Date: {post['created_utc']}"
            )
            logging.info(msg)

    # Save intermediate results to .tmp
    try:
        os.makedirs(".tmp", exist_ok=True)
        output_path = os.path.join(".tmp", "latest_reddit_posts.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        logging.info(f"Intermediate results saved to {output_path}")
    except Exception as e:
        logging.error(f"Failed to save intermediate results: {e}")

    logging.info("--- Execution Finished ---")

if __name__ == "__main__":
    main()
