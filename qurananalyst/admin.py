'''
Created on Aug 3, 2012

@author: hossain
'''
from qurananalyst.models import *
from django.contrib import admin

class LanguageAdmin(admin.ModelAdmin):
    pass

class AuthorAdmin(admin.ModelAdmin):
    pass

class ChapterAdmin(admin.ModelAdmin):
    pass

class VerseAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Language, LanguageAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Verse, VerseAdmin)
admin.site.register(Comment, CommentAdmin)

