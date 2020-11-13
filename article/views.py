from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from django.http import HttpResponse

from comment.models import Comment
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from .models import ArticlePost
import markdown
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import  ArticleColumn
# 引入评论表单
from comment.forms import CommentForm


# Create your views here.
def article_list(request):
    search=request.GET.get('search')
    order=request.GET.get('search')
    if search:
        if order=='total_views':
            articles=ArticlePost.objects.filter(
                Q(title_contains=search) |
                Q(title__contains=search)
            ).order_by('-total_views')
        else:
            articles = ArticlePost.objects.filter(
                Q(title__contains=search) |
                Q(title__contains=search)
            )
    else:
        # 将 search 参数重置为空
        search = ''
        if order == 'total_views':
            articles = ArticlePost.objects.all().order_by('-total_views')
        else:
            articles = ArticlePost.objects.all()

    # if request.GET.get('order')=='total_views':
    #     articles=ArticlePost.objects.all().order_by('-total_views')
    #     order = 'total_views'
    # else:
    #     articles = ArticlePost.objects.all()
    #     order = 'normal'

    paginator=Paginator(articles,6)
    page=request.GET.get('page')
    articles=paginator.get_page(page)

    context = {'articles': articles, 'order': order, 'search': search}
    return render(request,'article/list.html',context)


def article_detail(request,id):
    article=ArticlePost.objects.get(id=id)

    # 取出文章评论
    comments = Comment.objects.filter(article=id)
    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    md=markdown.Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                # 目录扩展
                'markdown.extensions.toc',
            ])
    article.body=md.convert(article.body)
    # 引入评论表单
    comment_form = CommentForm()
    # 新增了md.toc对象
    context = { 'article': article, 'toc': md.toc, 'comments': comments,'comment_form':comment_form}
    return render(request, 'article/detail.html',context)


@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method=="POST":
        # article_post_form=ArticlePostForm(data=request.POST)
        article_post_form=ArticlePostForm(request.POST,request.FILES)
        if article_post_form.is_valid():
            new_article=article_post_form.save(commit=False)
            # new_article.author=User.objects.get(id=1)
            new_article.author = User.objects.get(id=request.user.id)

            # 新增的代码
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])

            new_article.save()

            # 新增代码，保存 tags 的多对多关系
            article_post_form.save_m2m()
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form=ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context={"article_post_form":article_post_form,"columns":columns}
        return render(request,'article/create.html',context)


def article_delete(request,id):
    article=ArticlePost.objects.get(id=id)
    article.delete()
    return redirect("article:article_list")

def article_update(request,id):
    article=ArticlePost.objects.get(id=id)
    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")

    if request.method=="POST":
        # article_post_form=ArticlePostForm(data=request.POST)
        article_post_form=ArticlePostForm(request.POST,request.FILES)
        if article_post_form.is_valid():
            article.title=request.POST['title']
            article.body=request.POST['body']

            # 分类
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            # 标题图
            if request.FILES.get('avatar'):
                print(request.FILES.get('avatar'))
                article.avatar = request.FILES.get('avatar')
            else:
                print(0)
            # 标签
            article.tags.set(*request.POST.get('tags').split(','), clear=True)

            article.save()
            return redirect("article:article_detail",id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form=ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context={'article':article,'article_post_form':article_post_form,'columns':columns}
        return render(request,'article/update.html',context)
