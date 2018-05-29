from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect
import datetime as dt
from .models import Image, Profile, Comment
from .forms import InfoImageForm, NewsLetterForm, CommentForm, EditProfileForm
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='/accounts/login')
def latest_images(request):
    date = dt.date.today()
    image = Image.todays_images()

    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']
            recipient = NewsLetterRecipients(name=name, email=email)
            recipient.save()
            send_welcome_email(name, email)

            HttpResponseRedirect('latest')

    else:
        form = NewsLetterForm()
    return render(request, 'allofinsta/insta-home.html', {"date": date, "image": image, "letterform": form})


@login_required(login_url='/accounts/login')
def search_results(request):
    searched_images = Image.search_by_title()

    if 'image' in request.GET and request.GET["image"]:
        search_term = request.GET.get("image")
        message = f"{search_term}"

        return render(request, 'allofinsta/search.html', {"message": message, "images": searched_images})

    else:
        message = "You haven't searched for any term"
        return render(request, 'allofinsta/search.html', {"message": message})


@login_required(login_url='/accounts/login/')
def image_detail(request, id):
    test = 'test'
    image = Image.objects.get(id=id)
    return render(request, 'allofinsta/home.html', {'image': image, 'test': test})


@login_required(login_url='/accounts/login/')
def image(request, image_id):
    try:
        image = Image.objects.get(id=image_id)
    except DoesNotExist:
        raise Http404()
    return render(request, "allofinsta/image.html", {"image": image})


@login_required(login_url='/accounts/login')
def new_image(request):
    current_user = request.user
    if request.method == 'POST':
        form = InfoImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.editor = current_user
            image.save()
    else:
        form = InfoImageForm()
    return render(request, "new_image.html", {"form": form})


@login_required(login_url='/accounts/login/')
def profile(request, profile_id):
    title = 'Profile Page'
    current_user = request.user
    profile = Profile.get_profile(creator__username__iexact=profile_id)
    image = Image.get_images()
    comments = Comment.get_comment()
    return render(request, 'profiles/profile.html', {"title": title, "comments": comments, "image": image, "user": current_user, "profile": profile})


@login_required(login_url='/accounts/login/')
def account_details(request):
    title = 'Instagram'
    settings = Profile.get_profile()
    return render(request, 'profiles/account_details.html', {"settings": settings, "title": title})


@login_required(login_url='/accounts/login/')
def edit(request):
    title = 'Instagram'
    current_user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            update = form.save(commit=False)
            update.user = current_user
            update.save()
            return redirect('profile')
    else:
        form = EditProfileForm()
    return render(request, 'profiles/edit_profile.html', {"title": title, "form": form})


@login_required(login_url='/accounts/login/')
def after_detail(request, id):
    # return HttpResponse(slug)
    image = Image.objects.filter(id=id).all()
    return render(request, 'allofinsta/after.html', {'image': image})


@login_required(login_url="/accounts/login/")
def view_your_profile(request, pk):
    title = "Instagram"
    current_user = request.user
    image = Image.get_images()
    profile = Profile.get_profile()
    comment = Comment.get_comment()
    user = get_object_or_404(User, pk=pk)
    return render(request, 'profiles/view.html', {"user": current_user, "images": image, "my_user": user, "comments": comment, "profile": profile, "title": title})


@login_required(login_url='/accounts/login/')
def new_comment(request, pk):
    image = get_object_or_404(Image, pk=id)
    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = image
            comment.user = current_user
            comment.save()
            return redirect('home')
    else:
        form = CommentForm()
    return render(request, 'comment.html', {"user": current_user, "comment_form": form})


@login_required(login_url="/accounts/login/")
def like(request, operation, pk):
    image = get_object_or_404(Image, pk=pk)
    if operation == 'like':
        image.likes += 1
        image.save()
    elif operation == 'unlike':
        image.likes -= 1
        image.save()
    return redirect('home')
