from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import AuctionListing, User, Watchlist, Category
from .forms import CreateListingForm, BidForm, CommentForm
from django.contrib import messages

def index(request):
    listings = AuctionListing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



@login_required
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user  
            listing.active = True        
            listing.save()
            return redirect("index")
    else:
        form = CreateListingForm()

    return render(request, "auctions/create_listing.html", {
        "form": form
    })

def listing_detail(request, listing_id):
    listing = get_object_or_404(AuctionListing, pk=listing_id)
    bids = listing.bids.all()
    comments = listing.comments.all()
    current_price = listing.current_price()

    watchlisted = False
    if request.user.is_authenticated:
        watchlisted = Watchlist.objects.filter(user=request.user, listing=listing).exists()

    if request.method == "POST":
        # handle bid, comment, watchlist add/remove, or close auction here
        if 'watchlist_add' in request.POST:
            if request.user.is_authenticated:
                Watchlist.objects.get_or_create(user=request.user, listing=listing)
                messages.success(request, "Added to your watchlist.")
                return redirect('listing_detail', listing_id=listing.id)
            else:
                messages.error(request, "You must be logged in to add to watchlist.")

        elif 'watchlist_remove' in request.POST:
            if request.user.is_authenticated:
                Watchlist.objects.filter(user=request.user, listing=listing).delete()
                messages.success(request, "Removed from your watchlist.")
                return redirect('listing_detail', listing_id=listing.id)

            else:
                messages.error(request, "You must be logged in to remove from watchlist.")

        elif 'place_bid' in request.POST:
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                bid_amount = bid_form.cleaned_data['amount']
                if bid_amount >= listing.starting_bid and bid_amount > current_price:
                    new_bid = bid_form.save(commit=False)
                    new_bid.bidder = request.user
                    new_bid.listing = listing
                    new_bid.save()
                    messages.success(request, "Bid placed successfully!")
                    return redirect('listing_detail', listing_id=listing.id)
                else:
                    messages.error(request, "Bid must be higher than current price and starting bid.")
            comment_form = CommentForm()
        elif 'add_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.listing = listing
                comment.save()
                messages.success(request, "Comment added!")
                return redirect('listing_detail', listing_id=listing.id)
            
        elif 'close_auction' in request.POST and request.user == listing.owner:
            highest_bid = listing.bids.order_by('-amount').first()
            if highest_bid:
              listing.winner = highest_bid.bidder 
            listing.active = False  
            listing.save()
            messages.success(request, "Auction closed!")
            return redirect('listing_detail', listing_id=listing.id)

        
        else:
            bid_form = BidForm()
            comment_form = CommentForm()
    else:
        bid_form = BidForm()
        comment_form = CommentForm()

    return render(request, "auctions/listing_detail.html", {
        "listing": listing,
        "bids": bids,
        "comments": comments,
        "current_price": current_price,
        "watchlisted": watchlisted,
        "bid_form": bid_form,
        "comment_form": comment_form,
    })

@login_required
def watchlist(request):
    listings = AuctionListing.objects.filter(watchlisted_by__user=request.user)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })



def categories(request):
    categories = ["Electronics", "Fashion", "Starships", "Books"]
    for name in categories:
        Category.objects.get_or_create(name=name)

    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": categories})

def category_listings(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = AuctionListing.objects.filter(category=category, active=True)
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings
    })

