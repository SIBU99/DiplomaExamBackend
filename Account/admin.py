from django.contrib import admin
from .models import (
    Batch,
    Student,
    Result,
    Studentexam
)
from django.contrib.admin import ModelAdmin
from django.shortcuts import render
# from django.http import HttpResponseRedirect
from django.http import HttpResponse
import csv
# from django.core.exceptions import ValidationError
from django.contrib import messages as msg
# Register your models here.
class StudentInlineView(admin.StackedInline):
    "this will allow the user to add the comment"
    model = Student
    fieldsets = (
        (None, {'fields':(("regno","auth"),("name",),)}), #("email", "phone"))}),
    )
    extra = 0

class BatchAdmin(ModelAdmin):
    "this will customize the model admin view"
    search_fields = ("name", "branch", "year", "semester",)
    list_display = ("id", "name", "branch", "year", "semester",)
    list_filter = ("branch", "year", "semester",)
    actions = ["resetAllStudent",]
    readonly_fields = ("id",)
    fieldsets = (
        (None, {'fields': ("id","name",)}),
        ('Details', {'fields': (("branch", "semester","year",) )}),
    )
    inlines = [
        StudentInlineView
    ]

    

    def resetAllStudent(self, request, queryset):
        "this will allow all the student to give exam"
        for batch in queryset:
            for student in batch.batchList:
                student.active = False
                student.save()
    resetAllStudent.short_description = "Reset for Exam"

admin.site.register(Batch, BatchAdmin)

class StudentAdmin(ModelAdmin):
    "this will customize the model admin view"
    search_fields = ("regno", "name",)
    list_display = ("regno", "name", "active",)
    list_filter = ("active","batch__branch", "batch__year", "batch__semester",)
    actions = ["resetForExam", "passwordReset",]
    fieldsets = (
        ("Main", {'fields': (("regno", "auth",),)}),
        ('Details', {'fields': (("name",),)}),#("email", "phone",), )}),
        ("Batch", {"fields":(("batch",), ("active",))}),
    )

    def resetForExam(self, request, queryset):
        "this will reset the exam for exam"
        queryset.update(active=False)
    resetForExam.short_description = "Reset for Exam"

    def passwordReset(self, request, queryset):
        "this will reset the password of the students"
        for student in queryset:
            regno = student.regno
            user = student.auth
            user.set_password(regno)
            user.save()
    passwordReset.short_description = "Reset Password"
admin.site.register(Student, StudentAdmin)

class StudentexamInlineView(admin.StackedInline):
    "this will allow the user to add the comment"
    model = Studentexam
    # readonly_fields = ("student", "mark",)
    readonly_fields = ("student",)
    fieldsets = (
        (None, {'fields':(("student", "mark",),)}),
    )
    extra = 0

class ResultAdmin(ModelAdmin):
    "this will customize the model admin view"
    search_fields = ("code",)
    list_display = ("code","Count","active", )
    list_filter = ("active",)
    actions = ["ExportToCSV",]
    fieldsets = (
        (None, {'fields': (("code", "active",),)}),
    )
    inlines = [
        StudentexamInlineView
    ]

    def ExportToCSV(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="results.csv"'
        writer = csv.writer(response)
        writer.writerow(["Sl. No.",'Registration Number', "Student Name", 'Mark',  ])
        for query in queryset:
            datas = Studentexam.objects.all().filter(result=query).values_list("student__regno","student__name" , "mark")
            datas = [(no ,data[0], data[1], data[2] ) for no, data in enumerate(datas,1)]
            print(datas)
            for data in datas:
                writer.writerow(data)
        return response
    ExportToCSV.short_description = "Export To CSV"

admin.site.register(Result, ResultAdmin)

admin.site.site_header = 'DIPLOMA EXAMINATION'                    # default: "Django Administration"
admin.site.index_title = 'EXAMINATION DASHBOARD'                 # default: "Site administration"
