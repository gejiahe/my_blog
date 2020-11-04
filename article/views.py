from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from .models import ArticlePost
import markdown

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


def article_create(request):
    if request.method=="POST":
        article_post_form=ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article=article_post_form.save(commit=False)
            new_article.author=User.objects.get(id=1)
            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form=ArticlePostForm()
        context={"article_post_form":article_post_form}
        return render(request,'article/create.html',context)
