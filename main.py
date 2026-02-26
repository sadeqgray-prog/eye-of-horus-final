#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('main')

def main():
    logger.info("="*50)
    logger.info("🚀 Starting Eye of Horus")
    logger.info("="*50)
    
    try:
        from bot.ultimate_bot import UltimateBot
        bot = UltimateBot()
        bot.run()
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
