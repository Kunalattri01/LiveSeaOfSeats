from ..models import UserRole, RolePermission, Menubar

def allowed_menus(request):

    menus = []

    if request.user.is_authenticated:

        user_role = UserRole.objects.filter(user=request.user,is_active=True).select_related("role_code").first()

        if user_role:

            permissions = RolePermission.objects.filter(role_code = user_role.role_code, is_allowed=True, perm_code__perm_name = 'READ').select_related("menu_code")
            # print('permissions : ', permissions)

            menu_codes = [p.menu_code.menu_code for p in permissions]
            # print('menu_codes : ', menu_codes)

            menus = Menubar.objects.filter(menu_code__in=menu_codes,is_active=True).order_by("position")
            
    return {
        "allowed_menus": menus
    }