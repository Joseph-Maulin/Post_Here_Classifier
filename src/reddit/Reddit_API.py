
import praw
import os
import datetime


class Reddit_API:

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


    def get_user_comments(self, user, limit=5):
        """
            Get user comments
        """
        return list(self.connection.redditor(user).comments.new(limit=limit))

    def get_user_posts(self, user, limit=5):
        """
            Get user submissions
        """
        return list(self.connection.redditor(user).submissions.new(limit=limit))

    def get_post_comments(self, post, limit=10):

        comments = []

        post.comment_sort = "best"
        post.comment_limit = str(limit)
        for y in post.comments:
            if isinstance(y, praw.models.reddit.comment.Comment):
                comments.append(y)

        return comments

    def get_submission(self, post_id):
        """
            Get subbmission from id
        """
        submission = self.connection.submission(post_id)
        submission.comments.replace_more(limit=None)
        return submission


    def get_comments_for_comment(self, comment, levels=2):
        """
            Get comments above and x levels below
        """
        return self.get_comments_above(comment) + self.get_comments_below(comment, levels=levels)

    def get_comments_above(self, comment):
        """
            Get Parent comments
        """
        comment_chain = []

        while comment.parent():
            comment.refresh()
            comment = comment.parent()
            if not isinstance(comment, praw.models.reddit.comment.Comment):
                break
            comment_chain.insert(0, comment.body)

        return comment_chain


    def get_comments_below(self, comment, levels=2):
        """
            Get comments below
        """

        comment.refresh()
        return [comment.body] + self.build_comment_group(list(comment.replies), levels)


    def build_comment_group(self, comments, i):

        if not comments or i==0:
            return None

        else:
            comment_group = []
            for x in comments:
                x.refresh()
                comment_group += [x.body]
                if x.replies:
                    replies = [self.build_comment_group(list(x.replies), i-1)]
                    if replies[0]:
                        comment_group += replies


            return comment_group




if __name__ == "__main__":
    r = Reddit_API()

    for x in r.get_user_posts("masktoobig"):
        print(x.title)
        print(x.created_utc)
        print(datetime.datetime.fromtimestamp(x.created_utc))
        for y in r.get_post_comments(x):
            print(y.body)


    # comment = r.get_user_comments("Bloba_Fett", limit=2)[1]
    # comment.refresh()
    # comment.comments.replace_more(limit=None)



    # for x in r.get_comments(comment):
    #     print(x)
    #     print("\n")




    # comment_queue = submission.comments[:]
    # while comment_queue:
    #     comment = comment_queue.pop(0)
    #     print(comment.body)
    #     comment_queue.extend(comment.replies)



    # submission = r.get_submission("ld29nb")
    # print(submission.title)
    # print(submission.selftext)
    # print(submission.num_comments)

    # https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
    # for x in r.get_user_submissions("grilled_cheezeee", limit = 5):
    #     print(x.title)
    #     print(x.selftext)
    #     print("\n")

    # https://praw.readthedocs.io/en/latest/code_overview/models/comment.html
    # for x in r.get_user_comments("grilled_cheezeee"):
    #     print(x.body)
    #     print(x.submission)

    # posts = r.get_subreddit_top_k_posts("politics", 1)
    # for x in posts:
    #     print(x.title)
    #     print(x.selftext)
    #     print(x.created_utc)
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
