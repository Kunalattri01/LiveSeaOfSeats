from django.views.generic import TemplateView
from users.services.search_service import global_search


class SearchPageView(TemplateView):
    template_name = "events/events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query = self.request.GET.get('q')
        city = self.request.session.get('city')

        print('query : ', query)
        print('city : ', city)

        results = global_search(query, city)

        context.update({
            "query": query,
            "events": results["events"],
        })

        return context