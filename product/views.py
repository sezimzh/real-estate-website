from django.shortcuts import render

def index_view(request):
    return render(
        request=request,
        template_name='main/index.html'
    )
def estate_detail_view(request):
    return render(
        request=request,
        template_name='main/estate_detail.html'
    )