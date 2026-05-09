from django.db.models import Q
from access_control.models import UserRole, RolePermission, Menubar


def allowed_menus(request):

    parent_menus = []

    if request.user.is_authenticated:

        user_role = UserRole.objects.filter(
            user=request.user,
            is_active=True
        ).select_related("role_code").first()

        if user_role:

            permissions = RolePermission.objects.filter(
                role_code=user_role.role_code,
                is_allowed=True,
                perm_code__perm_name='READ'
            ).select_related("menu_code")

            # Allowed menu codes
            menu_codes = [p.menu_code.menu_code for p in permissions]

            # Allowed child menus
            allowed_child_menus = Menubar.objects.filter(
                menu_code__in=menu_codes,
                is_active=True
            )

            # Parent ids
            parent_ids = allowed_child_menus.exclude(
                parent=None
            ).values_list(
                'parent_id',
                flat=True
            )

            # Parent menus
            parent_menus = Menubar.objects.filter(
                Q(id__in=parent_ids) |
                Q(menu_code__in=menu_codes, parent=None),
                is_active=True
            ).prefetch_related(
                'children'
            ).order_by("position")

    return {
        "allowed_menus": parent_menus,
        "menu_codes": menu_codes if request.user.is_authenticated else []
    }