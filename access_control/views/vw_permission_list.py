from django.views import View
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from ..service.access_service import active_accessing_screens

from ..models import PermissionList, Menubar
from access_control.permissions import permission_required


class PermissionEntryView(View):

    @method_decorator(permission_required("READ"))
    def get(self, request):

        # permissions = PermissionList.objects.all().order_by("-id")
        menus = active_accessing_screens()

        context = {
            # "permissions": permissions,
            "menus": menus
        }

        return render(request, "access_control/permission_list.html", context)



    @method_decorator(permission_required("WRITE"))
    def post(self, request):

        perm_code = request.POST.get("perm_code")

        menu_code = request.POST.get("menu_code")
        perm_type = request.POST.get("perm_type")
        perm_name = request.POST.get("perm_name")
        is_active = True if request.POST.get('is_active') == "1" else False

        data = {
            "perm_name": perm_name,
            "perm_type": perm_type,
            "menu_code": Menubar.objects.get(menu_code=menu_code) if menu_code else None,
            "is_active": is_active
        }

        if not perm_code:

            last_code = PermissionList.objects.values('id').last()
            id = int(last_code['id']) + 1 if last_code else 1
            perm_code = f"PERM{id:04d}"

        perm_obj = PermissionList.objects.filter(perm_code=perm_code)

        if perm_obj.exists():

            if "MODIFY" not in request.base_rights:
                return redirect("PermissionEntryPage")

            perm_obj.update(**data)

        else:

            PermissionList.objects.create(**data, perm_code=perm_code)

        return redirect("PermissionEntryPage")