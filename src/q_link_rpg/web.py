from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Tuple

from q_link_rpg.engine.grid_world import GridWorld
from q_link_rpg.engine.game_logic import GameLogic, Action

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="src/q_link_rpg/static"), name="static")

templates = Jinja2Templates(directory="src/q_link_rpg/templates")

# Initialize Game
DEFAULT_WIDTH = 10
DEFAULT_HEIGHT = 10
START_POS = (0, 0)
GOAL_POS = (9, 9)
WALLS = [(1, 1), (1, 2), (2, 2), (5, 5), (6, 5), (7, 5), (3, 7), (4, 7), (5, 7)]
ENEMIES = [(3, 3), (4, 4), (6, 2), (8, 7)]

grid = GridWorld(DEFAULT_WIDTH, DEFAULT_HEIGHT, START_POS, GOAL_POS)
grid.add_walls(WALLS)
grid.add_enemies(ENEMIES)
game = GameLogic(grid)

class GameState(BaseModel):
    width: int
    height: int
    hero_pos: Tuple[int, int]
    goal_pos: Tuple[int, int]
    walls: List[Tuple[int, int]]
    enemies: List[Tuple[int, int]]
    score: int = 0
    game_over: bool = False

current_score = 0
game_over = False

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/api/state", response_model=GameState)
async def get_state():
    return GameState(
        width=grid.width,
        height=grid.height,
        hero_pos=grid.hero_pos,
        goal_pos=grid.goal_pos,
        walls=list(grid.walls),
        enemies=list(grid.enemies),
        score=current_score,
        game_over=game_over
    )

@app.post("/api/action/{action_id}")
async def take_action(action_id: int):
    global current_score, game_over
    if game_over:
        return await get_state()
    
    try:
        action = Action(action_id)
        reward, done = game.step(action)
        current_score += reward
        game_over = done
    except ValueError:
        pass # Invalid action
        
    return await get_state()

@app.post("/api/reset")
async def reset_game():
    global current_score, game_over, grid, game
    
    # Re-init grid to reset enemies
    grid = GridWorld(DEFAULT_WIDTH, DEFAULT_HEIGHT, START_POS, GOAL_POS)
    grid.add_walls(WALLS)
    grid.add_enemies(ENEMIES)
    game = GameLogic(grid)
    
    current_score = 0
    game_over = False
    return await get_state()
