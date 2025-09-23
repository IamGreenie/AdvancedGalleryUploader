from django.shortcuts import render

# Create your views here.
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from .models import Image, Comment
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import Case, When

class ImageCreateView(CreateView):
    model = Image
    fields = ['title', 'image', 'tags']
    template_name = 'gallery/upload.html'
    success_url = reverse_lazy('image-list')

    def form_valid(self, form):
        form.instance.session_key = self.request.session.session_key
        return super().form_valid(form)

class ImageListView(ListView):
    model = Image
    template_name = 'gallery/image_list.html'
    context_object_name = 'images'

    def get_queryset(self):
        tag = self.request.GET.get('tag')
        if tag:
            # Prioritize matching images first, then others
            matching = Image.objects.filter(tags__icontains=tag)
            others = Image.objects.exclude(tags__icontains=tag)
            return list(matching) + list(others)
        return Image.objects.all()


class PersonalGalleryView(ListView):
    model = Image
    template_name = 'gallery/personal_gallery.html'
    context_object_name = 'images'

    def get_queryset(self):
        session_key = self.request.session.session_key
        if not session_key:
            self.request.session.create()
        return Image.objects.filter(session_key=session_key)

class ImageDetailView(DetailView):
    model = Image
    template_name = 'gallery/image_detail.html'
    context_object_name = 'image'
    def get(self, request, *args, **kwargs):
        image = self.get_object()
        # Ensure the user can only view their own images
        viewed = request.session.get('viewed_images', [])
        if image.id not in viewed:
            viewed.append(image.id)
            request.session['viewed_images'] = viewed

        return super().get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        image = self.get_object()
        comment = request.POST.get('text')
        if comment:
            Comment.objects.create(image=image, text=comment)
        return redirect('image-detail', pk=image.pk)
    
class ViewingHistoryView(ListView):
    model = Image
    template_name = 'gallery/history.html'
    context_object_name = 'images'

    def get_queryset(self):
        viewed_ids = self.request.session.get('viewed_images', [])
        viewed_ids = list(reversed(viewed_ids))  # Show most recent first
        preserved_order = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(viewed_ids)])
        return Image.objects.filter(id__in=viewed_ids).order_by(preserved_order)
