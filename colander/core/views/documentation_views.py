from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def write_documentation_view(request):
    #active_case = get_active_case(request)
    active_case = request.contextual_case
    if not active_case:
        messages.add_message(request, messages.WARNING,
                             "In order to write case documentation, you must first select a case to work on")
        return redirect('case_create_view')

    return render(request,
                  'pages/document/base.html')
