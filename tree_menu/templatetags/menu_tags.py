from django import template
# from tree_menu.utils.utils import get_current_path, get_current_url
from utils.url import get_current_path, get_current_url
from tree_menu.models import Menu, MenuItem

register = template.Library()

@register.inclusion_tag('tree_menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    """
    Шаблонный тег для отрисовки древовидного меню.
    """
    current_path = get_current_path(context)
    current_url_name = get_current_url(context)
    active_item_id = None

    try:
        menu_items = MenuItem.objects.filter(
            menu__name=menu_name
        ).select_related('parent').order_by('order', 'name')

        items_by_id = {item.id: item for item in menu_items}

        for item in menu_items:
            item_url = item.get_absolute_url()

            if item_url == current_path:
                active_item_id = item.id
                break

            if item.named_url and current_url_name and item.named_url == current_url_name:
                active_item_id = item.id
                break

            if current_path.startswith(item_url) and item_url != '/':
                active_item_id = item.id
        menu_tree = build_menu_tree(menu_items, active_item_id, items_by_id)

    except Menu.DoesNotExist:
        menu_tree = []
    except Exception as e:
        print(f"Ошибка Отрисовки меню '{menu_name}': {e}")
        menu_tree = []

    return {
        'menu_items': menu_tree,
        'active_item_id': active_item_id,
        'current_path': current_path,
        'menu_name': menu_name,
    }

def build_menu_tree(menu_items, active_item_id, items_by_id):
    """
    Строит древовидную структуру меню и помечает развернутые ветки.
    """
    children_map = {item_id: [] for item_id in items_by_id.keys()}

    root_items = []

    active_path_ids = set()
    if active_item_id:
        current = items_by_id.get(active_item_id)
        while current:
            active_path_ids.add(current.id)
            current = current.parent

    for item in menu_items:
        item.is_active = (item.id == active_item_id)
        item.is_expanded = False
        item.children_list = []

        if item.parent_id is None:
            root_items.append(item)
        else:
            if item.parent_id in children_map:
                children_map[item.parent_id].append(item)

    def build_branch(items):
        for item in items:
            if item.id in active_path_ids:
                item.is_expanded = True

            if item.parent_id == active_item_id:
                item.is_expanded = True

            if item.id in children_map:
                item.children_list = sorted(children_map[item.id], key=lambda x: (x.order, x.name))
                build_branch(item.children_list)
        return items

    final_tree = sorted(root_items, key=lambda x: (x.order, x.name))
    build_branch(final_tree)
    
    return final_tree
