from django.shortcuts import render
from django.http import HttpResponse
import random


QUOTES = [
    "You must be the change you wish to see in the world.",
    "Well done is better than well said.",
    "Do not go where the path may lead, go instead where there is no path and leave a trail."
]


IMAGES = [
    "/static/images/mahatma-gandhi.jpg.webp",
    "/static/images/benjamin_franklin.jpeg",
    "/static/images/emerson-ralph-waldo.jpg"
]

QUOTES_IMAGES = list(zip(QUOTES, IMAGES))


def index(request):
    quote_image = random.choice(QUOTES_IMAGES)
    context = {'quote': quote_image[0], 'image': quote_image[1]}
    return render(request, 'quotes/quote.html', context)

def quote(request):
    quote = random.choice(QUOTES)
    image = random.choice(IMAGES)
    context = {'quote': quote, 'image': image}
    return render(request, 'quotes/quote.html', context)

def show_all(request):
    context = {'quotes_images': QUOTES_IMAGES}
    return render(request, 'quotes/show_all.html', context)


def about(request):
    context = {
        'creator': 'John Liu',
        'bio': {
            'ghandi': 'Mahatma Gandhi was an Indian lawyer, anti-colonial nationalist, and political ethicist who employed nonviolent resistance to lead the successful campaign for India’s independence from British rule.',
            'franklin': 'Benjamin Franklin was one of the Founding Fathers of the United States, renowned for his contributions to science, diplomacy, and his role in drafting the Declaration of Independence.',
            'emerson': 'Ralph Waldo Emerson was an American essayist, lecturer, philosopher, and poet, who led the transcendentalist movement of the mid-19th century.'
        }
    }
    return render(request, 'quotes/about.html', context)
