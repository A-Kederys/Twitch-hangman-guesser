import os
import requests
from dotenv import load_dotenv
from collections import Counter

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
OAUTH_TOKEN = os.getenv('OAUTH_TOKEN')

# Endpoint to fetch global emotes
url = "https://api.twitch.tv/helix/chat/emotes/global"

headers = {
    'Client-ID': CLIENT_ID,
    'Authorization': f'Bearer {OAUTH_TOKEN}'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    emote_names = []

    # Extracting and filter emotes
    for emote in data['data']:
        emote_name = emote['name']
        # Filtering out emotes containing unnecessary chars'
        if not any(char in emote_name for char in ":;<()._-"):
            emote_names.append(emote_name)

    # Counting occurrences of each letter for all emotes
    letter_count = Counter()
    for emote_name in emote_names:
        letter_count.update(emote_name.lower())

    # Filtering only alphabetic characters and sort them by count in descending order
    sorted_letter_count = sorted(
        ((char, count) for char, count in letter_count.items() if char.isalpha()),
        key=lambda x: x[1],
        reverse=True  #in descending
    )

    # Printing the top 3 letters for all emotes
    print("Top 3 Letters in Overall Emotes:")
    for char, count in sorted_letter_count[:3]:
        print(f"{char} - {count}")
    
    # Asking the user how many letters-long emotes they want to see
    try:
        num_letters = int(input("\nEnter the number of letters for emotes you'd like to see: "))
        
        if num_letters > 0:
            matching_emotes = [emote for emote in emote_names if len(emote) == num_letters]
            
            if matching_emotes:
                # Sorting matching emotes alphabetically
                matching_emotes.sort(key=lambda x: x.lower())

                print(f"\nEmotes with {num_letters} letters:")
                for i in range(0, len(matching_emotes), 3):
                    print(' | '.join(matching_emotes[i:i+3]))
                
                # Counting occurrences of each letter for filtered emotes
                filtered_letter_count = Counter()
                for emote in matching_emotes:
                    filtered_letter_count.update(emote.lower())

                # Sorting filtered letter count
                sorted_filtered_letter_count = sorted(
                    ((char, count) for char, count in filtered_letter_count.items() if char.isalpha()),
                    key=lambda x: x[1],
                    reverse=True
                )

                # Printing the top 3 letters for filtered emotes
                print(f"\nTop 3 Letters in {num_letters}-Letter Emotes:")
                for char, count in sorted_filtered_letter_count[:3]:
                    print(f"{char} - {count}")

                while True:
                    try:
                        position = int(input("\nEnter the letter position you guessed: ")) - 1

                        if 0 <= position < num_letters:
                            guessed_letter = input(f"Enter the letter you guessed in position {position + 1}: ").lower()

                            # Filtering emotes by the guessed letter in the specified position
                            matching_by_position = [
                                emote for emote in matching_emotes if emote.lower()[position] == guessed_letter
                            ]

                            if matching_by_position:
                                # Sorting filtered emotes by position alphabetically
                                matching_by_position.sort(key=lambda x: x.lower())

                                print(f"\nEmotes with {num_letters} letters and '{guessed_letter}' in position {position + 1}:")
                                for i in range(0, len(matching_by_position), 3):
                                    print(' | '.join(matching_by_position[i:i+3]))

                                # Counting occurrences of each letter for the position-filtered emotes
                                position_filtered_letter_count = Counter()
                                for emote in matching_by_position:
                                    position_filtered_letter_count.update(emote.lower())

                                # Sorting and displaying the top 3 letters in the position-filtered set
                                sorted_position_filtered_letter_count = sorted(
                                    ((char, count) for char, count in position_filtered_letter_count.items() if char.isalpha()),
                                    key=lambda x: x[1],
                                    reverse=True
                                )

                                print(f"\nTop 3 Letters in Emotes with '{guessed_letter}' in position {position + 1}:")
                                for char, count in sorted_position_filtered_letter_count[:3]:
                                    print(f"{char} - {count}")

                            else:
                                print(f"No emotes found with {guessed_letter} in position {position + 1}.")
                            break  # Exiting the loop when a valid position is entered

                        else:
                            print(f"Invalid position. Please enter a position between 1 and {num_letters}.")

                    except ValueError:
                        print("Invalid input. Please enter a valid number.")

            else:
                # If no emotes match the specified number of letters
                print(f"No emotes found with {num_letters} letters.")
        else:
            # If the number of letters is non-positive, inform the user
            print("Please enter a positive number.")
    
    except ValueError:
        # If the user input for the number of letters is not a valid integer
        print("Invalid input. Please enter a valid number.")

else:
    print(f"Error fetching emotes: {response.status_code} {response.text}")