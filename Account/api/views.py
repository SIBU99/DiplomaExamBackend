from rest_framework.exceptions import ValidationError
from ..models import (
    Batch,
    Student,
    Result,
    Studentexam
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

class AuthenticateStudent(APIView):
    "this will authenticate the User"
    def post(self, request, format=None):
        "this will accept the post request"
        username = request.data.get("username" ,None)
        password = request.data.get("password", None)
        code = request.data.get("code", None)
        if not code:
            msg = {
                "Error":"Please Provide Paper Code"
            }
            raise ValidationError(msg)
        if not username:
            msg = {
                "Error":"Please Provide Username"
            }
            raise ValidationError(msg)
        elif not password:
            msg = {
                "Error":"Please Provide Password"
            }
            raise ValidationError(msg)
        
        try:
            result = Result.objects.get(code = code)
        except:
            msg = {
                "Error":"Provide the valid Paper"
            }
            raise ValidationError(msg)
        
        user = authenticate(username= username, password = password)
        print(user)
        if not user:
            msg = {
                "Error":"Please Provide correct Credentials"
            }
            return Response(msg, status.HTTP_401_UNAUTHORIZED)
        
        try:
            student = user.studentAuth.all()[0]
        except:
            msg = {
                "Staus":False
            }
            return Response(msg, status.HTTP_401_UNAUTHORIZED)
        if student.active:
            msg = {
                "Staus":False
            }
            return Response(msg, status.HTTP_423_LOCKED)
        else:
            if result.active:
                student.active = True
                student.save()
                msg = {
                        "Staus":True
                    }
                return Response(msg, status.HTTP_202_ACCEPTED)
            else:
                msg = {
                        "Staus":False
                    }
            return Response(msg, status.HTTP_403_FORBIDDEN)

class ResultStore(APIView):
    "this will store the result"
    def post(self, requests, format=None):
        "this will be in action ever there will a post request"
        code = requests.data.get("code", None)
        studentid = requests.data.get("id", None)
        mark = requests.data.get("mark", None)
        mark = int(mark)
        
        if not code:
            msg = {
                "Error":"Please Provide Paper Code"
            }
            raise ValidationError(msg)
        elif not studentid:
            msg = {
                "Error":"Please Provide Registration Number"
            }
            raise ValidationError(msg)
        elif not mark:
            msg = {
                "Error":"Please Provide Mark"
            }
            raise ValidationError(msg)
        
        try:
            student = Student.objects.get(regno = studentid)
        except:
            msg = {
                "Error":"Provide the valid Registartion Number"
            }
            raise ValidationError(msg)
        try:
            result = Result.objects.get(code = code)
        except:
            msg = {
                "Error":"Provide the valid Paper"
            }
            raise ValidationError(msg)
        if not result.active:
            msg = {
                        "Staus":False
                    }
            return Response(msg, status.HTTP_401_UNAUTHORIZED)
        
        regnos = Studentexam.objects.all().filter(result = result).values_list("student__regno", flat = True)

        if studentid in regnos:
            msg = {
                        "Staus":False
                    }
            return Response(msg, status.HTTP_401_UNAUTHORIZED)
        
        _ = Studentexam.objects.create(result = result, student = student, mark = mark)
        
        msg = {
            "status":True
        }
        return Response(msg, status.HTTP_202_ACCEPTED)
