from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from .models import ArticlePost
import markdown
from django.contrib.auth.decorators import login_required


# Create your views here.
def article_list(request):
    articles=ArticlePost.objects.all()

    return render(request,'article/list.html',{'articles':articles})


def article_detail(request,id):
    article=ArticlePost.objects.get(id=id)
    article.body=markdown.markdown(article.body,
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
    return render(request, 'article/detail.html', {'article': article})


@login_required(login_url='/userprofile/login/')
def article_create(request):
    if request.method=="POST":
        article_post_form=ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article=article_post_form.save(commit=False)
            # new_article.author=User.objects.get(id=1)
            new_article.author = User.objects.get(id=request.user.id)
            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form=ArticlePostForm()
        context={"article_post_form":article_post_form}
        return render(request,'article/create.html',context)


def article_delete(request,id):
    article=ArticlePost.objects.get(id=id)
    article.delete()
    return redirect("article:article_list")

def article_update(request,id):
    article=ArticlePost.objects.get(id=id)
    if request.method=="POST":
        article_post_form=ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title=request.POST['title']
            article.body=request.POST['body']
            article.save()
            return redirect("article:article_detail",id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form=ArticlePostForm()
        context={'article':article,'article_post_form':article_post_form}
        return render(request,'article/update.html',context)
