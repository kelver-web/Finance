from datetime import datetime, timedelta
from io import BytesIO
from dateutil.parser import parse
from django.shortcuts import redirect, render
from django.http import FileResponse
from django.contrib import messages
from django.contrib.messages import constants
from django.template.loader import render_to_string
from django.conf import settings

import os
from weasyprint import HTML

from extrato.models import Valores
from perfil.models import Categoria, Conta

# Create your views here.


def novo_valor(request):
    if request.method == "GET":
        contas = Conta.objects.all()
        categorias = Categoria.objects.all()
        return render(
            request, "novo_valor.html", {"contas": contas, "categorias": categorias}
        )

    elif request.method == "POST":
        valor = request.POST.get("valor")
        categoria = request.POST.get("categoria")
        descricao = request.POST.get("descricao")
        data = request.POST.get("data")
        conta = request.POST.get("conta")
        tipo = request.POST.get("tipo")

        valores = Valores(
            valor=valor,
            categoria_id=categoria,
            descricao=descricao,
            data=data,
            conta_id=conta,
            tipo=tipo,
        )

        valores.save()

        conta = Conta.objects.get(id=conta)

        if tipo == "E":
            conta.valor += int(valor)
            messages.add_message(
                request, constants.SUCCESS, "Entrada cadastrada com sucesso"
            )

        else:
            conta.valor -= int(valor)
            messages.add_message(
                request, constants.SUCCESS, "Saída cadastrada com sucesso"
            )

        conta.save()

        return redirect("/extrato/novo_valor")


def view_extrato(request):
    valores = Valores.objects.filter(data__month=datetime.now().month)
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()

    conta_get = request.GET.get("conta")
    categorias_get = request.GET.get("categoria")

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if conta_get:
        valores = valores.filter(conta_id=conta_get)

    if categorias_get:
        valores = valores.filter(categoria_id=categorias_get)

    if start_date and end_date:
        # Convert to date and transform into day
        end_date = parse(end_date) + timedelta(days=1)
        valores = valores.filter(data__range=[start_date, end_date])

    return render(request, "view_extrato.html", {"valores": valores, "contas": contas, "categorias": categorias})


def zerar_filtro(request):
    return redirect("/extrato/view_extrato")


def exportar_pdf(request):
    valores = Valores.objects.filter(data__month=datetime.now().month)
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    
    path_template = os.path.join(settings.BASE_DIR, 'templates/partials/extrato.html')
    path_output = BytesIO()

    template_render = render_to_string(path_template, {'valores': valores, 'contas': contas, 'categorias': categorias})
    HTML(string=template_render).write_pdf(path_output)

    path_output.seek(0)
    

    return FileResponse(path_output, filename="extrato.pdf")

