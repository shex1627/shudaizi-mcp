I'm building a recipe and meal planning app and want to add AI assistant
capabilities via MCP. The app has a SQLite database with this schema:

```sql
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    cuisine TEXT,
    prep_time_min INTEGER,
    cook_time_min INTEGER,
    servings INTEGER,
    difficulty TEXT CHECK(difficulty IN ('easy', 'medium', 'hard')),
    instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id),
    name TEXT NOT NULL,
    quantity REAL,
    unit TEXT,
    is_optional BOOLEAN DEFAULT FALSE
);

CREATE TABLE meal_plans (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,
    date DATE NOT NULL,
    meal_type TEXT CHECK(meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
    recipe_id INTEGER REFERENCES recipes(id),
    servings_override INTEGER
);

CREATE TABLE pantry (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,
    ingredient_name TEXT NOT NULL,
    quantity REAL,
    unit TEXT,
    expiry_date DATE
);
```

Users should be able to do things like:
- "Find me a quick Italian dinner recipe"
- "Plan my meals for next week, I'm trying to eat healthy"
- "What do I need to buy for this week's meal plan?"
- "I have chicken, rice, and broccoli — what can I make?"
- "Add that pasta recipe to Wednesday's dinner"

Can you design and implement the MCP server? I want clean, well-designed
tools that work well with an AI assistant. Use the Python MCP SDK.
