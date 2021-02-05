
import praw
import os
from dotenv import load_dotenv
from pathlib import Path
import datetime


class Reddit_API:

    env_path = Path("./.env")
    load_dotenv(dotenv_path = env_path)

    def __init__(self):
        self.connection = self.set_connection()

    def set_connection(self):
        return praw.Reddit(client_id = os.getenv("REDDIT_CLIENT_ID"),
                                      client_secret = os.getenv("REDDIT_CLIENT_SECRET"),
                                      user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36')

    def get_subreddit_top_k_posts(self, subreddit, k = 5):
        """
            Get the top hot post objects for a given subreddit
        """
        page = self.connection.subreddit(subreddit)
        return page.hot(limit = k)




if __name__ == "__main__":
    r = Reddit_API()

    posts = r.get_subreddit_top_k_posts("politics", 1)
    for x in posts:
        print(x.title)
        print(x.selftext)
        print(x.created_utc)
        # print(dir(x))


# subreddit post attributes

# ['STR_FIELD', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__gt__', '__hash__', '__init__',
# '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
# '__weakref__', '_chunk', '_comments_by_id', '_fetch', '_fetch_data', '_fetch_info', '_fetched', '_kind', '_reddit', '_reset_attributes', '_safely_add_arguments', '_url_parts', '_vote',
# 'all_awardings', 'allow_live_comments', 'approved_at_utc', 'approved_by', 'archived', 'author', 'author_flair_background_color', 'author_flair_css_class', 'author_flair_richtext',
# 'author_flair_template_id', 'author_flair_text', 'author_flair_text_color', 'author_flair_type', 'author_fullname', 'author_patreon_flair', 'author_premium', 'award', 'awarders',
# 'banned_at_utc', 'banned_by', 'can_gild', 'can_mod_post', 'category', 'clear_vote', 'clicked', 'comment_limit', 'comment_sort', 'comments', 'content_categories', 'contest_mode',
# 'created', 'created_utc', 'crosspost', 'delete', 'disable_inbox_replies', 'discussion_type', 'distinguished', 'domain', 'downs', 'downvote', 'duplicates', 'edit', 'edited',
# 'enable_inbox_replies', 'flair', 'fullname', 'gild', 'gilded', 'gildings', 'hidden', 'hide', 'hide_score', 'id', 'id_from_url', 'is_crosspostable', 'is_meta', 'is_original_content',
# 'is_reddit_media_domain', 'is_robot_indexable', 'is_self', 'is_video', 'likes', 'link_flair_background_color', 'link_flair_css_class', 'link_flair_richtext', 'link_flair_text',
# 'link_flair_text_color', 'link_flair_type', 'locked', 'mark_visited', 'media', 'media_embed', 'media_only', 'mod', 'mod_note', 'mod_reason_by', 'mod_reason_title', 'mod_reports',
#  'name', 'no_follow', 'num_comments', 'num_crossposts', 'num_reports', 'over_18', 'parent_whitelist_status', 'parse', 'permalink', 'pinned', 'post_hint', 'preview', 'pwls', 'quarantine',
#  'removal_reason', 'removed_by', 'removed_by_category', 'reply', 'report', 'report_reasons', 'save', 'saved', 'score', 'secure_media', 'secure_media_embed', 'selftext', 'selftext_html',
#  'send_replies', 'shortlink', 'spoiler', 'stickied', 'subreddit', 'subreddit_id', 'subreddit_name_prefixed', 'subreddit_subscribers', 'subreddit_type', 'suggested_sort', 'thumbnail',
#  'thumbnail_height', 'thumbnail_width', 'title', 'top_awarded_type', 'total_awards_received', 'treatment_tags', 'unhide', 'unsave', 'ups', 'upvote', 'upvote_ratio', 'url', 'user_reports',
#   'view_count', 'visited', 'whitelist_status', 'wls']


# env_path = Path("./.env")
# load_dotenv(dotenv_path = env_path)
#
#
# r = praw.Reddit(client_id = os.getenv("REDDIT_CLIENT_ID"),
#                 client_secret = os.getenv("REDDIT_CLIENT_SECRET"),
#                 user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36')
#
# page = r.subreddit('politics')
# top_posts = page.hot(limit = 5)
# for post in top_posts:
#     # print(post.title, post.ups)
#     print(post)
