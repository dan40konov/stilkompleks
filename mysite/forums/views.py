from forums.models import Forum, Comment

from django.views import View
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from django.contrib.auth.mixins import LoginRequiredMixin

from forums.forms import CommentForm


class ForumListView(ListView):
    """
    Sub-class the ListView to pass the request to the form.
    """
    model = Forum
    template_name = "forums/list.html"


class ForumDetailView(DetailView):
    """
    Sub-class the DetailView to pass the request to the form.
    """
    model = Forum
    template_name = "forums/detail.html"
    def get(self, request, pk) :
        x = Forum.objects.get(id=pk)
        comments = Comment.objects.filter(forum=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'forum' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

class ForumCreateView(LoginRequiredMixin, CreateView):
    """
    Sub-class of the CreateView to automatically pass the Request to the Form
    and add the owner to the saved object.
    """
    model = Forum
    template_name = "forums/form.html"
    fields = ['text', 'title']
    # Saves the form instance, sets the current object for the view, and redirects to get_success_url().
    def form_valid(self, form):
        print('form_valid called')
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super(ForumCreateView, self).form_valid(form)


class ForumUpdateView(LoginRequiredMixin, UpdateView):
    """
    Sub-class the UpdateView to pass the request to the form and limit the
    queryset to the requesting user.
    """
    model = Forum
    template_name = "forums/form.html"
    fields = ['text', 'title']
    def get_queryset(self):
        print('update get_queryset called')
        """ Limit a User to only modifying their own data. """
        qs = super(ForumUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)


class ForumDeleteView(LoginRequiredMixin, DeleteView):
    """
    Sub-class the DeleteView to restrict a User from deleting other
    user's data.
    """
    model = Forum
    template_name = "forums/delete.html"
    def get_queryset(self):
        print('delete get_queryset called')
        qs = super(ForumDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        f = get_object_or_404(Forum, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, forum=f)
        comment.save()
        return redirect(reverse('forums:forum_detail', args=[pk]))

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "forums/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        forum = self.object.forum
        return reverse('forums:forum_detail', args=[forum.id])

