

from django.template.context import RequestContext
from django.shortcuts import render_to_response

from django.http import HttpResponse

from django.db.models import Q,Count, Min, Max, Sum, datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from qurananalyst.models import *

from datetime import date

import json
from qurananalyst.forms import VerseCommentForm


def home(request):
    context = RequestContext(request)
    context.update({ 'msg_body' : "All Chapters", })
    
    chapters = Chapter.objects.all()
    
    context.update({ 'chapters' : chapters, })
    
    return render_to_response("home.html", context_instance=context)


def info(request):
    context = RequestContext(request)
    context.update({ 'msg_body' : "", })
    
    return render_to_response("info.html", context_instance=context)


def chapter(request, **Args):
    context = RequestContext(request)
    
    chapterNum = str(Args.get('chap')).strip('/')
    cNum = str(chapterNum)
    context.update({ 'cnum' : int(cNum), })
    
    chName = Chapter.objects.get(pk=cNum)
    context.update({ 'msg_body' : "All verses of the chapter " + cNum + ": " + chName.transliteration + " " + chName.arabic_name + " (" + chName.english_name + ")", })
    
    
    v = Q(chapter=cNum) & Q(author__name='Original Text')
    full_chap = Verse.objects.filter(v).order_by('number')
    context.update({ 'full_chap' : full_chap, })
    
    
    
    auths = Verse.objects.filter(chapter=cNum).values('author').distinct()
    authors = []
    for a in auths:
        authors.append(Author.objects.get(pk=a['author']))
    
    context.update({ 'authors' : authors, })
    
    
    return render_to_response("chapter.html", context_instance=context)



def verse(request, **Args):
    context = RequestContext(request)
    
    cSuccess = False
    
    chapterNum = str(Args.get('chap')).strip('/')
    verseNum = str(Args.get('verse')).strip('/')
    
    cNum = str(chapterNum)
    vNum = str(verseNum)
    
    cf_init = dict(user=request.user.pk, vnum=vNum, cnum=cNum)
    
    if(request.method=="POST"):
        post = request.POST.copy()
        comment_form = VerseCommentForm(request.POST, initial=cf_init)
        if(comment_form.is_valid()):
            try:
                newComment = comment_form.save()
                cSuccess = True
            except:
                print "comment save failed."
                raise
        else:
            print comment_form.errors
    else:
        comment_form = VerseCommentForm(initial=cf_init)
    
    
    context.update({ 'cnum' : int(cNum), 'vnum' : int(vNum) })
    
    context.update({ 'msg_body' : "Chapter " + cNum + " Verse " + vNum, })
    
    f1 = Q(chapter=cNum) & Q(number=vNum) & Q(author__name='Original Text')
    
    verse = Verse.objects.filter(f1)
    
    context.update({ 'verse' : verse, })
    
    auths = Verse.objects.filter(chapter=cNum).values('author').distinct()
    
    authors = []
    for a in auths:
        authors.append(Author.objects.get(pk=a['author']))
    
    context.update({ 'authors' : authors, })
    
    f2 = Q(cnum=cNum) & Q(vnum=vNum)
    
    comments = Comment.objects.filter(f2)
    
    context.update({ 'comments' : comments, 'comment_form': comment_form})
    
    if(cSuccess):
        context.update({ 'messages' : ['Your comment has been posted successfully'], 'cSuccess' : cSuccess, })
    
    
    cdetail = Chapter.objects.get(pk=chapterNum)
    if cdetail.total_verses:
        total_verse = cdetail.total_verses
        
        pnext = False
        if (int(verseNum) < int(total_verse)):
            pnext = True
            
        pprevious = False
        if int(verseNum) > 1:
            pprevious = True
        
        context.update({ 'pnext' : pnext, 'pprevious' : pprevious, })
    else:
        context.update({ 'pnext' : False, 'pprevious' : False, })
    
    return render_to_response("verse.html", context_instance=context)



def getchapter(request):
    
    try:
    	authorName = request.POST.get('authorName', False)
    	chapterNum = request.POST.get('chapterNum', False)
    except:
    	raise
    
    f1 = Q(chapter=chapterNum) & Q(author__name=authorName)
    
    verses = Verse.objects.filter(f1)
    
    results = []
    
    for v in verses:
    	results.append({ 'verseNum' : v.number, 'vtext' : v.vtext, 'author' : v.author.name, 'authorid' : v.author.id, 'lang' : v.author.alang.name })
    
    return HttpResponse(json.dumps(results), mimetype="application/json")


def getverse(request):
    try:
    	authorName = request.POST.get('authorName', False)
    	chapterNum = request.POST.get('chapterNum', False)
    	verseNum = request.POST.get('verseNum', False)
    except:
    	raise
    
    f1 = Q(chapter=chapterNum) & Q(number=verseNum) & Q(author__name=authorName)
    
    verses = Verse.objects.filter(f1)
    
    results = []
    
    for v in verses:
    	results.append({ 'verseNum' : v.number, 'vtext' : v.vtext, 'author' : v.author.name, 'authorid' : v.author.id, 'lang' : v.author.alang.name })
    
    return HttpResponse(json.dumps(results), mimetype="application/json")



def search(request, **Args):
    context = RequestContext(request)
    
    try:
        search = request.POST.get('search', Args.get('search'))
    except:
        search = False

    try:
        page = str(Args.get('page', 1)).strip('/')
    except:
        page = 1
    
    pageNum = int(page);
    pageSize = 20;
    
    if(search != False):
        titlesearch = Q(english_name__icontains=search) | Q(arabic_name__icontains=search) | Q(transliteration__icontains=search)
        versesearch = Q(vtext__icontains=search)
        commentsearch = Q(ctext_icontains=search)
    
    
    try:
        titleresult = Paginator(Chapter.objects.filter(titlesearch), pageSize).page(pageNum)
    except:
        titleresult = []
    
    try:
        verseresult = Paginator(Verse.objects.filter(versesearch), pageSize).page(pageNum)
    except:
        verseresult = []
    
    try:
        commentresult = Paginator(Comment.objects.filter(commentsearch), pageSize).page(pageNum)
    except:
        commentresult = []
    
    context.update({
        'titleresult' : titleresult,
        'verseresult' : verseresult,
        'commentresult' : commentresult,
        'searchkey' : search,
        'pageNum' : pageNum,
        'pageSize': pageSize,
        'totalresult' : sum(getattr(x, 'paginator', Paginator([], 0)).count for x in [titleresult, verseresult, commentresult])
    })
    
    return render_to_response("search.html", context_instance=context)


def discussions(request):
    context = RequestContext(request)
    context.update({ 'msg_body' : "", })
    
    comments = Comment.objects.all().order_by('-date_published')
    
    #context.update({ 'comments' : comments, })
    
    comment_data = []
    for c in comments:
    	ff = Q(vnum=c.vnum) & Q(cnum=c.cnum)
    	numcomment = Comment.objects.filter(ff).count()
    	comment_data.append({'comment' : c, 'count' : numcomment })
    	
    context.update({ 'comments' : comment_data, })
    
    return render_to_response("discussions.html", context_instance=context)








