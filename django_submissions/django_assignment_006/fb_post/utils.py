from fb_post.models import *
from django.db.models import *
from django.db import *
from datetime import datetime
from fb_post.exceptions import *
from fb_post.constants import *


def user_exists(user_id):
    if not(User.objects.filter(id = user_id).exists()):
        raise InvalidUserException

def post_exists(post_id):
    if not(Post.objects.filter(id = post_id).exists()):
        raise InvalidPostException

def comment_exists(comment_id):
    if not(Comment.objects.filter(id = comment_id).exists()):
        raise InvalidCommentException

def post_content_empty(post_content):
    if not(post_content):
        raise InvalidPostContent
        
def comment_content_empty(comment_content):
    if not(comment_content):
        raise InvalidCommentContent

def comment_reply_content_empty(reply_content):
    if not(reply_content):
        raise InvalidReplyContent

def check_reaction_type(reaction_type):
    if reaction_type not in ReactType.values:
        raise InvalidReactionTypeException
        
#task-2 
def create_post(user_id, post_content):
    
    user_exists(user_id)
    post_content_empty(post_content)
    return Post.objects.create(content = post_content,
            posted_by_id = user_id ).id
#task-3
def create_comment(user_id, post_id, comment_content):
    
    user_exists(user_id)
    post_exists(post_id)
    comment_content_empty(comment_content)
    return Comment.objects.create(
            content = comment_content,
            commented_by_id = user_id,
            post_id = post_id
            ).id    
    
#task-4 
def reply_to_comment(user_id, comment_id, reply_content):
    
    user_exists(user_id)
    comment_obj = Comment.objects.filter(id = comment_id).select_related('parent_comment')
    if len(comment_obj) == 0:
        raise InvalidCommentException
    comment = comment_obj[0]
    comment_reply_content_empty(reply_content)
    if comment.parent_comment:
        comment_id = comment.parent_comment.id
    return Comment.objects.create(
                content = reply_content,
                commented_by_id = user_id,
                post_id = comment.post_id,
                parent_comment_id = comment_id
            ).id
        
#task-5
def react_to_post(user_id, post_id, reaction_type):
    user_exists(user_id)
    post_exists(post_id)
    check_reaction_type(reaction_type)
    try:
        reaction_obj = Reaction.objects.get(reacted_by_id = user_id,post_id = post_id)
        if reaction_obj.reaction == reaction_type:
            reaction_obj.delete()
        else:
            reaction_obj.reaction = reaction_type
            reaction_obj.save()
    except Reaction.DoesNotExist:
        Reaction.objects.create(
            post_id = post_id,
            reaction = reaction_type,
            reacted_by_id = user_id
            )
#task-6
def react_to_comment(user_id, comment_id, reaction_type):
    user_exists(user_id)
    comment_exists(comment_id)
    check_reaction_type(reaction_type)
    try:
        reaction_obj = Reaction.objects.get(reacted_by_id = user_id,comment_id = comment_id)
        if reaction_obj.reaction == reaction_type:
            reaction_obj.delete()
        else:
            reaction_obj.reaction = reaction_type
            reaction_obj.save()
    except Reaction.DoesNotExist:
        Reaction.objects.create(
            comment_id = comment_id,
            reaction = reaction_type,
            reacted_by_id = user_id
            )
#rask-7
def get_total_reaction_count():
    return Reaction.objects.aggregate(count = Count('id'))
    
#task-8
def get_reaction_metrics(post_id):
    post_exists(post_id)
    reaction_values_list = Reaction.objects.filter(
        post_id = post_id).values_list(
            'reaction').annotate(
                count =Count('id')).order_by('-count')
    return dict(reaction_values_list)
    
#task-9
def delete_post(user_id, post_id):
    user_exists(user_id)
    post_objs = Post.objects.filter(id = post_id)
    if len(post_objs) == 0:
        raise InvalidPostException
    post_obj = post_objs[0]
    if post_obj.posted_by_id == user_id:
        post_obj.delete()
    else:
        raise UserCannotDeletePostException
        
#task-10
def get_posts_with_more_positive_reactions():
    
    positive = Count('reaction',filter=Q(reaction__reaction__in=['THUMBS-UP', 'LIT', 'LOVE', 'HAHA', 'WOW']))
    negative = Count('reaction',filter=Q(reaction__reaction__in =['SAD', 'ANGRY', 'THUMBS-DOWN']))
    return list(Post.objects.values_list(
        'id',flat=True).annotate(
            positive_reactions = positive,negative_reactions = negative).filter(positive_reactions__gt=F('negative_reactions')))
#task-11
def get_posts_reacted_by_user(user_id):
    user_exists(user_id)
    return Post.objects.values_list('id',flat = True).filter(
        reaction__in = Reaction.objects.filter(reacted_by_id = user_id)
        ).distinct()
        
#task-12
def get_reactions_to_post(post_id):
    post_exists(post_id)
    reactions = Reaction.objects.values_list('reacted_by_id','reacted_by__name','reacted_by__profile_pic','reaction').filter(post_id = post_id)
    reaction_list = []
    for reaction in reactions:
        reaction_list.append({"user_id": reaction[0], "name": reaction[1], "profile_pic": reaction[2], "reaction": reaction[3]})
    return reaction_list

#task-15
def get_replies_for_comment(comment_id):
    comment_exists(comment_id)
    comment_objs = Comment.objects.filter(parent_comment_id = comment_id).select_related('commented_by')
    reply_comments_list = []
    for comment in comment_objs:
        reply_comments_list.append({
            "comment_id": comment.id,
            "commenter": {
                "user_id": comment.commented_by_id,
                "name": comment.commented_by.name,
                "profile_pic": comment.commented_by.profile_pic
            },
            "commented_at": datetime.strftime(comment.commented_at,"%Y-%m-%d %H:%M:%S.%f"),
            "comment_content": comment.content
        })
    return reply_comments_list

def post_object_reactions(post_obj):
    post_reaction_list = []
    for reaction in post_obj.post_reactions:
        if reaction.reaction not in post_reaction_list:
            post_reaction_list.append(reaction.reaction)
    return post_reaction_list

def post_details(post_obj):
    comments_list = []
    parents_comment_list = []
    all_reply_comments_list = []
    for comment in post_obj.comments:
        if comment.parent_comment_id == None:
            parents_comment_list.append(comment)
        else:
            all_reply_comments_list.append(comment)
    for comment in parents_comment_list:
        comments_list.append(get_parent_comment(comment,all_reply_comments_list))
    
    return {
        "post_id": post_obj.id,
        "posted_by": {
            "name": post_obj.posted_by.name,
            "user_id": post_obj.posted_by_id,
            "profile_pic": post_obj.posted_by.profile_pic
        },
        "posted_at": datetime.strftime(post_obj.posted_at,"%Y-%m-%d %H:%M:%S.%f"),
        "post_content": post_obj.content,
        "reactions": {
            "count": len(post_obj.post_reactions),
            "type": post_object_reactions(post_obj)
        },
        "comments": comments_list,
        "comments_count": len(parents_comment_list)
    }
    
#task-13
def get_post(post_id):
    post_exists(post_id)
    queryset = Comment.objects.select_related('commented_by').prefetch_related(
                    Prefetch('reaction_set',to_attr = 'comment_reactions'))
    post_obj =  Post.objects.filter(id = post_id).select_related('posted_by').prefetch_related(
        Prefetch('reaction_set',to_attr = 'post_reactions'),
        Prefetch('comment_set',queryset = queryset,to_attr = 'comments'))
    return post_details(post_obj[0])
    
#task-14    
def get_user_posts(user_id):
    user_exists(user_id)
    queryset = Comment.objects.select_related('commented_by').prefetch_related(
                    Prefetch('reaction_set',to_attr = 'comment_reactions'))
    post_objs =  Post.objects.filter(posted_by_id = user_id).select_related('posted_by').prefetch_related(
        Prefetch('reaction_set',to_attr = 'post_reactions'),
        Prefetch('comment_set',queryset = queryset,to_attr = 'comments'))
    posts_list = []
    for post in post_objs:
        posts_list.append(post_details(post))
    return posts_list

def comment_object_reactions(comment_obj):
    comment_reaction_list = []
    for reaction in comment_obj.comment_reactions:
        if reaction.reaction not in comment_reaction_list:
            comment_reaction_list.append(reaction.reaction)
    return comment_reaction_list

def get_parent_comment(comment,comment_objs):
    reply_comments = []
    for comment_obj in comment_objs:
        if comment.id == comment_obj.parent_comment_id:
            reply_comments.append(comment_obj)
    return {
            "comment_id": comment.id,
            "commenter": {
                "user_id": comment.commented_by_id,
                "name": comment.commented_by.name,
                "profile_pic": comment.commented_by.profile_pic
            },
            "commented_at": datetime.strftime(comment.commented_at,"%Y-%m-%d %H:%M:%S.%f"),
            "comment_content": comment.content,
            "reactions": {
                    "count": len(comment.comment_reactions),
                    "type": comment_object_reactions(comment)
                },
            "replies_count": len(reply_comments),
            "replies":get_child_comments(reply_comments)
    }

def get_child_comments(comment_objs):
    replies_comment_list = []
    for comment in comment_objs:
        replies_comment_list.append({
            "comment_id": comment.id,
            "commenter": {
                "user_id": comment.commented_by_id,
                "name": comment.commented_by.name,
                "profile_pic": comment.commented_by.profile_pic
            },
            "commented_at": datetime.strftime(comment.commented_at,"%Y-%m-%d %H:%M:%S.%f"),
            "comment_content": comment.content,
            "reactions": {
                "count": len(comment.comment_reactions),
                "type": comment_object_reactions(comment)
            }
        })
    return replies_comment_list
    
