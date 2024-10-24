import pygame
import random
from pygame.locals import *
import pygame_gui
import pygame_menu
import numpy as np

class Particle:
    def __init__(self, x, y, color, velocity=(0, 0), size=2, lifetime=30):
        self.x = x
        self.y = y
        self.color = color
        self.vx, self.vy = velocity
        self.size = size
        self.lifetime = lifetime
        self.age = 0
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.age += 1
        return self.age < self.lifetime
        
    def draw(self, screen):
        alpha = 255 * (1 - self.age / self.lifetime)
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, alpha), (self.size, self.size), self.size)
        screen.blit(surf, (int(self.x - self.size), int(self.y - self.size)))

class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def add_particle(self, particle):
        self.particles.append(particle)
    
    def update(self):
        self.particles = [p for p in self.particles if p.update()]
    
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

class Minesweeper:
    def __init__(self):
        pygame.init()
        # 将基础单元格大小从30增加到45
        self.CELL_SIZE = 45  # 修改这里
        
        # 定义状态栏高度
        self.STATUS_BAR_HEIGHT = 60  # 添加这行
        
        # Game difficulty settings (保持格子数量不变，只是显示更大)
        self.EASY = {"size": (9, 9), "mines": 10, "name": "Easy"}
        self.MEDIUM = {"size": (16, 16), "mines": 40, "name": "Medium"}
        self.HARD = {"size": (30, 16), "mines": 99, "name": "Hard"}
        
        # Initialize clock
        self.clock = pygame.time.Clock()
        
        # Modern color scheme
        self.COLORS = {
            'bg': (240, 240, 245),           # Light blue-gray background
            'cell': {
                'normal': (255, 255, 255),    # White cells
                'hover': (230, 235, 240),     # Light blue hover
                'revealed': (245, 245, 250),  # Slightly darker than bg
                'border': (200, 205, 210)     # Soft gray border
            },
            'numbers': [
                (66, 133, 244),    # 1: Google Blue
                (52, 168, 83),     # 2: Google Green
                (234, 67, 53),     # 3: Google Red
                (121, 80, 242),    # 4: Royal Purple
                (255, 143, 0),     # 5: Orange
                (0, 151, 167),     # 6: Teal
                (66, 66, 66),      # 7: Dark Gray
                (158, 158, 158)    # 8: Gray
            ],
            'status_bar': {
                'bg': (255, 255, 255),        # White background
                'text': (75, 85, 99),         # Dark gray text
                'border': (226, 232, 240)     # Light gray border
            },
            'menu': {
                'bg': (255, 255, 255),        # White background
                'button': {
                    'normal': (66, 133, 244),  # Google Blue
                    'hover': (25, 103, 210),   # Darker Blue
                    'text': (255, 255, 255)    # White text
                },
                'title': (31, 41, 55),        # Dark text
                'subtitle': (107, 114, 128)    # Gray text
            }
        }
        
        # Initialize game settings
        self.settings = {
            'sound_enabled': True,
            'animations_enabled': True,
            'dark_mode': False,
            'cell_size': 30
        }
        
        # Initialize game
        self.current_difficulty = self.EASY
        self.CELL_SIZE = 45  # 确保这里也是45
        self.font = pygame.font.Font(None, 54)  # 从36增加到54
        self.timer_font = pygame.font.Font(None, 48)  # 从32增加到48
        self.initialize_game()

    def initialize_game(self):
        """Initialize or reset the game state"""
        width = self.current_difficulty["size"][0] * self.CELL_SIZE
        height = self.current_difficulty["size"][1] * self.CELL_SIZE + self.STATUS_BAR_HEIGHT
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Minesweeper - All For Diarina")
        
        rows, cols = self.current_difficulty["size"]
        self.board = np.zeros((rows, cols), dtype=int)
        self.revealed = np.zeros((rows, cols), dtype=bool)
        self.flagged = np.zeros((rows, cols), dtype=bool)
        
        self.game_over = False
        self.first_click = True
        self.start_time = None
        self.mines_left = self.current_difficulty["mines"]
        
        # Setup GUI and particle system
        self.setup_gui()
        self.particle_system = ParticleSystem()  # Use our custom ParticleSystem class

    def place_mines(self, first_x, first_y):
        """在游戏板上放置地雷，确保第一次点击的位置及其周围没有地雷"""
        rows, cols = self.current_difficulty["size"]
        mines_count = self.current_difficulty["mines"]
        
        # 创建所有可能的位置列表（排除第一次点击的位置及其周围）
        safe_zone = [(x, y) for x in range(max(0, first_x-1), min(rows, first_x+2))
                     for y in range(max(0, first_y-1), min(cols, first_y+2))]
        all_positions = [(x, y) for x in range(rows) for y in range(cols)
                        if (x, y) not in safe_zone]
        
        # 随选择位置放置地雷
        mine_positions = random.sample(all_positions, mines_count)
        
        # 在选定位置放置地雷（-1表示地雷）
        for x, y in mine_positions:
            self.board[x][y] = -1
            
            # 更新周围格子的数字
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    new_x, new_y = x + dx, y + dy
                    if (0 <= new_x < rows and 0 <= new_y < cols and 
                        self.board[new_x][new_y] != -1):
                        self.board[new_x][new_y] += 1

    def get_neighbors(self, x, y):
        """获取指定位置周围的所有有效相邻格子"""
        rows, cols = self.current_difficulty["size"]
        neighbors = []
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < rows and 0 <= new_y < cols:
                    neighbors.append((new_x, new_y))
        
        return neighbors

    def handle_click(self, x, y, button):
        """Handle mouse click events"""
        # Convert mouse coordinates to grid coordinates
        grid_x = x // self.CELL_SIZE
        grid_y = (y - self.STATUS_BAR_HEIGHT) // self.CELL_SIZE  # 修改这里
        
        # Check if coordinates are valid
        rows, cols = self.current_difficulty["size"]
        if not (0 <= grid_x < rows and 0 <= grid_y < cols):
            return
        
        # If game is over, don't process clicks
        if self.game_over:
            return
        
        # Left click
        if button == 1:
            if self.flagged[grid_x][grid_y]:
                return
            
            # First click
            if self.first_click:
                self.first_click = False
                self.start_time = pygame.time.get_ticks()
                self.place_mines(grid_x, grid_y)
            
            self.reveal_cell(grid_x, grid_y)
        
        # Right click
        elif button == 3:
            if not self.revealed[grid_x][grid_y]:
                # Update mines_left counter
                if not self.flagged[grid_x][grid_y]:
                    self.mines_left -= 1
                else:
                    self.mines_left += 1
                self.flagged[grid_x][grid_y] = not self.flagged[grid_x][grid_y]

    def reveal_cell(self, x, y):
        """揭示指定位置的格子"""
        # 如果格子已经被揭示或已标记，返回
        if self.revealed[x][y] or self.flagged[x][y]:
            return
        
        self.revealed[x][y] = True
        
        # 如果点到地雷游戏结束
        if self.board[x][y] == -1:
            self.game_over = True
            self.reveal_all_mines()
            return
        
        # 如果是空格子（周围没有地雷），递归揭示周围的格子
        if self.board[x][y] == 0:
            for nx, ny in self.get_neighbors(x, y):
                self.reveal_cell(nx, ny)

    def reveal_all_mines(self):
        """游戏结束时显示所有地雷"""
        rows, cols = self.current_difficulty["size"]
        for x in range(rows):
            for y in range(cols):
                if self.board[x][y] == -1:
                    self.revealed[x][y] = True

    def check_win(self):
        """检查是否获胜"""
        rows, cols = self.current_difficulty["size"]
        for x in range(rows):
            for y in range(cols):
                # 如果有非雷格子未被揭示，游戏未胜利
                if self.board[x][y] != -1 and not self.revealed[x][y]:
                    return False
        return True

    def draw(self):
        """绘制游戏界面"""
        self.screen.fill(self.COLORS['bg'])
        
        # 绘制状态栏
        self.draw_status_bar()
        
        # 绘制
        rows, cols = self.current_difficulty["size"]
        for x in range(rows):
            for y in range(cols):
                rect = pygame.Rect(
                    x * self.CELL_SIZE,
                    y * self.CELL_SIZE + 40,  # 40像素用于状态栏
                    self.CELL_SIZE,
                    self.CELL_SIZE
                )
                
                # 绘制未揭示的格子
                if not self.revealed[x][y]:
                    pygame.draw.rect(self.screen, self.COLORS['cell']['normal'], rect)
                    pygame.draw.rect(self.screen, self.COLORS['cell']['border'], rect, 1)
                    
                    # 绘制旗子
                    if self.flagged[x][y]:
                        # 这里可以添加旗子的图形，暂时用红色方块代替
                        small_rect = pygame.Rect(
                            x * self.CELL_SIZE + 8,
                            y * self.CELL_SIZE + 48,
                            self.CELL_SIZE - 16,
                            self.CELL_SIZE - 16
                        )
                        pygame.draw.rect(self.screen, (255, 0, 0), small_rect)
                
                # 绘制已揭示格子
                else:
                    pygame.draw.rect(self.screen, self.COLORS['cell']['revealed'], rect)
                    pygame.draw.rect(self.screen, self.COLORS['cell']['border'], rect, 1)
                    
                    # 绘制数字或地雷
                    if self.board[x][y] == -1:
                        # 绘制地雷（暂时用黑色圆形代替）
                        center = (x * self.CELL_SIZE + self.CELL_SIZE // 2,
                                y * self.CELL_SIZE + 40 + self.CELL_SIZE // 2)
                        pygame.draw.circle(self.screen, (0, 0, 0), center, 10)
                    elif self.board[x][y] > 0:
                        # 绘制数字
                        text = self.font.render(str(self.board[x][y]), True, self.COLORS['numbers'][min(self.board[x][y]-1, 2)])
                        text_rect = text.get_rect(center=(
                            x * self.CELL_SIZE + self.CELL_SIZE // 2,
                            y * self.CELL_SIZE + 40 + self.CELL_SIZE // 2
                        ))
                        self.screen.blit(text, text_rect)
        
        pygame.display.flip()

    def draw_status_bar(self):
        """Draw status bar with modern design"""
        # Draw status bar background with subtle gradient
        status_rect = pygame.Rect(0, 0, self.screen.get_width(), self.STATUS_BAR_HEIGHT)
        pygame.draw.rect(self.screen, self.COLORS['status_bar']['bg'], status_rect)
        pygame.draw.line(self.screen, self.COLORS['status_bar']['border'],
                        (0, self.STATUS_BAR_HEIGHT), 
                        (self.screen.get_width(), self.STATUS_BAR_HEIGHT))
        
        # Draw mine counter with icon
        mines_text = f"💣 {self.mines_left}"
        mines_surface = self.timer_font.render(mines_text, True, self.COLORS['status_bar']['text'])
        mines_rect = mines_surface.get_rect(left=30, centery=self.STATUS_BAR_HEIGHT//2)
        self.screen.blit(mines_surface, mines_rect)
        
        # Draw "All For Diarina" in center
        dedication = self.timer_font.render("All For Diarina", True, self.COLORS['status_bar']['text'])
        dedication_rect = dedication.get_rect(center=(self.screen.get_width() // 2, self.STATUS_BAR_HEIGHT//2))
        self.screen.blit(dedication, dedication_rect)
        
        # Draw timer with icon
        if self.start_time is not None and not self.game_over:
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            time_text = f"⏱ {elapsed_time:03d}"
        else:
            time_text = "⏱ 000"
        
        time_surface = self.timer_font.render(time_text, True, self.COLORS['status_bar']['text'])
        time_rect = time_surface.get_rect(right=self.screen.get_width() - 30, 
                                        centery=self.STATUS_BAR_HEIGHT//2)
        self.screen.blit(time_surface, time_rect)

    def run(self):
        """Game main loop"""
        running = True
        while running:
            time_delta = self.clock.tick(60)/1000.0
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mouse_y -= 40  # Adjust for status bar
                    self.handle_click(mouse_x, mouse_y, event.button)
                    
                    if self.check_win():
                        self.game_over = True
                        if self.show_game_over_screen(won=True):
                            # Restart game
                            if self.show_difficulty_menu():
                                self.initialize_game()
                                continue
                            else:
                                running = False
                elif self.game_over:
                    if self.show_game_over_screen(won=False):
                        # Restart game
                        if self.show_difficulty_menu():
                            self.initialize_game()
                            continue
                        else:
                            running = False
            
                self.gui_manager.process_events(event)
            
            self.gui_manager.update(time_delta)
            self.particle_system.update()  # Update particles
            
            self.draw()
            self.particle_system.draw(self.screen)  # Draw particles
            self.gui_manager.draw_ui(self.screen)
            
            pygame.display.flip()
        
        pygame.quit()

    def show_difficulty_menu(self):
        """显示难度选择菜单"""
        menu_screen = pygame.display.set_mode((800, 600))  # 改为更大的尺寸，比如 (800, 600)
        pygame.display.set_caption("Minesweeper - All For Diarina")
        menu = DifficultyMenu(menu_screen)
        
        while True:
            menu.draw()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return False
                elif event.type == MOUSEBUTTONDOWN:
                    choice = menu.handle_click(event.pos)
                    if choice is not None:
                        if choice == 0:
                            self.current_difficulty = self.EASY
                        elif choice == 1:
                            self.current_difficulty = self.MEDIUM
                        else:
                            self.current_difficulty = self.HARD
                        self.initialize_game()
                        return True

    def show_game_over_screen(self, won=False):
        """Show game over screen with animation"""
        overlay = pygame.Surface(self.screen.get_size())
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Show message
        message = "VICTORY!" if won else "GAME OVER"
        color = (50, 205, 50) if won else (220, 20, 60)
        
        # Create message surface with shadow
        font = pygame.font.Font(None, 72)
        shadow = font.render(message, True, (0, 0, 0))
        text = font.render(message, True, color)
        
        # Position text in center
        text_rect = text.get_rect(center=(self.screen.get_width() // 2,
                                         self.screen.get_height() // 2 - 40))
        shadow_rect = shadow.get_rect(center=(text_rect.centerx + 2,
                                            text_rect.centery + 2))
        
        # Draw text with shadow
        self.screen.blit(shadow, shadow_rect)
        self.screen.blit(text, text_rect)
        
        # Draw restart button
        button_width = 200
        button_height = 50
        button_rect = pygame.Rect(
            (self.screen.get_width() - button_width) // 2,
            text_rect.bottom + 20,
            button_width,
            button_height
        )
        
        # Draw button with hover effect
        mouse_pos = pygame.mouse.get_pos()
        button_color = self.COLORS['menu']['button']['hover'] if button_rect.collidepoint(mouse_pos) \
                      else self.COLORS['menu']['button']['normal']
        
        pygame.draw.rect(self.screen, button_color, button_rect, border_radius=5)
        
        # Draw button text
        button_font = pygame.font.Font(None, 36)
        button_text = button_font.render("Back to Menu", True, self.COLORS['menu']['button']['text'])
        button_text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, button_text_rect)
        
        # Draw "All For Diarina"
        dedication_font = pygame.font.Font(None, 24)
        dedication_text = dedication_font.render("All For Diarina", True, (200, 200, 200))
        dedication_rect = dedication_text.get_rect(centerx=self.screen.get_width() // 2,
                                                 bottom=self.screen.get_height() - 10)
        self.screen.blit(dedication_text, dedication_rect)
        
        pygame.display.flip()
        
        # Handle button click
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return False
                elif event.type == MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        return True
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        return True
        return False

    def draw_cell(self, x, y, rect):
        """Draw a single cell with modern styling"""
        mouse_pos = pygame.mouse.get_pos()
        cell_hovered = rect.collidepoint(mouse_pos) and not self.revealed[x][y]
        
        if not self.revealed[x][y]:
            # Draw unrevealed cell
            color = self.COLORS['cell']['hover'] if cell_hovered else self.COLORS['cell']['normal']
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, self.COLORS['cell']['border'], rect, 1)
            
            # Draw flag if flagged
            if self.flagged[x][y]:
                flag_text = self.font.render("🚩", True, (255, 0, 0))
                flag_rect = flag_text.get_rect(center=rect.center)
                self.screen.blit(flag_text, flag_rect)
        
        else:
            # Draw revealed cell
            pygame.draw.rect(self.screen, self.COLORS['cell']['revealed'], rect)
            pygame.draw.rect(self.screen, self.COLORS['cell']['border'], rect, 1)
            
            # Draw content (number or mine)
            if self.board[x][y] == -1:
                mine_text = self.font.render("💣", True, (0, 0, 0))
                mine_rect = mine_text.get_rect(center=rect.center)
                self.screen.blit(mine_text, mine_rect)
            elif self.board[x][y] > 0:
                number_color = self.COLORS['numbers'][self.board[x][y] - 1]
                text = self.font.render(str(self.board[x][y]), True, number_color)
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)

    def setup_gui(self):
        """Setup pygame-gui elements"""
        self.gui_manager = pygame_gui.UIManager((self.screen.get_width(), self.screen.get_height()))
        
        # 移除按钮相关代码，只保留GUI管理器的初始化
        # 不再创建 restart_button 和 settings_button

    def setup_particle_system(self):
        """Setup particle system for effects"""
        self.particle_system = ParticleSystem()
        
    def create_reveal_effect(self, x, y):
        """Create particle effect when revealing a cell"""
        center_x = x * self.CELL_SIZE + self.CELL_SIZE // 2
        center_y = y * self.CELL_SIZE + 40 + self.CELL_SIZE // 2
        
        for _ in range(10):
            velocity = (random.uniform(-2, 2), random.uniform(-2, 2))
            color = self.COLORS['cell']['normal']
            particle = Particle(
                center_x, 
                center_y,
                color,
                velocity=velocity,
                size=3,
                lifetime=20
            )
            self.particle_system.add_particle(particle)

    def create_settings_menu(self):
        """Create settings menu using pygame-menu"""
        menu = pygame_menu.Menu(
            'Settings',
            self.screen.get_width() // 2,
            self.screen.get_height() // 2,
            theme=pygame_menu.themes.THEME_BLUE
        )
        
        menu.add.toggle_switch('Sound Effects', self.settings['sound_enabled'])
        menu.add.toggle_switch('Animations', self.settings['animations_enabled'])
        menu.add.toggle_switch('Dark Mode', self.settings['dark_mode'])
        menu.add.range_slider('Cell Size', default=30, range_values=(20, 40))
        menu.add.button('Back', pygame_menu.events.BACK)
        
        return menu

class DifficultyMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 54)
        self.title_font = pygame.font.Font(None, 80)
        self.small_font = pygame.font.Font(None, 42)
        
        # 调整按钮位置以适应新的窗口大小
        button_width = 300
        button_height = 70
        start_y = 250  # 调整起始位置
        spacing = 30
        
        self.buttons = [
            {
                "text": "Easy",
                "rect": pygame.Rect((800 - button_width) // 2, start_y, 
                                  button_width, button_height)
            },
            {
                "text": "Medium",
                "rect": pygame.Rect((800 - button_width) // 2, 
                                  start_y + button_height + spacing, 
                                  button_width, button_height)
            },
            {
                "text": "Hard",
                "rect": pygame.Rect((800 - button_width) // 2, 
                                  start_y + 2 * (button_height + spacing), 
                                  button_width, button_height)
            }
        ]
        
        self.COLORS = {
            'bg': (240, 240, 245),
            'button': {
                'normal': (66, 133, 244),
                'hover': (25, 103, 210),
                'text': (255, 255, 255)
            },
            'title': (31, 41, 55),
            'subtitle': (107, 114, 128)
        }
    
    def draw(self):
        self.screen.fill(self.COLORS['bg'])
        
        # 调整标题位置
        title = self.title_font.render("MINESWEEPER", True, self.COLORS['title'])
        title_shadow = self.title_font.render("MINESWEEPER", True, (220, 220, 220))
        title_rect = title.get_rect(center=(400, 150))  # 调整到新窗口中心
        shadow_rect = title_rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        self.screen.blit(title_shadow, shadow_rect)
        self.screen.blit(title, title_rect)
        
        # 调整副标题位置
        dedication = self.small_font.render("All For Diarina", True, self.COLORS['subtitle'])
        dedication_rect = dedication.get_rect(center=(400, 200))  # 调整到新窗口中心
        self.screen.blit(dedication, dedication_rect)
        
        # Draw buttons
        for button in self.buttons:
            self.draw_button(button)
        
        pygame.display.flip()
    
    def draw_button(self, button):
        rect = button["rect"]
        is_hovered = self.is_hovered(rect)
        
        # Draw button shadow
        shadow_rect = rect.copy()
        shadow_rect.y += 3
        pygame.draw.rect(self.screen, (0, 0, 0, 30), shadow_rect, border_radius=8)
        
        # Draw button with hover effect
        color = self.COLORS['button']['hover'] if is_hovered else self.COLORS['button']['normal']
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        
        # Draw button text
        text = self.font.render(button["text"], True, self.COLORS['button']['text'])
        text_rect = text.get_rect(center=rect.center)
        self.screen.blit(text, text_rect)
    
    def is_hovered(self, rect):
        return rect.collidepoint(pygame.mouse.get_pos())
    
    def handle_click(self, pos):
        for i, button in enumerate(self.buttons):
            if button["rect"].collidepoint(pos):
                return i
        return None

if __name__ == "__main__":
    game = Minesweeper()
    if game.show_difficulty_menu():
        game.run()

