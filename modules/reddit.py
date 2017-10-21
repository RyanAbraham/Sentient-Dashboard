# Delivers reddit posts from a subreddit that matches a chosen emotion
import indicoio
import praw
import json
import modules.config as config
from collections import Counter

indicoio.config.api_key = config.indico_api_key
MAX_POSTS, MAX_COMMENTS = 10, 2

def fetchposts(subreddit, target_emotion):
    submissions = {}
    return_data = {}
    return_data['submissions'] = []

    reddit = praw.Reddit(client_id='Us-byLFTjQmSJQ',
                         client_secret=config.reddit_client_secret,
                         user_agent='python:com.hackharvard.sentient-dashboard:v1.0')

    for submission in reddit.subreddit(subreddit).hot(limit=MAX_POSTS):
        emotion_sum = Counter(indicoio.emotion(submission.title))
        for counter, comment in enumerate(submission.comments):
            if counter >= MAX_COMMENTS:
                break
            if comment != "[removed]": # Ignore removed comments
                emotion_sum.update(Counter(indicoio.emotion(comment.body)))
            else:
                counter -= 1
        # Average the emotion values
        for emotion in emotion_sum:
            emotion_sum[emotion] /= counter+1
        submissions[submission.title] = [emotion_sum, submission.shortlink]

    for sub in submissions:
        submissions[sub][0] = submissions[sub][0][target_emotion]

    for post in reversed(sorted(submissions, key=submissions.get)):
        return_data['submissions'].append({'title': post, 'score': submissions[post][0], 'shortlink': submissions[post][1]})
    return json.dumps(return_data)

