#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
📚 اضافه کردن کتاب‌های نمونه
"""

import asyncio
from knowledge.api import knowledge_api
from knowledge.auto_learner import auto_learner

# کتاب‌های نمونه
SAMPLE_BOOKS = [
    {
        'title': 'The Kybalion',
        'author': 'Three Initiates',
        'category': 'hermetic',
        'content': '''
The Kybalion - Hermetic Philosophy

Chapter I: The Hermetic Philosophy

"The lips of wisdom are closed, except to the ears of Understanding."
The sages of ancient Egypt, the priests and priestesses of the Nile,
possessed knowledge that surpassed the wisdom of later ages.

The Seven Hermetic Principles:
1. The Principle of Mentalism
2. The Principle of Correspondence
3. The Principle of Vibration
4. The Principle of Polarity
5. The Principle of Rhythm
6. The Principle of Cause and Effect
7. The Principle of Gender

THE ALL is MIND; The Universe is Mental.
As above, so below; as below, so above.
Nothing rests; everything moves; everything vibrates.
Everything is dual; everything has poles.
Everything flows, out and in; everything has its tides.
Every cause has its effect; every effect has its cause.
Gender is in everything; everything has its masculine and feminine principles.
        '''
    },
    {
        'title': 'Numbers and Character',
        'author': 'Sepharial',
        'category': 'numerology',
        'content': '''
Numbers and Their Influence on Character

The number 1: The Individualist
Those born under the influence of number 1 are natural leaders.
They are creative, ambitious, and determined.
Their challenge is to avoid becoming too domineering.

The number 2: The Diplomat
Number 2 people are cooperative, sensitive, and intuitive.
They make excellent mediators and partners.
Their challenge is indecision and over-sensitivity.

The number 3: The Communicator
Creative, optimistic, and expressive.
Number 3 individuals are the artists and entertainers.
They must guard against scattering their energies.

The number 4: The Builder
Practical, disciplined, and reliable.
Number 4 people are the foundation of society.
Their challenge is rigidity and stubbornness.

The number 5: The Adventurer
Freedom-loving, adaptable, and progressive.
Number 5 individuals seek variety and change.
They must avoid restlessness and inconsistency.

The number 6: The Nurturer
Responsible, loving, and protective.
Number 6 people are the caregivers of the world.
Their challenge is meddling and worry.

The number 7: The Seeker
Analytical, intuitive, and wise.
Number 7 individuals are the philosophers and mystics.
They must guard against isolation and cynicism.

The number 8: The Achiever
Ambitious, efficient, and authoritative.
Number 8 people are the executives and financiers.
Their challenge is materialism and workaholism.

The number 9: The Humanitarian
Compassionate, generous, and artistic.
Number 9 individuals are here to serve humanity.
They must avoid emotional excess and resentment.
        '''
    }
]

async def add_samples():
    """اضافه کردن کتاب‌های نمونه"""
    print("📚 Adding sample books...")
    
    for book in SAMPLE_BOOKS:
        # اضافه کردن کتاب
        result = knowledge_api.add_book_manually(
            title=book['title'],
            author=book['author'],
            category=book['category'],
            content=book['content']
        )
        
        print(f"✅ Added: {book['title']}")
        
        # پردازش کتاب
        process_result = knowledge_api.process_book(result['book_id'])
        if process_result['success']:
            print(f"   ✅ Processed")
        
        # یادگیری کتاب
        learn_result = await knowledge_api.learn_book(result['book_id'])
        if learn_result['success']:
            print(f"   ✅ Learned")
    
    print("\n🎉 All sample books added and learned!")

if __name__ == "__main__":
    asyncio.run(add_samples())
