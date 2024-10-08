import os
import random
import tkinter as tk
from PIL import Image, ImageTk
import pygame

# Initialize pygame mixer for sound effects
pygame.mixer.init()

# Load sound effects
try:
    correct_sound = pygame.mixer.Sound("sounds/correct.mp3")
    incorrect_sound = pygame.mixer.Sound("sounds/incorrect.mp3")
    game_over_sound = pygame.mixer.Sound("sounds/game_over.mp3")
    new_game_sound = pygame.mixer.Sound("sounds/new_game.mp3")
    print("Sound files loaded successfully.")
except Exception as e:
    print(f"Error loading sound files: {e}")

# Function to play sound effects without overlap
def play_sound(sound):
    sound.stop()
    sound.play()

# Load player images and names from the player_images directory
def load_player_images(folder):
    player_images = {}
    for filename in os.listdir(folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            player_name = filename[:-4].replace('-', ' ').title()
            player_images[player_name] = os.path.join(folder, filename)
    return player_images

# Function to handle the guessing game
def guess_the_player():
    global player_name, attempts_remaining, displayed_name, horse_word
    player_name = random.choice(list(player_images.keys()))
    attempts_remaining = 5
    displayed_name = '_' * len(player_name.replace(' ', ''))
    label_displayed_name.config(text=' '.join(displayed_name))
    label_attempts.config(text=f"Attempts remaining: {attempts_remaining}")

    player_image = Image.open(player_images[player_name])
    img_tk = ImageTk.PhotoImage(player_image.resize((200, 200)))
    label_img.config(image=img_tk)
    label_img.image = img_tk

    horse_word = ['_'] * 5
    label_horse.config(text=' '.join(horse_word))

    play_sound(new_game_sound)

    entry_guess.delete(0, tk.END)
    entry_guess.focus()

# Function to check the user's guess
def check_guess():
    global displayed_name, attempts_remaining, horse_word
    
    guess = entry_guess.get().strip().title()
    
    if guess.lower() == player_name.lower():
        play_sound(correct_sound)
        show_custom_message("Congratulations!", f"You won! The player is {player_name}.")
        guess_the_player()  # Start a new game
    else:
        attempts_remaining -= 1
        play_sound(incorrect_sound)

        if attempts_remaining > 0:
            label_feedback.config(text=f"Incorrect guess! Attempts remaining: {attempts_remaining}.")
            give_random_letter_hint()
            add_to_horse_word()
        else:
            play_sound(game_over_sound)
            label_feedback.config(text=f"Sorry, you've run out of attempts! The correct answer was {player_name}.")
            guess_the_player()

# Function to show a custom message box with a GIF
def show_custom_message(title, message):
    msg_box = tk.Toplevel(root)
    msg_box.title(title)
    msg_box.geometry("500x300")
    msg_box.configure(bg='blue')

    # Load the GIF
    gif_path = "image/correct.gif"  # Change to your GIF file path
    gif = Image.open(gif_path)

    # Create a label to display the GIF
    gif_label = tk.Label(msg_box, bg='blue')
    gif_label.pack(pady=10)

    # Use an ImageTk.PhotoImage to create an image that Tkinter can use
    frames = [ImageTk.PhotoImage(gif.copy().convert("RGBA").resize((100, 100))) for _ in range(gif.n_frames)]

    def update_gif(frame_index):
        gif_label.configure(image=frames[frame_index])
        msg_box.after(100, update_gif, (frame_index + 1) % len(frames))

    update_gif(0)

    # Message label
    label_message = tk.Label(msg_box, text=message, font=('Helvetica', 14), bg='blue', fg='white')
    label_message.pack(pady=10)

    # Close button
    btn_close = tk.Button(msg_box, text="Close", command=lambda: close_message_box(msg_box), font=('Helvetica', 12), bg='#f44336', fg='white')
    btn_close.pack(pady=10)

# Function to stop the sound when the message box is closed
def close_message_box(msg_box):
    msg_box.destroy()
    pygame.mixer.stop()  # Stop the correct sound

# Give a random letter from the player's name as a hint
def give_random_letter_hint():
    global displayed_name
    random_letter = random.choice([char for char in player_name if char.isalpha() and char not in displayed_name])
    if random_letter:
        displayed_name = ''.join(
            original if original.lower() == random_letter.lower() else hidden
            for original, hidden in zip(player_name.replace(' ', ''), displayed_name)
        )
        label_displayed_name.config(text=' '.join(displayed_name))

# Add to the "HORSE" word in the top right corner
def add_to_horse_word():
    global horse_word
    letters = "HORSE"
    for i in range(len(horse_word)):
        if horse_word[i] == '_' and (5 - attempts_remaining) > i:
            horse_word[i] = letters[i]
            break
    label_horse.config(text=' '.join(horse_word))

# Load player images
player_images = load_player_images('player_images')

# Tkinter setup
root = tk.Tk()
root.title("NBA Player Guessing Game")
root.geometry("900x700")
root.configure(bg='blue')

# Player Image Label
label_img = tk.Label(root, bg='blue')
label_img.pack(pady=20)

# Displayed Name Label
label_displayed_name = tk.Label(root, text='', font=('Helvetica', 32, 'bold'), bg='navy', fg='white')
label_displayed_name.pack(pady=20)

# Attempts Label
label_attempts = tk.Label(root, text='', font=('Helvetica', 14), bg='blue', fg='white')
label_attempts.pack(pady=5)

# Feedback Label
label_feedback = tk.Label(root, text='', font=('Helvetica', 14), bg='blue', fg='white')
label_feedback.pack(pady=5)

# Horse Word Label
label_horse = tk.Label(root, text='H O R S E', font=('Helvetica', 14), bg='blue', fg='white', anchor='e')
label_horse.pack(pady=5, padx=10, anchor='ne')

# Entry field for guesses
entry_guess = tk.Entry(root, width=40, font=('Helvetica', 14), bd=0, relief=tk.FLAT, bg='navy', fg='white')
entry_guess.pack(pady=10)
entry_guess.focus()

# Hover effects for buttons
def on_enter(e):
    e.widget['bg'] = '#5cb85c'

def on_leave(e):
    e.widget['bg'] = '#4CAF50'

# Guess Button
btn_guess = tk.Button(root, text="Submit Guess", command=check_guess, font=('Helvetica', 14), bg='#4CAF50', fg='white', borderwidth=0)
btn_guess.pack(pady=5)
btn_guess.bind("<Enter>", on_enter)
btn_guess.bind("<Leave>", on_leave)

# New Game Button
btn_new_game = tk.Button(root, text="New Game", command=guess_the_player, font=('Helvetica', 14), bg='#f44336', fg='white', borderwidth=0)
btn_new_game.pack(pady=10)
btn_new_game.bind("<Enter>", on_enter)
btn_new_game.bind("<Leave>", on_leave)

# Start the first game
guess_the_player()

# Run the application
root.mainloop()

# Stop the correct sound when exiting
pygame.mixer.quit()
