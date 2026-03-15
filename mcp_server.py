from fastmcp import FastMCP
from supabase import create_client
import os
from datetime import date
from pathlib import Path
from dotenv import load_dotenv

# load env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

mcp = FastMCP("EatButCount")

supabase = create_client(
    os.getenv("VITE_SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)


@mcp.tool()
def get_today_food_logs(telegram_id: int):
    """Return today's food logs for the user."""

    result = supabase.table("food_logs")\
        .select("*")\
        .eq("telegram_id", telegram_id)\
        .eq("log_date", date.today().isoformat())\
        .order("created_at", desc=True)\
        .execute()
    print(result.data)
    return result.data

@mcp.tool()
def health():
    """Check MCP server status"""
    return {"status": "ok"}

@mcp.tool()
def add_food_log(
    telegram_id: int,
    food: str,
    calories: int,
    protein: int,
    carbs: int,
    fat: int
):
    """Insert a food log into the database."""

    result = supabase.table("food_logs").insert({
        "telegram_id": telegram_id,
        "food": food,
        "calories": calories,
        "protein": protein,
        "carbs": carbs,
        "fat": fat
    }).execute()
    print(result.data)
    return result.data


if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
    )