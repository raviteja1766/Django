from fb_post.models import *
from django.db.models import *
from django.db import *
from datetime import datetime
from fb_post.exceptions import *
from fb_post.constants import *
import operator


def is_valid_user(user_id,member = False):
    
    try:
        user_obj = User.objects.get(id = user_id)
    except User.DoesNotExist:
        if member:
            raise InvalidMemberException
        raise InvalidUserException
    return user_obj

def is_valid_post(post_id):
    
    try:
        post_obj = Post.objects.get(id = post_id)
    except Post.DoesNotExist:
        raise InvalidPostException
    return post_obj

def is_valid_comment(comment_id):
    
    try:
        comment_obj = Comment.objects.get(id = comment_id)
    except Comment.DoesNotExist:
        raise InvalidCommentException
    return comment_obj
    
def is_valid_post_content(post_content):
    if not(post_content):
        raise InvalidPostContent
        
def is_valid_comment_content(comment_content):
    if not(comment_content):
        raise InvalidCommentContent

def is_valid_reply_comment_content(reply_content):
    if not(reply_content):
        raise InvalidReplyContent

def is_valid_reaction_type(reaction_type):
    if reaction_type not in ReactType.values:
        raise InvalidReactionTypeException

def is_valid_group_name(group_name):
    if not(group_name):
        raise InvalidGroupNameException

def is_valid_members(member_ids):
    
    user_ids = User.objects.filter(id__in=member_ids).values_list('id',flat = True)
    if operator.ne(len(member_ids),len(user_ids)):
        raise InvalidMemberException
    return list(user_ids)

def add_members_to_group(group_id,admin_id,user_ids):
    
    group_members = []
    group_members.append(Membership(group_id = group_id,member_id = admin_id,is_admin = True))
    for user in user_ids:
        group_members.append(Membership(group_id = group_id,member_id = user))
    Membership.objects.bulk_create(group_members)
    
    
#task-2
def create_group(user_id, name, member_ids):
    is_valid_user(user_id)
    is_valid_group_name(name)
    member_ids = list(dict.fromkeys(member_ids))
    user_ids = is_valid_members(member_ids)
    group_obj = Group.objects.create(name = name)
    if user_id in user_ids:
        user_ids.remove(user_id)
    add_members_to_group(group_obj.id,user_id,user_ids)
    return group_obj.id
    
def is_valid_group(group_id):
    
    group_objs = Group.objects.filter(id = group_id).prefetch_related('members','membership_set')
    if len(group_objs):
        return group_objs[0]
    else:
        raise InvalidGroupException

def is_user_in_group(user_obj,group_obj,check=False):
    if user_obj not in group_obj.members.all():
        if check:
            raise MemberNotInGroupException
        raise UserNotInGroupException

def is_user_an_admin_in_group(user_obj,group_obj,check=False):

    for member in group_obj.membership_set.all():
        if operator.eq(member.member_id,user_obj.id):
            if not(member.is_admin):
                if check:
                    member.is_admin = True
                    member.save()
                else:
                    raise UserIsNotAdminException
            break

#task-3
def add_member_to_group(user_id, new_member_id, group_id):
    
    user_obj = is_valid_user(user_id)
    new_member_obj = is_valid_user(new_member_id,True)
    group_obj = is_valid_group(group_id)
    is_user_in_group(user_obj,group_obj)
    is_user_an_admin_in_group(user_obj,group_obj)
    if new_member_obj not in group_obj.members.all():
        group_obj.members.add(new_member_obj)

#task-4
def remove_member_from_group(user_id, member_id, group_id):
    user_obj = is_valid_user(user_id)
    member_obj = is_valid_user(member_id,True)
    group_obj = is_valid_group(group_id)
    is_user_in_group(user_obj,group_obj)
    is_user_in_group(member_obj,group_obj,True)
    is_user_an_admin_in_group(user_obj,group_obj)
    group_obj.members.remove(member_obj)
    
#task-5
def make_member_as_admin(user_id, member_id, group_id):
    user_obj = is_valid_user(user_id)
    member_obj = is_valid_user(member_id,True)
    group_obj = is_valid_group(group_id)
    is_user_in_group(user_obj,group_obj)
    is_user_in_group(member_obj,group_obj,True)
    is_user_an_admin_in_group(user_obj,group_obj)
    is_user_an_admin_in_group(member_obj,group_obj,check = True)

#task-6
def create_post(user_id, post_content, group_id=None):
    user_obj = is_valid_user(user_id)
    is_valid_post_content(post_content)
    if not(group_id):
        group_obj = is_valid_group(group_id)
        is_user_in_group(user_obj,group_obj)
    return Post.objects.create(content = post_content,
                posted_by_id = user_id,group_id =group_id).id
    
#task-7
def get_group_feed(user_id, group_id, offset, limit):
    
    user_obj = is_valid_user(user_id)
    group_obj = is_valid_group(group_id)
    is_user_in_group(user_obj,group_obj)
    if operator.lt(offset,0):
        raise InvalidOffSetValueException
    elif operator.le(limit,0):
        raise InvalidLimitSetValueException
    queryset = Comment.objects.select_related('commented_by').prefetch_related(
                    Prefetch('reaction_set',to_attr = 'comment_reactions'))
    post_objs =  Post.objects.filter(posted_by_id = user_id,group_id = group_id).select_related('posted_by').prefetch_related(
        Prefetch('reaction_set',to_attr = 'post_reactions'),
        Prefetch('comment_set',queryset = queryset,to_attr = 'comments'))[offset:offset+limit]
    posts_list = []
    for post in post_objs:
        posts_list.append(post_details(post))
    return posts_list
    
def post_details(post_obj,check = False):
    comments_list = []
    parents_comment_list = []
    all_reply_comments_list = []
    
    for comment in post_obj.comments:
        if comment.parent_comment_id:
            parents_comment_list.append(comment)
        else:
            all_reply_comments_list.append(comment)
            
    for comment in parents_comment_list:
        comments_list.append(get_parent_comment(comment,all_reply_comments_list))
     
    post_dict = {
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
    if check:
        if post_obj.group_id:
            post_dict["group"] = None
        else:
            post_dict["group"] = {
                "group_id": post_obj.group_id,
                "name": post_obj.group.name
            }
        pass
    return post_dict

def post_object_reactions(post_obj):
    post_reaction_list = []
    for reaction in post_obj.post_reactions:
        if reaction.reaction not in post_reaction_list:
            post_reaction_list.append(reaction.reaction)
    return post_reaction_list

def comment_object_reactions(comment_obj):
    comment_reaction_list = []
    for reaction in comment_obj.comment_reactions:
        if reaction.reaction not in comment_reaction_list:
            comment_reaction_list.append(reaction.reaction)
    return comment_reaction_list

def get_parent_comment(comment,comment_objs):
    reply_comments = []
    for comment_obj in comment_objs:
        if operator.eq(comment.id,comment_obj.parent_comment_id):
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

#-task-8
def get_posts_with_more_comments_than_reactions():
    
    return  list(Post.objects.annotate(
                comments = Count('comment'),reactions = Count('reaction')).filter(
                    comments__gt=F('reactions')).values_list('id',flat = True))
        
#task-9
def get_user_posts(user_id):
    is_valid_user(user_id)
    queryset = Comment.objects.select_related('commented_by').prefetch_related(
                    Prefetch('reaction_set',to_attr = 'comment_reactions'))
    post_objs =  Post.objects.filter(posted_by_id = user_id).select_related('posted_by','group').prefetch_related(
        Prefetch('reaction_set',to_attr = 'post_reactions'),
        Prefetch('comment_set',queryset = queryset,to_attr = 'comments'))
    posts_list = []
    for post in post_objs:
        posts_list.append(post_details(post,True))
    return posts_list
    
#task-10
def get_silent_group_members(group_id):
    
    try:
        Group.objects.get(id = group_id)
    except Group.DoesNotExist:
        raise InvalidGroupException
    
    return list(User.objects.filter(group__id=group_id).annotate(
                posts_count = Count(
                    'post',filter=Q(post__group_id=group_id)
                    )).filter(posts_count = 0).values_list('id',flat = True))

#task-11
def get_posts_with_more_comments_than_post_with_comments_replies_and_reactions():
    
    return  list(Post.objects.annotate(
                parent_comments = Count('comment',filter = Q(comment__parent_comment_id__isnull = True)),
                reply_comments = Count('comment',filter = Q(comment__parent_comment_id__isnull = False)),
                reactions = Count('reaction')).filter(
                    Q(parent_comments__gt=F('reactions')),
                    Q(parent_comments__gt=F('reply_comments'))).values_list('id',flat = True))


    
    
    
