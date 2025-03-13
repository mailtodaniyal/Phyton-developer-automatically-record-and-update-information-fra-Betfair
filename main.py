import os
import datetime
import asyncio
from flask import Flask, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import betfairlightweight

DATABASE_URL = "postgresql://username:password@localhost:5432/betting_db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Bet(Base):
    __tablename__ = "bets"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, index=True)
    market_id = Column(String, index=True)
    selection_id = Column(String, index=True)
    odds = Column(Float)
    stake = Column(Float)
    profit_loss = Column(Float, default=0.0)
    status = Column(String) 
    placed_at = Column(DateTime, default=datetime.datetime.utcnow)
    settled_at = Column(DateTime, nullable=True)

Base.metadata.create_all(engine)

USERNAME = "your_betfair_username"
PASSWORD = "your_betfair_password"
APP_KEY = "your_app_key"

trading = betfairlightweight.APIClient(USERNAME, PASSWORD, APP_KEY)
trading.login()

def fetch_active_bets():
    session = SessionLocal()
    market_filter = {"eventTypeIds": ["1"]}  
    market_catalogue = trading.betting.list_market_catalogue(
        filter=market_filter, 
        max_results="10"
    )
    
    for market in market_catalogue:
        market_id = market.market_id
        runners = market.runners
        
        for runner in runners:
            bet = Bet(
                event_id=market.event.id,
                market_id=market_id,
                selection_id=runner.selection_id,
                odds=runner.last_price_traded or 0.0,
                stake=10.0,  
                status="Open"
            )
            session.add(bet)
    
    session.commit()
    session.close()

async def update_bets():
    while True:
        session = SessionLocal()
        active_bets = session.query(Bet).filter(Bet.status == "Open").all()
        
        for bet in active_bets:
            market_book = trading.betting.list_market_book(
                market_ids=[bet.market_id]
            )
            if market_book:
                runner_data = next(
                    (runner for runner in market_book[0].runners if runner.selection_id == bet.selection_id), None
                )
                if runner_data:
                    new_odds = runner_data.last_price_traded or bet.odds
                    profit_loss = (new_odds - bet.odds) * bet.stake if new_odds else 0.0
                    
                    bet.odds = new_odds
                    bet.profit_loss = profit_loss
                    if market_book[0].status == "CLOSED":
                        bet.status = "Settled"
                        bet.settled_at = datetime.datetime.utcnow()
        
        session.commit()
        session.close()
        await asyncio.sleep(10)  

app = Flask(__name__)

@app.route('/bets', methods=['GET'])
def get_bets():
    session = SessionLocal()
    bets = session.query(Bet).all()
    session.close()
    
    return jsonify([
        {
            "id": bet.id,
            "event_id": bet.event_id,
            "market_id": bet.market_id,
            "selection_id": bet.selection_id,
            "odds": bet.odds,
            "stake": bet.stake,
            "profit_loss": bet.profit_loss,
            "status": bet.status
        } for bet in bets
    ])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(update_bets()) 
    app.run(debug=True, port=5000)
