from django import template
from ..models import MenuItem

register = template.Library()


def expand_all_above_active_from_root(
    expanded_ids, root, active_root=None, active=None
):
    if active_root and active is None or active and active_root is None:
        raise ValueError(
            "Параметры active и active_root должны быть оба переданы, либо не переданы"
        )

    expanded_ids.add(root.id)

    for child in root.children_list:
        if active and root.id == active_root.id and active.order <= child.order:
            continue
        expand_all_above_active_from_root(
            expanded_ids, child, active_root, active
        )


@register.inclusion_tag("menu/menu.html", takes_context=True)
def draw_menu(context, menu_name):
    request = context["request"]
    current_url = request.path

    menu_items = list(
        MenuItem.objects.filter(menu_name=menu_name)
        .select_related("parent")
        .order_by("order")
    )

    items_dict = {item.id: item for item in menu_items}
    root_items = []

    for item in menu_items:
        item.is_expanded = False
        item.children_list = []

    for item in menu_items:
        if item.parent_id in items_dict:
            items_dict[item.parent_id].children_list.append(item)
        else:
            root_items.append(item)

    # Находим активный пункт
    active_item = None
    for item in menu_items:
        if item.get_url() == current_url:
            active_item = item
            break

    expanded_ids = set()

    if active_item:
        # Разворачиваем все, что всерху
        current = active_item
        while current:
            expanded_ids.add(current.id)
            last = current
            current = items_dict.get(current.parent_id)

        if items_dict.get(active_item.parent_id) is not None:
            expand_all_above_active_from_root(
                expanded_ids,
                last,
                items_dict[active_item.parent_id],
                active_item,
            )

        # Разворачиваем первый уровень под активным
        for child in active_item.children_list:
            expanded_ids.add(child.id)

    for item in menu_items:
        item.is_expanded = item.id in expanded_ids
        item.is_active = item == active_item

    return {
        "root_items": root_items,
        "menu_name": menu_name,
        "active_item": active_item,  # Для тестов (не используется в шаблоне)
        "expanded_ids": expanded_ids,  # Для тестов (не используется в шаблоне)
    }
