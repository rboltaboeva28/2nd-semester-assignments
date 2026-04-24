class RecipeError(Exception):
    pass

class RecipeNotFound(RecipeError):
    def __init__(self, recipe_name):
        self.recipe_name = recipe_name
        super().__init__(f"recipe not found: {recipe_name}")

class DuplicateRecipeError(RecipeError):
    def __init__(self, recipe_name):
        self.recipe_name = recipe_name
        super().__init__(f"recipe already exists: {recipe_name}")

class InvalidServingError(RecipeError):
    def __init__(self, servings):
        self.servings = servings
        super().__init__(f"invalid servings: {servings}. must be positive")

class MissingIngredientsError(RecipeError):
    def __init__(self, recipe_name, missing):
        self.recipe_name = recipe_name
        self.missing = missing
        super().__init__(f"cannot make {recipe_name}: missing {missing}")

class RecipeBook:
    def __init__(self):
        self.recipes = {}

    def add_recipe(self, name, servings, ingredients):
        if name in self.recipes:
            raise DuplicateRecipeError(name)
        if servings <= 0:
            raise InvalidServingError(servings)
        else:
            self.recipes[name] = {"servings": servings, "ingredients": ingredients}

    def scale_recipe(self, name, desired_servings):
        try:
            recipe = self.recipes[name]
        except KeyError:
            raise RecipeNotFound(name) from None
        if desired_servings <= 0:
            raise InvalidServingError(desired_servings)
        else:
            new_recipe = {}
            base_servings = recipe["servings"]
            for ingredient, amount in recipe["ingredients"].items():
                new_recipe[ingredient] = round(amount * (desired_servings / base_servings), 2)
            return new_recipe
        
    def check_pantry(self, name, pantry):
        try:
            recipe = self.recipes[name]
        except KeyError:
            raise RecipeNotFound(name) from None
        
        missing = {}
        ingredients = recipe["ingredients"]
        for ingredient, amount in ingredients.items():
            if ingredient not in pantry:
                missing[ingredient] = round(amount, 2)
            elif pantry[ingredient] < amount:
                lacking = amount - pantry[ingredient]
                missing[ingredient] = round(lacking, 2)
        if missing:
            raise MissingIngredientsError(name, missing)
        return True
    
book = RecipeBook()

book.add_recipe("Pancakes", 4, {"flour": 2.0, "eggs": 3.0, "milk": 1.5, "sugar": 0.5})
book.add_recipe("Omelette", 2, {"eggs": 4.0, "cheese": 1.0, "pepper": 0.25})

scaled = book.scale_recipe("Pancakes", 8)
print(f"pancakes for 8: {scaled}")

scaled = book.scale_recipe("Omelette", 1)
print(f"omelette for 1: {scaled}")

pantry = {"flour": 2.0, "eggs": 1.0, "milk": 1.5, "sugar": 0.5}
try:
    book.check_pantry("Pancakes", pantry)
except RecipeError as e:
    print(e)

pantry2 = {"eggs": 5.0, "cheese": 2.0, "pepper": 1.0}
result = book.check_pantry("Omelette", pantry2)
print(f"can make omelette: {result}")

tests = [
    lambda: book.add_recipe("Pancakes", 4, {"flour": 1.0}),
    lambda: book.scale_recipe("Salad", 2),
    lambda: book.scale_recipe("Pancakes", -1),
]

for test in tests:
    try:
        test()
    except RecipeError as e:
        print(e)