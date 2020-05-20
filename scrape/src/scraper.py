# 2020 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details
import praw
import confparser

class CommentScraper:

    def __init__(self, subreddit: str, limit: int):
        self.sub = subreddit
        self.limit = limit
        self.config = confparser.get("../config.json")

        self.reddit = praw.Reddit(client_id=self.config.reddit_id,
                                    client_secret=self.config.reddit_secret,
                                    password=self.config.reddit_password,
                                    user_agent=self.config.reddit_useragent,
                                    username=self.config.reddit_username)

    def get_comments(self):
        subreddit = self.reddit.subreddit(self.sub)
        hot_posts = subreddit.hot(limit=self.limit)
        
        idx = 0
        comment_data = []
        for post in hot_posts:
            if post.score >= 5 and post.num_comments >= 1:
                for c in post.comments.list():
                    try:
                        data = {
                            "text": c.body,
                            "url": "https://reddit.com" + c.permalink,
                            "id": c.id,
                            "upvote": c.score,
                            "timestamp": c.created}
                        comment_data.append(data)
                    except AttributeError:
                        pass
            idx+=1
            if idx % 10 == 0:
                print(f"scraping comments : {idx}/?")
        return comment_data