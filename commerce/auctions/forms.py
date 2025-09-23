from django import forms
from .models import AuctionListing, Bid, Comment

class CreateListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']
        labels = {
            'starting_bid': 'Starting Price (Credits)',
            'image_url': 'Image URL (optional)',
            'category': 'Category (optional)',
        }
        widgets = {
          'description': forms.Textarea(attrs={'rows':4}),
          'image_url': forms.URLInput(attrs={'placeholder':'https://...'}),
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        labels = {'amount': 'Your Bid (Credits)'}
        widgets = {'amount': forms.NumberInput(attrs={'step':'0.01'})}

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': 'Add a comment'}
        widgets = {'content': forms.Textarea(attrs={'rows':3})}

