from django.views.generic import FormView
from django.urls import reverse

from main.forms import IPForm


class HomeView(FormView):
    template_name = 'main.html'
    form_class = IPForm

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        ip = self.request.get_full_path()[1:-1]
        context['ip'] = ip
        return context

    def form_valid(self, form):
        return super(HomeView, self).form_valid(form)

    def get_success_url(self):
        return reverse('home', args=[self.request.POST['address'],])

