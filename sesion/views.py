from django.shortcuts import render, redirect
from django.http import HttpResponse
from appShare.models import Users,MyCustomException
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.tokens import default_token_generator
from appShare.clases.Email import Email
import copy
import shortuuid
from django.contrib.auth.decorators import login_required

# from django.core.exceptions import ValidationError

# Create your views here.
#sesion user
def signIn(request):
      if request.method == 'POST':
          
          try:
                    user = Users.objects.filter(email= request.POST["email"]).first()
                    userCamps = Users(
                         email = request.POST["email"],
                         password = request.POST["password"] ,
                    )    
                    userCamps.ValidatorCampLogin()
                    if user :
                         checkPasswordHash = check_password(request.POST["password"],user.password)
                         checkConfirmation = user.confirmado
                         print("ver el password",checkPasswordHash)
                         checkPasswordHash if checkPasswordHash else  userCamps.ValidatorCampLogin(["El password no coincide"])
                         checkConfirmation if checkConfirmation else  userCamps.ValidatorCampLogin(["Esta cuenta no esta confirmada tienes que confirmarla"])
                         # userSesion = authenticate(email = request.POST["email"], password = user.password)
                         print("este es el usuario", user.id)
                         request.session['idUser'] = user.id
                         request.session['nombre'] = user.nombre
                         request.session['apellido'] = user.apellido
                         request.session['email'] = user.email

                         print("este es el usuario", user)
                         login(request,user)
                         if user.admin:
                              return redirect('admininstrador')
                         else:     
                              return redirect('citas')
                    else:
                         return render(request, 'auth/loging.html',{
                              'errors': ['El email que has ingresado no esta vinculado a nuestro servicio, cree una cuenta']  
                         })  
          except MyCustomException  as error:
                    print("estos son los errores", error.errors)
                    return render(request, 'auth/loging.html',{
                         "errors":error.errors
                    })                  
      else:
          return render(request, 'auth/loging.html')
    
def logout(request):
     response = HttpResponse('<h1> Este es el logout </h1>')
     return response

#I forgot my password
def forgotPassword(request):
     if request.method == 'POST':
          email = request.POST['email']
          error = ''
          token = shortuuid.uuid()
          if len(email) == 0:
               error="El Email es obligatorio"
          user = Users.objects.filter(email= email).first()
          if user:
               user.token = token
               user.save()
               email_address = Email(user.email,user.nombre,user.token)
               email_address.sendResetPassword()
               return render(request, 'auth/forgotPassword.html',{
                    'msg':'revisa tu correo y sigue las instrucciones'
               })
          else:
               return render(request, 'auth/forgotPassword.html',{
                    'error':error
               })
     else:
          return render(request, 'auth/forgotPassword.html')

def resetPassword(request):
     if request.method == 'POST':
          print(request.GET['token'])
          password = request.POST['password']
          newPassword = make_password(password)
          errors= []
          queryTokenUrl = request.GET['token']
          if len(password) == 0:
               errors.append('El password es obligatorio')
               return render(request,'auth/resetPassword.html',
                         {
                    'token': queryTokenUrl,
                    'errors': errors
               })
          if len(password) < 6:
               errors.append('El password tiene que tener un tamaños mayor a 6 caracteres')
               return render(request,'auth/resetPassword.html',
                         {
                    'token': queryTokenUrl,
                    'errors': errors
               })
          user = Users.objects.filter(token=queryTokenUrl).first()
          if user:
               user.password = newPassword
               user.token = ''
               user.save()
               return redirect('login')
          else:     
               return render(request,'auth/resetPassword.html',
                         {
                    'token': queryTokenUrl,
                    'errors': errors
               })

     else:     
          token= request.GET['token']
          return render(request,'auth/resetPassword.html',{
               'token': token if token else "NO_EXISTE_"
          })

#create acount
def createAccount(request):
     print(request.POST)
     if request.method == 'GET':
           return render(request, 'auth/createCount.html')
     else:
          try:
               usercreate = Users.objects.filter(email=request.POST["email"]).first()
               print(usercreate)
               if usercreate :
                    return render(request, 'auth/createCount.html',
                         {
                          "errors":["El usuario registrado con este correo ya existe intente iniciar sesion"]
                          })
               else:
                    token = shortuuid.uuid()
                    password_nothashed = request.POST["password"]
                    password = make_password(request.POST["password"]) if request.POST["password"] else ""
                    print("este es el password")
                    usercreate = Users(
                         nombre = request.POST["nombre"],
                         apellido = request.POST["apellido"],
                         email = request.POST["email"],
                         password = password ,
                         telefono = request.POST["telefono"],
                         token = token
                    )
                    usercreate.validatorCamp()
                    email = Email(usercreate.email,usercreate.nombre,usercreate.token)
                    print("esta es la instancia de Email",email)
                    email.sendConfirm()
                    usercreate.save()
                    login( request, usercreate)
                    # print("esta es la funcion login",request.user.is_authenticated)
                    # return render(request, 'auth/createCount.html',
                    #           {
                    #                "msg":"El usuario fue creado con exito confirme su cuenta entrando a su correo"
                    #           })
                    return redirect('mensaje')
          except MyCustomException  as error:
               print("estos son los errores", error.errors)
               return render(request, 'auth/createCount.html',{
                    "errors":error.errors
               })
          
def mensajes(request):
     return render(request,'auth/message.html')

def confirAccount(request):
     token = request.GET['token']
     print("ver el resultado del token", token)
     user = Users.objects.filter(token = token).first()
     if user:
          #aca actualizamos el campo confimar a true y ponemos el token en null y mostramos un mensaje de exito al usuario
          user.token = ''
          user.confirmado = True
          user.save()
          return render(request,'auth/confirmAccount.html',{
          "msg":"Tu cuenta fue validada con exito, inicia sesión"
     })   
     else:
          #mostramos un mensaje de error al usuario
          return render(request,'auth/confirmAccount.html',{
          "error":"Token invalido"
     })      

#Page not found
def PageNotFound(request):
     return render(request,'notFound.html')