import pandas as pd
import numpy as np
import time
import random
import keyboard  

class FlappyBird:
    def __init__(self, width=20, height=10):
        self.width = width
        self.height = height
        self.bird_pos = height // 2
        self.bird_char = '🐦'
        self.gap_size = 4
        self.pipe_width = 3
        self.pipe_char = '▓'
        self.empty_char = ' '
        self.gravity = 1
        self.jump_force = -2
        self.velocity = 0
        self.score = 0
        self.game_over = False
        self.pipes = []
        
        # Initialize game board as a pandas DataFrame
        self.board = pd.DataFrame(
            np.full((height, width), self.empty_char),
            columns=[str(i) for i in range(width)]
        )
        
    def add_pipe(self):
        """Add a new pipe to the right of the screen"""
        gap_start = random.randint(1, self.height - self.gap_size - 1)
        self.pipes.append({
            'x': self.width - 1,
            'gap_start': gap_start,
            'gap_end': gap_start + self.gap_size
        })
    
    def update_pipes(self):
        """Move pipes to the left and remove off-screen pipes"""
        for pipe in self.pipes:
            pipe['x'] -= 1
        
        # Remove pipes that are off screen
        self.pipes = [pipe for pipe in self.pipes if pipe['x'] + self.pipe_width >= 0]
        
        # Randomly add new pipes
        if random.random() < 0.3 and (not self.pipes or self.pipes[-1]['x'] < self.width - 10):
            self.add_pipe()
    
    def update_bird(self):
        """Update bird position based on velocity"""
        self.velocity += self.gravity
        self.bird_pos += self.velocity
        
        # Keep bird within screen bounds
        if self.bird_pos < 0:
            self.bird_pos = 0
            self.velocity = 0
        elif self.bird_pos >= self.height:
            self.bird_pos = self.height - 1
            self.velocity = 0
    
    def check_collision(self):
        """Check if bird collided with pipe or ground"""
        # Check if bird hit the ground or ceiling
        if self.bird_pos <= 0 or self.bird_pos >= self.height - 1:
            self.game_over = True
            return
        
        # Check collision with pipes
        bird_col = 1  # Bird is always in column 1
        bird_row = round(self.bird_pos)
        
        for pipe in self.pipes:
            if bird_col >= pipe['x'] and bird_col < pipe['x'] + self.pipe_width:
                if not (pipe['gap_start'] <= bird_row < pipe['gap_end']):
                    self.game_over = True
                    return
        
        # Increment score if passed a pipe
        for pipe in self.pipes:
            if pipe['x'] + self.pipe_width == bird_col - 1:
                self.score += 1
    
    def jump(self):
        """Make the bird jump"""
        self.velocity = self.jump_force
    
    def render(self):
        """Render the game board"""
        # Clear the board
        self.board.iloc[:, :] = self.empty_char
        
        # Draw pipes
        for pipe in self.pipes:
            for col in range(pipe['x'], pipe['x'] + self.pipe_width):
                if 0 <= col < self.width:
                    for row in range(self.height):
                        if not (pipe['gap_start'] <= row < pipe['gap_end']):
                            self.board.iloc[row, col] = self.pipe_char
        
        # Draw bird
        bird_row = min(max(0, round(self.bird_pos)), self.height - 1)
        self.board.iloc[bird_row, 1] = self.bird_char
        
        # Clear the console and print the board
        print("\033[H\033[J")  # Clear console
        print(f"Score: {self.score}")
        print(self.board.to_string(index=False, header=False))
    
    def run(self):
        """Main game loop"""
        print("Press SPACE to jump. Press Q to quit.")
        
        # Initial pipe
        self.add_pipe()
        
        while not self.game_over:
            if keyboard.is_pressed(' '):
                self.jump()
            if keyboard.is_pressed('q'):
                break
            
            self.update_pipes()
            self.update_bird()
            self.check_collision()
            self.render()
            
            time.sleep(0.2)
        
        print(f"Game Over! Final Score: {self.score}")

if __name__ == "__main__":
    game = FlappyBird(width=30, height=15)
    game.run()      