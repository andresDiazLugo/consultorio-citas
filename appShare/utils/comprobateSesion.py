from django.shortcuts import render, redirect

def comprobateSesion(autenticate=False):
    if not autenticate:
        print("me ejecutoooooooooooooooo")
        directionUrl ='login'
        return redirect(directionUrl)
