from typing import List
from datetime import datetime

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# App
app = FastAPI(
    title='MockAPI',
    servers=[
        {'url': 'http://127.0.0.1:8000', 'description': 'Mock Server'},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schemas
class User(BaseModel):
    name: str
    email: str


class Message(BaseModel):
    text: str


class Currency(BaseModel):
    code: str
    name: str


class Portfolio(BaseModel):
    id: int
    code: str
    currency: str


class Instrument(BaseModel):
    name: str


class Holding(BaseModel):
    id: int
    portfolio: Portfolio
    date: datetime
    instrument: Instrument
    weight: float
    performance: float


class Performance(BaseModel):
    holding_id: int
    contribution: float


# Fake data
currencies = [
    Currency(code='EUR', name='EURO'),
    Currency(code='USD', name='US Dollar'),
    Currency(code='ZAR', name='South African Rand'),
]

portfolios = [
    Portfolio(id=1, code='Equity Portfolio', currency='EUR'),
    Portfolio(id=2, code='Fixed Income Portfolio', currency='USD'),
    Portfolio(id=3, code='Balanced Portfolio', currency='ZAR'),
]

instruments = [
    Instrument(name='Google'),
    Instrument(name='Apple'),
    Instrument(name='Microsoft'),
    Instrument(name='Tesla'),
]

holdings = [
    Holding(id=1, portfolio=portfolios[0],date=datetime(2023,1,31), instrument=instruments[0], weight=25.0, performance=5.0),
    Holding(id=2, portfolio=portfolios[0],date=datetime(2023,1,31), instrument=instruments[1], weight=10.0, performance=-3.2),
    Holding(id=3, portfolio=portfolios[0],date=datetime(2023,1,31), instrument=instruments[2], weight=35.0, performance=2.5),
    Holding(id=4, portfolio=portfolios[0],date=datetime(2023,1,31), instrument=instruments[3], weight=30.0, performance=2.5),

    Holding(id=5, portfolio=portfolios[1],date=datetime(2023,1,31), instrument=instruments[0], weight=25.0, performance=3.0),
    Holding(id=6, portfolio=portfolios[1],date=datetime(2023,1,31), instrument=instruments[1], weight=10.0, performance=-1.2),
    Holding(id=7, portfolio=portfolios[1],date=datetime(2023,1,31), instrument=instruments[2], weight=35.0, performance=1.5),
    Holding(id=8, portfolio=portfolios[1],date=datetime(2023,1,31), instrument=instruments[3], weight=30.0, performance=1.5),

    Holding(id=9, portfolio=portfolios[2],date=datetime(2023,1,31), instrument=instruments[0], weight=25.0, performance=-3.0),
    Holding(id=10, portfolio=portfolios[2],date=datetime(2023,1,31), instrument=instruments[1], weight=10.0, performance=-4.2),
    Holding(id=11, portfolio=portfolios[2],date=datetime(2023,1,31), instrument=instruments[2], weight=35.0, performance=1.5),
    Holding(id=12, portfolio=portfolios[2],date=datetime(2023,1,31), instrument=instruments[3], weight=30.0, performance=1.5),
]


# Routes
@app.get('/', status_code=status.HTTP_200_OK)
async def get_user() -> User:
    return User(name='John Doe', email='john.doe@company.com')


@app.get('/portfolios', status_code=status.HTTP_200_OK)
async def get_portfolios(currency_code: str) -> List[Portfolio]:
    return [portfolio for portfolio in portfolios if portfolio.currency == currency_code]


@app.get('/holdings', status_code=status.HTTP_200_OK)
async def get_holdings(portfolio_id: int) -> List[Holding]:
    return [holding for holding in holdings if holding.portfolio.id == portfolio_id]


@app.get('/performance', status_code=status.HTTP_200_OK)
async def get_performance(holding_id: int) -> float:
    holding = next(holding for holding in holdings if holding.id == holding_id)
    return holding.weight * holding.performance * 0.01


