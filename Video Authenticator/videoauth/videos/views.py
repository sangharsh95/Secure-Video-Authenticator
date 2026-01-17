from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Video
from .forms import VideoForm
from .utils import verify_video

def video_list(request):
    videos = Video.objects.all()
    return render(request, template_name='videos/video_list.html', context={'videos': videos})

@login_required
def video_upload(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.uploaded_by = request.user
            video.save()
            # Run the verification
            video.verification_status = verify_video(video.file.path)
            video.save()
            return redirect('video_list')
    else:
        form = VideoForm()
    return render(request, template_name='videos/video_upload.html', context={'form': form})