from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ToolForm, DependencyTagForm, BusinessTagForm, SearchForm, FeedbackForm
from .models import Tool, Update, User, DependencyTag, BusinessTag
from django.http import JsonResponse

from django.apps import apps
ldap = apps.get_app_config('app').ldap


# search page
def search(request):
    form = SearchForm()
    tags = BusinessTag.objects.all()
    tag_names = [tag.name for tag in tags]
    context = {'tag_names': tag_names, 'form': form}
    return render(request, 'search.html', context)


# page of search
def results(request):
    tools = Tool.objects.all()
    page = request.GET.get('page',1)
    # 20 results per page
    paginator = Paginator(tools,20)

    form = SearchForm(request.GET)
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()

    if form.is_valid():
        # filter removes empty strings from the list
        words = list(filter(None, form.data['text_search'].split()))
        tags = list(filter(None, form.data['tag_search'].split(',')))

        # filter by active
        tools = tools.filter(active__iexact=1).order_by('name')

        # filter by words
        for word in words:
            tools = tools.filter(name__icontains=word) | tools.filter(short_description__icontains=word) | tools.filter(long_description__icontains=word)

        # filter by tags
        for tag in tags:
            tools = tools.filter(business_tags__name__iexact=tag)

        try:
            toolresults = paginator.page(page)
        except PageNotAnInteger:
            toolresults = paginator.page(1)
        except EmptyPage:
            toolresults = paginator.page(paginator.num_pages)


        context = {'tools': toolresults, 'parameters': parameters}
        return render(request, 'results.html', context)
    return render(request, 'search.html', {'form': form})


# informational page for a tool
def tool(request, tool_id):
    tool = Tool.objects.get(pk=tool_id)
    last_update = Update.objects.filter(tool=tool).latest('date')
    context = {'tool': tool, 'last_update': last_update}
    return render(request, 'tool.html', context)


# page of tools associated with user
def my_tools(request):
    current_user = get_current_user(request)
    tools = list(Tool.objects.filter(owner=current_user))
    context = {'tools': tools}
    return render(request, 'my_tools.html', context)


# page to add a new tool
def add_tool(request):

    if request.method == 'GET':
        form = ToolForm()

        tags1 = DependencyTag.objects.all()
        tags2 = BusinessTag.objects.all()
        tag_names_d = [tag.name for tag in tags1]
        tag_names_b = [tag.name for tag in tags2]

        context = {'form': form, 'tag_names_d': tag_names_d, 'tag_names_b': tag_names_b}
        return render(request, 'add_tool.html', context)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ToolForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            tool = form.save(commit=False)
            tool.owner = get_current_user(request)
            tool.created_by = get_current_user(request).name

            # save both tool, and many-to-many fields for tool
            tool.save()
            form.save_m2m()

            tool.register_update(get_current_user(request), 'Added to register')

            # redirect to my tools
            return redirect('my_tools')
        return render(request, 'add_tool.html', {'form': form})

# page to add a new tag
def tags(request):
    if request.method == 'GET':
        dependencytag_form = DependencyTagForm()
        businesstag_form = BusinessTagForm()

        businesstags = BusinessTag.objects.all()
        dependencytags = DependencyTag.objects.all()
        businesstag_names = [tag.name for tag in businesstags]
        dependencytag_names = [tag.name for tag in dependencytags]

        context = {'dependencytag_form': dependencytag_form, 'businesstag_form': businesstag_form, \
            'dependencytag_names': dependencytag_names, 'businesstag_names': businesstag_names}
        return render(request, 'tags.html', context)


def add_dependencytag(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DependencyTagForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            tag = form.save(commit=False)
            # save both tool, and many-to-many fields for tool
            tag.save()
            form.save_m2m()

            # redirect back to tags
            return redirect('tags')


def add_businesstag(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form2 = BusinessTagForm(request.POST)

        # check whether it's valid:
        if form2.is_valid():
            tag = form2.save(commit=False)

            # save both tool, and many-to-many fields for tool
            tag.save()
            form2.save_m2m()

            # redirect back to tags
            return redirect('tags')


# page to edit an existing tool
def edit_tool(request, tool_id):
    tool = Tool.objects.get(pk=tool_id)

    if tool.owner == get_current_user(request):
        if request.method == 'GET':
            form = ToolForm(instance=tool)

            context = {'tool': tool, 'form': form}
            return render(request, 'edit_tool.html', context)

        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = ToolForm(request.POST, instance=tool)

            # check whether it's valid:
            if form.is_valid():
                tool = form.save(commit=False)

                # save both tool, and many-to-many fields for tool
                tool.save()
                form.save_m2m()

                tool.register_update(get_current_user(request), 'Edited fields')

                # redirect to the tool page
                return redirect('tool', tool_id=tool.id)

            return render(request, 'edit_tool.html', {'tool': tool, 'form': form})
    return redirect('search')


# url to delete an existing tool
def delete_tool(request, tool_id):
        tool = Tool.objects.get(pk=tool_id)

        if tool.owner == get_current_user(request):
            tool.delete()

            # redirect to my tools
            return redirect('my_tools')
        return redirect('search')    


# url to transfer ownership of an existing tool
def transfer_tool(request, tool_id):
    tool = Tool.objects.get(pk=tool_id)

    if request.method == 'GET':
        context = {'tool': tool}
        return render(request, 'transfer_tool.html', context)

    if request.method == 'POST':
        sesas = find_users_sesas(request.POST['name_input'])
        if len(sesas) > 0:
            user = get_or_create_user(sesas[0])
            tool.owner = user
            tool.save()
            return redirect('my_tools')
        else:
            context = {'tool': tool}
            return render(request, 'transfer_tool.html', context)


# list of analytics repots
def reports(request):
    context = {}
    return render(request, 'reports.html', context)


# about page
def about(request):
    context = {}
    return render(request, 'about.html', context)


# contact the developers page
def contact_devs(request):
    if request.method == 'GET':
        form = FeedbackForm()
        context = {'form': form}
        return render(request, 'contact_devs.html', context)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)

        # check whether it's valid
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.sesa = get_current_user(request).sesa
            feedback.save()

            return redirect('search')


# function to search for users
def find_users(request):
    name_search = request.GET['name']
    results = ldap.get_name(name_search)
    name_list = []
    for person in results:
        name_list.append(person.displayName.value)
    return JsonResponse(name_list, safe=False)


# function to obtain user sesas
def find_users_sesas(name):
    results = ldap.get_name(name)
    sesa_list = []
    for person in results:
        sesa_list.append(person.employeeID.value)
    return sesa_list


# function to grab current user
def get_current_user(request):
    try:
        sesa = request.META['REMOTE_USER']
        sesa = sesa.split('\\')[-1]
    except KeyError:
        sesa = 'Default'
    user = get_or_create_user(sesa)
    return user

def get_or_create_user(sesa):
    user = User.objects.filter(sesa=sesa).first()
    if user is None:
        user = User(sesa=sesa)
        ldap.sync_user(user)
    return user
