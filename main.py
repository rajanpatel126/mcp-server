from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), 'expenses.db')

CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), 'categories.json')

mcp = FastMCP("Expense Tracker")

#database initialization
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
                     CREATE TABLE IF NOT EXISTS expenses (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            amount REAL NOT NULL,
                            category TEXT NOT NULL,
                            subcategory TEXT NOT NULL DEFAULT '',
                            date TEXT NOT NULL,
                            note TEXT DEFAULT ''
                     )
                     """)
        
init_db()

# adding expense
@mcp.tool()
def add_expense(amount: float, category: str, subcategory: str = '', date: str='', note: str = ''):
    """Add a new expense to the tracker."""
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("""
                     INSERT INTO expenses (amount, category, subcategory, date, note)
                     VALUES (?, ?, ?, ?, ?)
                     """, (amount, category, subcategory, date, note))
    return {'status':'ok', 'id': cur.lastrowid}

# listing all expenses
@mcp.tool()
def list_all_expenses(start_date: None, end_date: None):
    """List all expenses."""
    with sqlite3.connect(DB_PATH) as conn:
        query = "SELECT (amount, category, subcategory, date, note) FROM expenses ORDER BY id ASC"
        params = []

        if start_date and end_date:
            query += " WHERE date BETWEEN ? AND ?"
            params.extend([start_date, end_date])
            
        cur = conn.execute(query, params)
        cols = [description[0] for description in cur.description]
        expenses = [dict(zip(cols, row)) for row in cur.fetchall()]
        return {'expenses': expenses}

# deleting expense
@mcp.tool()
def delete_expense(expense_id: int):
    """Delete an expense by its ID."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    return {'status':'ok'}

# summary
@mcp.tool()
def summary(start_date: str = '', end_date: str = '', category = None):
    "Summary of expnses by category within a date range."
    with sqlite3.connect(DB_PATH) as conn:
        query = """
        SELECT category, SUM(amount) as total_amount
        FROM expenses
        WHERE date BETWEEN ? AND ?
        """
        params = [start_date, end_date]
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        cur = conn.execute(query, params)
        cols = [description[0] for description in cur.description]
        expenses = [dict(zip(cols, row)) for row in cur.fetchall()]
        return {'expenses': expenses}

@mcp.resource("expense://categories", mime_type='application/json')
def categories():
    with open(CATEGORIES_PATH, 'r', encoding='utf-8') as f:
        return f.read()

# running the MCP
if __name__ == "__main__":
    mcp.run()
