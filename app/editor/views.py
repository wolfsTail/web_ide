from django.http import HttpResponse
from django.shortcuts import render

from editor.utils import run_code


def get_editor(request):    
    return render(request, "editor/editor.html")


def execute_code_partial(request):
    if request.method == "POST":
        code_data = request.POST.get("codearea", None)
        language = request.POST.get("language")
        if code_data is None:
            return render(request, "editor/partial/editor_output.html", {"error": "Пожалуйста, укажите хоть что-то!"})
        else:
            output = run_code(code_data, language)
            return render(request, "editor/partial/editor_output.html", {"code": code_data, "output": output})
    else:
        return render(request, "editor/editor.html")
