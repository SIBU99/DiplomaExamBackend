from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


# Create your models here.
class Batch(models.Model):
    "Batch Details"
    name = models.CharField(verbose_name="Name",help_text="Name of Batch", max_length=50)
    branch = models.CharField(verbose_name="Branch", max_length=50)
    year = models.IntegerField(verbose_name="Year")
    semester = models.IntegerField(verbose_name="Semester")

    @property
    def batchList(self):
        return self.batchs.all()
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Batch"
        verbose_name_plural = "Batchs"


def phoneVerify(value):
    "this will verify the Phone Number"
    if len(str(value)) is not 10:
        raise ValidationError("Provide a 10 digit number")
    elif not value.isdigit():
        
        raise ValidationError("Provide the Number")
    else:
        return value
class Student(models.Model):
    "This will hold the information of the Student"
    regno = models.SlugField(
        verbose_name="Registartion Number",
        max_length=13,
        unique=True,
        primary_key=True,
    )
    auth = models.ForeignKey(
        User, 
        verbose_name="Student's Auth", 
        on_delete=models.CASCADE,
        related_name="studentAuth"
    )
    name = models.CharField(
        verbose_name="Name",
        help_text="Student's Name",
        max_length=120
    )
    # email = models.EmailField(
    #     verbose_name="Email",
    #     help_text="Studnet's Student", 
    #     max_length=254,
    #     unique=True
    # ) 
    # phone = models.CharField(
    #     verbose_name="Phone", 
    #     help_text="Student's phone number", 
    #     max_length=10,
    #     validators=[
    #         phoneVerify
    #         ],
    # unique=True,
    # )
    batch = models.ForeignKey(Batch, verbose_name= "Batch", on_delete=models.SET_NULL, null=True, related_name="batchs")
    active = models.BooleanField(verbose_name = "Active", default= False)
    
    def __str__(self):
        return f"{self.regno}"

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

class Result(models.Model):
    "This will hold the information of the results"
    code  = models.SlugField(verbose_name = "Paper Code", max_length = 20, unique=True, primary_key=True)
    students = models.ManyToManyField(
        Student ,verbose_name="Students",through="Studentexam",related_name="studExam",)
    active  = models.BooleanField(verbose_name="Active", help_text="Student will be alowed to enter the exam and also allow to submit the exam", default=False)
    
    @property
    def Count(self):
        return self.students.all().count()

    class Meta:
        verbose_name = "Result"
        verbose_name_plural = "Results"

class Studentexam(models.Model):
    "this will hold the information of student and exam"
    result  = models.ForeignKey(Result, verbose_name="Examination", on_delete=models.CASCADE,)
    student = models.ForeignKey(Student, verbose_name="Student", on_delete=models.SET_NULL, null= True)
    mark = models.IntegerField(verbose_name = "Mark", default = 0)

    class Meta:
        ordering = ("mark",)
