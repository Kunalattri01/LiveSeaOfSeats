from django.views import View
from django.shortcuts import render, redirect
from ..service.access_service import active_parent_menus
from ..models import Menubar

from django.utils.decorators import method_decorator
from access_control.permissions import permission_required


class MenubarEntryView(View):
    
    @method_decorator(permission_required("READ"))
    def get(self, request):

        result = Menubar.objects.all().order_by('position')
        dropdown_parent = active_parent_menus() # active parent menus
        

        context = {
            'result' : result,
            'dropdown_parent' : dropdown_parent,
        }

        return render(request, 'access_control/menubar_entry.html', context)
    

    @method_decorator(permission_required("READ"))
    def post(self, request):

        menu_code = request.POST.get('menu_code')
        menu_name = request.POST.get('menu_name')
        position = request.POST.get('position') or None
        url = request.POST.get('url')
        icon = request.POST.get('icon')
        parent = request.POST.get('parent')
        is_active = True if request.POST.get('is_active') == "1" else False

        # print('menu_code : ', menu_code)
        # print('menu_name : ', menu_name)
        # print('position : ', position)
        # print('url : ', url)
        # print('icon : ', icon)
        # print('parent : ', parent)
        # print('is_active : ', is_active)

        data = {
            'position' : position,
            'menu_name' : menu_name,
            # 'parent' : parent,
            'parent' : Menubar.objects.get(menu_code=parent) if parent else None,
            'url' : url,
            'icon' : icon,
            'is_active' : is_active
        }

        if not menu_code:

            last_code = Menubar.objects.values('id').last()
            id = int(last_code['id']) + 1 if last_code else 1
            menu_code = f"MU{id:04d}"

        if menu_code and menu_name:
            is_data = Menubar.objects.filter(menu_code = menu_code)

            if is_data.exists():

                if 'MODIFY' not in request.base_rights:
                    return redirect('MenubarEntryPage')
                
                is_data.update(**data)

            else:
                Menubar.objects.create(**data, menu_code = menu_code)

        return redirect('MenubarEntryPage')