"""Categories."""
# === Standard library imports ===
from typing import Dict, List, NamedTuple

# === Local application imports ==
import db


class Category(NamedTuple):
    """Category."""

    codename: str
    name: str
    is_base_expense: bool
    aliases: List[str]


class Categories:
    """Categories."""

    def __init__(self):
        self._categories = self._load_categories()

    def _load_categories(self) -> List[Category]:
        categories = db.fetchall_values('categories')
        categories = self._convert_categories(categories)
        return categories

    def _convert_categories(self, categories) -> List[Category]:
        converted_categories = []
        for category in categories:
            aliases = category['aliases'].split(',')
            aliases.append(category['codename'])
            aliases.append(category['name'])
            converted_categories.append(Category(
                codename=category['codename'],
                name=category['name'],
                is_base_expense=category['is_base_expense'],
                aliases=aliases,
            ))

        return converted_categories

    def get_all_categories(self) -> List[Dict]:
        """Возвращает справочник категорий."""
        return self._categories

    def get_category(self, category_name: str) -> Category:
        """Возвращает категорию по одному из её алиасов."""
        finded = None
        other_category = None
        for category in self._categories:
            if category.codename == 'other':
                other_category = category
            for alias in category.aliases:
                if category_name in alias:
                    finded = category
        if not finded:
            finded = other_category
        return finded
