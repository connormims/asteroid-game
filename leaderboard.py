import json
import os

FILENAME = "leaderboard.json"

def load_leaderboard():
    if not os.path.exists(FILENAME):
        return [] # Return empty list if no file exists yet
    with open(FILENAME, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_score(name, score):
    scores = load_leaderboard()
    scores.append({"name": name, "score": score})
    
    # Sort by score descending and keep only top 5
    scores = sorted(scores, key=lambda x: x['score'], reverse=True)[:5]
    
    with open(FILENAME, "w") as f:
        json.dump(scores, f, indent=4)

def display_leaderboard(screen, screen_width, screen_height, large_font, font):
    # 1. Load the data
    top_scores = load_leaderboard() # From your leaderboard.py
    
    # 2. Draw a Header
    header_surf = large_font.render("TOP PILOTS", True, (255, 215, 0)) # Gold
    header_rect = header_surf.get_rect(center=(screen_width/2, screen_height/2 - 200))
    screen.blit(header_surf, header_rect)

    # 3. Iterate and Draw each score
    for i, entry in enumerate(top_scores):
        # Calculate Y position dynamically for each row
        y_offset = screen_height/2 + 150 + (i * 35)
        
        name = entry['name']
        val = entry['score']
        
        # Create the text string
        text = f"{i+1}. {name.upper():<10} {val:>5}"
        
        score_surf = font.render(text, True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(screen_width/2, y_offset - 200))
        screen.blit(score_surf, score_rect)