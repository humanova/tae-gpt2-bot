# 2020 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details
import praw
import time
import codecs
import requests
import random
import confparser

API_URL = None 

class AbstractAhbapBot():
    
    def __init__(self):
        self.sub_list = [
            "tamamahbapengelli",
            "turkishbruhmemes",
            "shitposttc"
        ] 
        self.day_delta = 1
        self.min_score = -1
        self.start_timestamp = time.time() - (86400 * self.day_delta)
        self.config = confparser.get("../config.json")
        self.reply_file = codecs.open("tae_generated_text.txt", "r", "utf-8")
        self.replied_ids_file = codecs.open("replied_ids.txt", "r", "utf-8")

        self.replied_ids = [id.replace("\n", "") for id in self.replied_ids_file.readlines()]
        self.replies = self.reply_file.readlines()
        
        self.replied_ids_file.close()
        self.reply_file.close()
        
        self.reddit = praw.Reddit(client_id=self.config.reddit_id,
                                    client_secret=self.config.reddit_secret,
                                    password=self.config.reddit_password,
                                    user_agent=self.config.reddit_useragent,
                                    username=self.config.reddit_username)
        
        self.subreddit = self.reddit.subreddit("+".join(self.sub_list))

    def start(self):
        '''
        if len(self.replied_ids) == 0:
            exit()
        '''
        for submission in self.subreddit.stream.submissions():
            if not submission.id in self.replied_ids:
                if submission.created > self.start_timestamp:
                    if submission.score > self.min_score:
                        # sleep before replying
                        time.sleep(random.randint(1000, 1500))
                        gen_text = self.find_reply(submission.title)
                        try:
                            submission.reply(gen_text)
                        except praw.exceptions.APIException:
                            print("sleeping 5 minutes due to ratelimit")
                            time.sleep(300)
                            submission.reply(gen_text)

                        # logging stuff
                        self.add_to_replied(submission.id)
                        self.log_reply(submission, gen_text)
                        
                        # if it's night sleep longer to look like a "human redditor"
                        if time.localtime().tm_hour >= 2 and time.localtime().tm_hour <= 9:
                            time.sleep(25200) # 7 hours
                        else:
                            time.sleep(random.randint(400, 900))
            
    def find_reply(self, title):
        # use API to generate reply IF defined
        if API_URL:
            content = {"title" : title}
            try:
                r = requests.post(f"{API_URL}/gen_reply", timeout=4.0, json=content)
                data = r.json()
                if data['success']:
                    reply = data['reply'].replace("<bs>", '\n')
                    return reply
            except Exception as e:
                print(f"error in /gen_reply request : {e}")

        # pick a related text 80%
        # pick a random text 20%
        if random.random() >= 0.20:
            keywords = title.lower().split(" ")
            possible_reply_dict = {}        
            for r in self.replies:
                for k in keywords:
                    if k in r.lower():
                        try:
                            possible_reply_dict[r] += 1
                        except KeyError:
                            possible_reply_dict[r] = 1
            if not len(possible_reply_dict) == 0:
                sorted_reply_dict = {k: v for k, v in sorted(possible_reply_dict.items(), reverse=True, key=lambda item: item[1])}
                # pick randomly from first top 60%
                rnd_index = int(len(sorted_reply_dict) / 1.6)
                random_reply = list(sorted_reply_dict.keys())[random.randint(0, rnd_index)].replace("<bs>","\n")
                return random_reply
        # pick a random one    
        random_reply = random.choice(self.replies).replace("<bs>","\n")
        return random_reply

    def add_to_replied(self, id):
        self.replied_ids.append(id)

        self.replied_ids_file = codecs.open("replied_ids.txt", "a", "utf-8")
        self.replied_ids_file.write(f"{id}\n")
        self.replied_ids_file.close()

    def log_reply(self, submission, reply):
        print(f"replied to {submission.id} from u/{submission.author.name}")

        self.log_file = codecs.open("log.txt", "a", "utf-8")
        self.log_file.write(f"title : {submission.title} , timestamp : {submission.created}\n")
        self.log_file.write(f"url : {'https://reddit.com' + submission.permalink}\n")
        self.log_file.write(f"reply : {reply}")
        self.log_file.write("==================\n")
        self.log_file.close()


if __name__ == "__main__":
    bot = AbstractAhbapBot()
    bot.start()
    print("bot stopped")