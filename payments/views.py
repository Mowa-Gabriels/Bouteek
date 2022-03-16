from django.conf import settings
from django.views.generic.base import TemplateView

class HomePageView(TemplateView):
    template_name = 'store/homepage.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.RAVE_PUBLIC_KEY
        return context