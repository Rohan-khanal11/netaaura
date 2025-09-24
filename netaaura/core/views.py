from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Avg
from .models import Politician, Rating, Comment
from .forms import PoliticianForm, RatingForm, CommentForm
from django.contrib.admin.views.decorators import staff_member_required

# ----------------------------
# Admin-only decorator
# ----------------------------
def admin_required(view_func):
    return login_required(user_passes_test(lambda u: u.is_staff)(view_func))


# ----------------------------
# List all approved politicians
# ----------------------------

def politician_list(request):
    politicians = Politician.objects.filter(is_approved=True)
    context = {
        'politicians': politicians
    }
    if request.user.is_authenticated:
        for p in politicians:
            p.user_rating = p.rating_set.filter(user=request.user).first()
    else:
        for p in politicians:
            p.user_rating = None

    return render(request, "core/politician_list.html", {"politicians": politicians})

# ----------------------------
# Politician detail + ratings + comments
# ----------------------------
def politician_detail(request, pk):
    politician = get_object_or_404(Politician, pk=pk, is_approved=True)
    ratings = politician.rating_set.all()
    comments = Comment.objects.filter(rating__politician=politician)

    rating_form = RatingForm()
    comment_form = CommentForm()

    # Handle comment submission
    if request.method == "POST" and "comment_submit" in request.POST:
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.politician = politician
                comment.user = request.user
                comment.save()
                messages.success(request, "Comment added!")
                return redirect("politician_detail", pk=pk)
        else:
            messages.error(request, "You must be logged in to comment.")
            return redirect("login")

    context = {
        "politician": politician,
        "ratings": ratings,
        "comments": comments,
        "rating_form": rating_form,
        "comment_form": comment_form,
    }
    return render(request, "core/politician_detail.html", context)


# ----------------------------
# Add new politician
# ----------------------------
@login_required
def add_politician(request):
    if request.method == "POST":
        form = PoliticianForm(request.POST, request.FILES)
        if form.is_valid():
            politician = form.save(commit=False)
            politician.created_by = request.user
            politician.is_approved = False  # Needs admin approval
            politician.save()
            messages.success(request, "Politician added successfully!")
            return redirect("politician_list")
    else:
        form = PoliticianForm()
    return render(request, "core/add_politician.html", {"form": form})


# ----------------------------
# Submit rating for a politician (update if already rated)
# ----------------------------
@login_required
def rate_politician(request, pk):
    politician = get_object_or_404(Politician, pk=pk, is_approved=True)

    if request.method == "POST":
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                user=request.user,
                politician=politician,
                defaults={'aura_score': form.cleaned_data['aura_score']}
            )
            messages.success(request, "Your rating has been saved!")
            return redirect("politician_detail", pk=pk)

    return redirect("politician_detail", pk=pk)


# ----------------------------
# Admin: Approve politicians
# ----------------------------
@admin_required
def approve_politicians_view(request):
    politicians = Politician.objects.filter(is_approved=False)

    for p in politicians:
        # Aura given by current user (optional)
        try:
            user_rating = Rating.objects.get(user=request.user, politician=p)
            p.aura_given = user_rating.aura_score
        except Rating.DoesNotExist:
            p.aura_given = None

        # Average aura
        avg = p.rating_set.aggregate(Avg('aura_score'))['aura_score__avg']
        p.average_aura = round(avg, 2) if avg is not None else "N/A"

    return render(request, "core/approve_politicians.html", {"politicians": politicians})


# ----------------------------
# Admin: Approve a single politician
# ----------------------------
@admin_required
def approve_politician_action(request, pk):
    politician = get_object_or_404(Politician, pk=pk, is_approved=False)
    politician.is_approved = True
    politician.save()
    messages.success(request, f"{politician.name} approved!")
    return redirect("approve_politicians")


# ----------------------------
# Admin: Delete politicians
# ----------------------------
@admin_required  # already defined in your code
def delete_politician(request, pk):
    politician = get_object_or_404(Politician, pk=pk)
    if request.method == "POST":
        politician.delete()
        messages.success(request, f"{politician.name} has been deleted!")
        return redirect("politician_list")
    return render(request, "core/confirm_delete.html", {"politician": politician})
