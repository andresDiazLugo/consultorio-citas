from django.shortcuts import render,redirect
from appShare.models import Servicios
from django.http import HttpResponse,JsonResponse   
from datetime import datetime
from appShare.models import Citas,CitasServicios,Users,Servicios
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
import json
# from appShare.utils.comprobateSesion import comprobateSesion
# Create your views here.

@login_required()
def citas(request):
    nombre = request.session.get('nombre')
    apellido = request.session.get('apellido')
    fecha_actualy = datetime.now()
    fecha_formateada = fecha_actualy.strftime('%Y-%m-%d')
    concat_NameLastName = f"{nombre} {apellido}"
    idUser = request.session.get('idUser')
    name_user = request.session.get('nombre')
    # print("ESTOS SON LOS NOMBRES",concat_NameLastName)
    # print("esta es la fecha",fecha_formateada)
    print("Este es el nombre del usuario", idUser )
    return render(request,'landing/citas.html',{
        "nombre": concat_NameLastName,
        "fecha":fecha_formateada,
        "idUser":idUser,
        'nameUser':name_user
    })

def apiServicios(request):
    data_servicios = Servicios.objects.all()
    print("estos son los servicios",data_servicios)
    data_serializable = list(data_servicios.values())
    json_data = json.dumps(data_serializable)
    response = HttpResponse(json_data, content_type='application/json')
    response.status_code = 200
    return response

def apiTurnos(request):
    
    if request.method == 'POST':
        print(request.POST)
        # json_data = json.dumps({"msg":"TODO OK"}); 
        # response = HttpResponse(json_data,content_type='application/json')
# {'usuarioId': ['33'], 'fecha': ['2023-06-20'], 'hora': ['18:11'], 'servcio':  ['1,2']}>
        userInstance = Users.objects.get(id=request.POST['usuarioId'])
        citasCreat = Citas(
            fecha = request.POST['fecha'],
            hora = request.POST['hora'],
            usuarioId = userInstance
        )
        citasCreat.save()

        for element in request.POST['servcio'].split(','):
         
            serviceInstance = Servicios.objects.get(id=element)
            citas_X_servicios = CitasServicios(
                citaId = citasCreat,
                serviciosId = serviceInstance
            )
            citas_X_servicios.save()

        response_data = {
        'resultado': True,
        'status': 'success',
        }

        return JsonResponse(response_data)

    else:
          return JsonResponse({'resultado': False}, status=405)
def signout(request):
    logout(request)
    return redirect('login')