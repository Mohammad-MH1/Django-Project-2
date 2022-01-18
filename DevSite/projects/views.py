
from django.shortcuts import redirect, render
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import searchProjects, paginationProjects


def projects(request):
    # imported form utils.py
    projects, search_query = searchProjects(request)
    custom_range, projects = paginationProjects(request, projects, 6)

    context = {'projects': projects,
               'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    form = ReviewForm()
    projectObj = Project.objects.get(id=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount

        messages.success(request, 'your review was succesfully submitted!')
        return redirect('project', pk=projectObj.id)

    return render(request, 'projects/single-project.html', {'projectObj': projectObj, 'form': form})


@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()

        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    form = ProjectForm(instance=project)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()

        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    context = {'form': form, 'project': project}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'delete_template.html', context)
