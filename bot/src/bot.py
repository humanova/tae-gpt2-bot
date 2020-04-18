import praw
import time
import codecs
import random
import confparser

class AbstractAhbapBot():
    
    def __init__(self):
        self.sub = "tamamahbapengelli"
        self.config = confparser.get("config.json")
        self.reply_file = codecs.open("tae_generated_text.txt", "r", "utf-8")
        self.replied_ids_file = codecs.open("replied_ids.txt", "w+", "utf-8")
        self.log_file = codecs.open("log.txt", "w+", "utf-8")

        self.replied_ids = self.replied_ids_file.readlines()

        self.reddit = praw.Reddit(client_id=self.config.reddit_id,
                                    client_secret=self.config.reddit_secret,
                                    password=self.config.reddit_password,
                                    user_agent=self.config.reddit_useragent,
                                    username=self.config.reddit_username)
        
        self.subreddit = self.reddit.subreddit(self.sub)

    
    def start(self):
        '''
        if len(replied_ids) == 0:
            exit()
        '''
        for submission in self.subreddit.stream.submissions():
            if not submission.id in replied_ids:
                gen_text = self.find_reply(submission.title)
                submission.reply(gen_text)
                
                # logging stuff
                add_to_replied(submission.id)
                log_reply(submission, gen_text)
                
            time.sleep(30)


    def find_reply(self, title):
        replies = self.reply_file.readlines()
        keywords = title.lower().split(" ")

        # pick a related text 80%
        # pick a random text 20%
        if random.random() >= 0.20:
            possible_reply_dict = {}        
            for r in replies:
                for k in keywords:
                    if k in r.lower():
                        try:
                            possible_reply_dict[r] += 1
                        except KeyError:
                            possible_reply_dict[r] = 1
            if not len(possible_reply_dict) == 0:
                sorted_reply_dict = {k: v for k, v in sorted(possible_reply_dict.items(), reverse=True, key=lambda item: item[1])}

                # pick randomly from first quarter
                rnd_index = int(len(sorted_reply_dict) / 4)
                return list(sorted_reply_dict.keys())[random.randint(0, rnd_index)]
        # pick a random one    
        random_reply = random.choice(replies)
        return random_reply


    def add_to_replied(id):
        self.replied_ids.append(id)
        self.replied_ids_file.write(id)


    def log_reply(self, submission, reply):
        print(f"replied to {submission.title}")
        self.log_file.write(f"title : {submission.title} , timestamp : {submission.created}")
        self.log_file.write(f"url : {'https://reddit.com' + submission.permalink}")
        self.log_file.write(f"reply : {reply}")
        self.log_file.write("==================")

if __name__ == "__main__":
    bot = AbstractAhbapBot()
    bot.start()

    print("bot stopped")