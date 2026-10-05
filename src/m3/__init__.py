"""
Member 3 - Shelter & Resource Management

Core data structures:
- Custom HashMap
- Binary Search Tree
- Custom Priority Queue
- Sorting
- Dynamic occupancy management
"""

from .shelter import Shelter
from .hash_map import ShelterHashMap
from .bst import ShelterBST
from .priority_queue import ShelterPriorityQueue
from .shelter_manager import ShelterManager

__all__ = [
    "Shelter",
    "ShelterHashMap",
    "ShelterBST",
    "ShelterPriorityQueue",
    "ShelterManager",
]