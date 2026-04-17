from ..models import Menubar

# get active parent menus
def active_parent_menus():
    return Menubar.objects.filter(is_active = True, url__isnull = True).values('menu_name', 'menu_code').order_by('menu_name')


# get active sub menus with no child (screens to access)
def active_accessing_screens():
    return Menubar.objects.filter(is_active = True, url__isnull = False, parent__isnull = False).values('menu_name', 'menu_code').order_by('menu_name')