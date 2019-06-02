from django.shortcuts import render
# Form de Contato
from .forms import Contato


def contato(request):
    title = 'Envie-nos seu feedback ou sugestão'
    confirm_message = None
    context = {}
    template_name = 'contact.html'

    if request.method == 'POST':
        # Se for POST eu to validando e enviando alguma coisa pros dados
        form = Contato(request.POST or None)
        if form.is_valid():
            context['is_valid'] = True
            form.send_mail()
            # quando o formulário for válido e o submit
            # for acionado esse comando limpará os dados
            form = Contato()

            title = "Nós agradecemos!"
            confirm_message = "Obrigado pela mensagem!!!"
            form = None
    else:
        form = Contato()  # se não OK
    context['form'] = form
    context['title'] = title
    context['confirm_message'] = confirm_message
    return render(request, template_name, context)
