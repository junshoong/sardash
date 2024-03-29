from django.views.generic import FormView
from django.urls import reverse

from main.forms import IPForm
from main.models import Server


class HomeView(FormView):
    template_name = 'main.html'
    form_class = IPForm

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['server'] = Server.objects.all()
        context['ip'] = self.request.get_full_path()[1:-1]
        if context['ip'] is '':
            context['ip'] = '127.0.0.1'
        return context

    def form_valid(self, form):
        ip = self.request.POST['ip']
        form.get_remote_sar_data(ip)
        return super(HomeView, self).form_valid(form)

    def get_success_url(self):
        return reverse('home', args=[self.request.POST['ip'],])

