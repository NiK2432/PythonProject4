from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI()



class GameCreate(BaseModel):
    title: str
    genre: str
    players: int

class Game(BaseModel):
    id: int
    title: str
    genre: str
    players: int


games = [
    {"id": 1, "title": "Catan", "genre": "Strategy", "players": 4},
    {"id": 2, "title": "Dungeons & Dragons", "genre": "RPG", "players": 6},
]


@app.get("/games", response_model=List[Game])
def get_games():
    return games

@app.post("/games", response_model=Game, status_code=status.HTTP_201_CREATED)
def create_game(game_in: GameCreate):
    new_id = games[-1]["id"] + 1 if games else 1

    new_game = {"id": new_id, **game_in.model_dump()}

    games.append(new_game)
    return new_game

@app.put("/games/{game_id}", response_model=Game)
def update_game(game_id: int, game_in: GameCreate):
    for index, existing_game in enumerate(games):
        if existing_game["id"] == game_id:
            updated_game = {"id": game_id, **game_in.model_dump()}
            games[index] = updated_game
            return updated_game

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Игра с id {game_id} не найдена, сорян"
    )

@app.delete("/games/{game_id}", response_model=Game)
def delete_game(game_id: int):
    for index, existing_game in enumerate(games):
        if existing_game["id"] == game_id:

            deleted_game = games.pop(index)
            return deleted_game

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Нельзя удалить то, чего нет. ID {game_id} отсутствует"