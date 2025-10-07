from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .forms import PuzzleForm
import math, random

def home(request):
    result, attempts = None, []
    if request.method == 'POST':
        form = PuzzleForm(request.POST)
        if form.is_valid():
            n = form.cleaned_data['number']
            text = form.cleaned_data['text']

            number_msg = (f"The number {n} is even. Its square root is {round(math.sqrt(n),4)}."
                          if n % 2 == 0 else f"The number {n} is odd. Its cube is {n**3}.")

            binary = ' '.join(format(ord(ch), '08b') for ch in text)
            vowels = sum(1 for ch in text.lower() if ch in 'aeiou')

            secret = random.randint(1, 100)
            low, high, win = 1, 100, False
            for i in range(1, 6):
                guess = (low + high) // 2
                if guess > secret:
                    attempts.append(f"Attempt {i}: {guess} (Too high!)"); high = guess - 1
                elif guess < secret:
                    attempts.append(f"Attempt {i}: {guess} (Too low!)"); low = guess + 1
                else:
                    attempts.append(f"Attempt {i}: {guess} (Correct!)"); win = True; break

            result = {
                'number_msg': number_msg,
                'binary': binary,
                'vowel_count': vowels,
                'secret': secret,
                'attempts': attempts,
                'win': win,
            }
    else:
        form = PuzzleForm()
    return render(request, 'puzzle/home.html', {'form': form, 'result': result})
