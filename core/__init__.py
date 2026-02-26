"""
هسته اصلی ربات - Eye of Horus
نسخه ∞ - جاودانه
ساخته شده توسط: Al Hashash (ال حشاش)
"""

from .safe_imports import SafeImporter, importer
from .error_handler import ErrorHandler, error_handler, safe_execute, safe_async_execute
from .self_healer import SelfHealer, self_healer
from .evolution_engine import EvolutionEngine, evolution_engine
from .quantum_memory import QuantumMemory, quantum_memory
from .cosmic_intelligence import CosmicIntelligence, cosmic_ai
from .eternal_backup import EternalBackup, eternal_backup
from .self_recovery import SelfRecovery, self_recovery

__version__ = "∞"
__codename__ = "Eye of Horus"
__creator__ = "Al Hashash"
__symbol__ = "𓂀"

__all__ = [
    'SafeImporter', 'importer',
    'ErrorHandler', 'error_handler', 'safe_execute', 'safe_async_execute',
    'SelfHealer', 'self_healer',
    'EvolutionEngine', 'evolution_engine',
    'QuantumMemory', 'quantum_memory',
    'CosmicIntelligence', 'cosmic_ai',
    'EternalBackup', 'eternal_backup',
    'SelfRecovery', 'self_recovery',
    '__version__', '__codename__', '__creator__', '__symbol__'
]
