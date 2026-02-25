"""
Configuration management for Evolutionary Trading Protocols.
Centralizes all system configuration with validation and environment awareness.
"""
import os
import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
from pathlib import Path

import structlog
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = structlog.get_logger()


class ExchangeType(Enum):
    """Supported cryptocurrency exchanges."""
    BINANCE = "binance"
    COINBASE = "coinbase"
    KRAKEN = "kraken"
    BYBIT = "bybit"


class Timeframe(Enum):
    """Supported timeframes for trading analysis."""
    ONE_MINUTE = "1m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    ONE_HOUR = "1h"
    FOUR_HOURS = "4h"
    ONE_DAY = "1d"


@dataclass
class TradingConfig:
    """Trading-specific configuration."""
    exchange: ExchangeType = field(
        default_factory=lambda: ExchangeType(os.getenv("DEFAULT_EXCHANGE", "binance"))
    )
    timeframe: Timeframe = field(
        default_factory=lambda: Timeframe(os.getenv("DEFAULT_TIMEFRAME", "1h"))
    )
    initial_capital: float = field(
        default_factory=lambda: float(os.getenv("INITIAL_CAPITAL", "10000"))
    )
    max_position_size: float = field(
        default_factory=lambda: float(os.getenv("MAX_POSITION_SIZE", "0.1"))
    )
    max_drawdown_pct: float = field(
        default_factory=lambda: float(os.getenv("MAX_DRAWDOWN_PCT", "20"))
    )
    stop_loss_pct: float = field(
        default_factory=lambda: float(os.getenv("STOP_LOSS_PCT", "2"))
    )
    take_profit_pct: float = field(
        default_factory=lambda: float(os.getenv("TAKE_PROFIT_PCT", "4"))
    )
    
    def validate(self) -> None:
        """Validate trading configuration values."""
        if self.initial_capital <= 0:
            raise ValueError(f"Initial capital must be positive: {self.initial_capital}")
        if not 0 < self.max_position_size <= 1:
            raise ValueError(f"Max position size must be between 0 and 1: {self.max_position_size}")
        if self.max_drawdown_pct <= 0:
            raise ValueError(f"Max drawdown must be positive: {self.max_drawdown_pct}")


@dataclass
class EvolutionaryConfig:
    """Evolutionary algorithm configuration."""
    population_size: int = field(
        default_factory=lambda: int(os.getenv("POPULATION_SIZE", "50"))
    )
    generations: int = field(
        default_factory=lambda: int(os.getenv("GENERATIONS", "100"))
    )
    mutation_rate: float = field(
        default_factory=lambda: float(os.getenv("MUTATION_RATE", "0.1"))
    )
    elitism_count: int = field(
        default_factory=lambda: int(os.getenv("ELITISM_COUNT", "5