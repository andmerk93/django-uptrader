from json import loads

from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.http import Http404, JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict

from .models import Menu


def index(request, slug):
    if slug == '':
        raise Http404("No Menu URL was given.")
    tree = slug.strip('/').split('/')
    all_menues = Menu.objects.all().select_related('parent')
    slugged_menues = [
        get_object_or_404(all_menues, slug=i)
        for i in tree
    ]
    for num, obj in enumerate(slugged_menues):
        if num == 0:
            continue
        if slugged_menues[num-1] != obj.parent:
            raise Http404("No Menu matches the given query.")
    all_nested = [*map(model_to_dict, all_menues)]
    for parent in all_nested:
        parent['children'] = []
        for child in all_nested:
            if child['parent'] == parent['id']:
                parent['children'] += [child]
    for obj in [*all_nested]:
        if obj['parent']:
            all_nested.remove(obj)
#    return JsonResponse(all_nested, safe=False)
#    get_list_or_404(Menu, slug=tree[0])
#    lst = [*Menu.objects.values(), tree]
#    ser = serializers.serialize('json', slugged_menues)
#    lst = [loads(ser), tree]
#    lst = [model_to_dict(obj) for obj in slugged_menues] + [tree]
    slugged_nested = [*map(model_to_dict, slugged_menues)]
    for num, obj in enumerate(slugged_nested):
        if num == 0:
            obj['url'] = obj['slug']
            continue
        obj['url'] = slugged_nested[num-1]['url'] + '/' + obj['slug']
    context = dict(
        tree=slugged_nested,
    )
#    1/0
    return render(request, 'index.html', dict(context=context))
#    return JsonResponse((*lst, tree), safe=False)
