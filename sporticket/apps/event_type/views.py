from django.shortcuts import render
from apps.event_type.forms import EventTypeForm

# Create your views here.
def insertEventType(request):
    if request.method == 'POST':
        form = EventTypeForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('insertEvents.html')
    else:
        form = EventTypeForm()
    return render(request, 'events/insertEvenType.html',{'form':form})