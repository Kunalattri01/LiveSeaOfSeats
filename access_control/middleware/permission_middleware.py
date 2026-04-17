from ..models import Menubar, RolePermission, UserRole
from django.http import Http404
from django.urls import reverse
from django.conf import settings
from users.models import User
from django.db.models import F

class PermissionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # excluded_urls = [reverse('LoginPage'), reverse('logout'), reverse('DashboardPage'),reverse('VendorEntryPage')]
        excluded_urls = []

        static_url = settings.STATIC_URL
        media_url = settings.MEDIA_URL

        # Check if the request path is not in the excluded URLs and doesn't start with static or media URLs
        if not (request.path.startswith(static_url) or request.path.startswith(media_url) or request.path in excluded_urls):
            request.base_rights = []
            request.current_menu = None

            visiting_url = request.path

            menu_name = Menubar.objects.filter(url = visiting_url, is_active = True).first()
            request.current_menu = menu_name.menu_code if menu_name else None   # storing the current menu code

            user = request.user if request.user.is_authenticated else None

            user_category = UserRole.objects.filter(user=user,is_active=True).values('role_code', role_name = F('user__role')).first() # getting the role for each logged person 
                                                                                                                    # ['ADMIN', 'ORGANIZER', 'USER']

            # print('user_category : ', user_category)
            # print('request.user.is_authenticated : ', request.user.is_authenticated)
            # print('menu_name : ', menu_name)

            # if (user_category and user_category != 'USER') and request.user.is_authenticated and menu_name:
            if (user_category) and request.user.is_authenticated and menu_name:

                    permissions = RolePermission.objects.filter(menu_code = menu_name.menu_code, role_code = user_category['role_code'], is_allowed = True)
                    base_rights = [row.perm_code.perm_name for row in permissions]

                    request.base_rights = base_rights
                    # print('base_rights : ', base_rights)

                    
                    if 'READ' not in request.base_rights:   # shows the page404 if user had not READ write of the visited url
                        raise Http404()

        response  = self.get_response(request)

        return response