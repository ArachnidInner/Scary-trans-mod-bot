import praw
import time
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()

class gaynessbot:
    def __init__(self):
        # Does the reddit thingy
        self.reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            username=os.getenv('REDDIT_USERNAME'),
            password=os.getenv('REDDIT_PASSWORD'),
            user_agent='ModBot/1.0'
        )
        
        # Sub to control (kinkyyyyyyy)
        self.subreddit_name = os.getenv('SUBREDDIT_NAME')
        
        # Flair to check
        self.target_flair = os.getenv('TARGET_FLAIR')
    
    def scan_and_moderate(self):
        """
        Scan recent posts with specific flair and moderate them
        """
        try:
            # Get subreddit instance
            subreddit = self.reddit.subreddit(self.subreddit_name)
            
            # Iterate through new posts
            for submission in subreddit.new(limit=500):
                # Check if post has the target flair and isn't approved
                if (submission.link_flair_text == self.target_flair and 
                    not submission.approved):
                    
                    # Remove the post for being meanie
                    submission.mod.remove()
                    
                    # Send modmail to alert the scary queer overlords of someone being naughty :3
                    subreddit.message(
                        subject=f'Post Removed - {self.target_flair} Flair',
                        message=f'Removed post: {submission.title}\n\n'
                               f'Link: {submission.permalink}\n'
                               f'Reason: Unapproved post with {self.target_flair} flair'
                    )
                    
                    print(f'Removed post: {submission.title} and {submission.permalink}')
        
        except Exception as e:
            print(f'Error in moderation process: {e}')
    
    def run(self):
        """
        Run the bot continuously
        """
        while True:
            self.scan_and_moderate()
            # Wait for 5 mins before next scan
            time.sleep(300)

def main():
    bot = gaynessbot()
    bot.run()

if __name__ == '__main__':
    main()
