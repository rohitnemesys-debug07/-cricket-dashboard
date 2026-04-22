import streamlit as st
import pandas as pd
from db import get_connection
from api import get_matches

st.set_page_config(page_title="Cricbuzz LiveStats", layout="wide")
st.sidebar.title("🏏 Cricbuzz Dashboard")
st.sidebar.write("Real-time Cricket Analytics")
# =========================
# CREATE TABLES
# =========================
def create_tables():
    conn = get_connection()
    if conn:
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id SERIAL PRIMARY KEY,
            team1 TEXT,
            team2 TEXT,
            status TEXT
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            name TEXT,
            team TEXT,
            role TEXT,
            runs INT,
            wickets INT
        )
        """)

        conn.commit()
        conn.close()

create_tables()

# =========================
# SIDEBAR
# =========================
menu = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Live Matches", "Saved Matches", "Top Players", "SQL Analytics", "CRUD", "Graphs"]
)

# =========================
# HOME
# =========================
# =========================
# HOME
# =========================
if menu == "Home":
    st.title("🏏 Cricbuzz LiveStats Dashboard")

    conn = get_connection()

    if conn:
        matches_count = pd.read_sql("SELECT COUNT(*) FROM matches", conn).iloc[0][0]
        players_count = pd.read_sql("SELECT COUNT(*) FROM players", conn).iloc[0][0]
        conn.close()

        col1, col2 = st.columns(2)
        col1.metric("Total Matches", matches_count)
        col2.metric("Total Players", players_count)

    else:
        st.error("Database not connected")

    st.write("📊 Real-time cricket analytics platform")

# =========================
# LIVE MATCHES
# =========================
elif menu == "Live Matches":

    data = get_matches()
    matches_list = []

    for match_type in data.get("typeMatches", []):
        for series in match_type.get("seriesMatches", []):
            matches = series.get("seriesAdWrapper", {}).get("matches", [])

            for match in matches:
                info = match.get("matchInfo", {})

                matches_list.append({
                    "team1": info.get("team1", {}).get("teamName", ""),
                    "team2": info.get("team2", {}).get("teamName", ""),
                    "status": info.get("status", "")
                })

    df = pd.DataFrame(matches_list[:5])
    st.table(df)

    # ✅ FIXED SAVE BUTTON
    if st.button("Save Matches"):

        conn = get_connection()

        if conn:
            cur = conn.cursor()

            for match in matches_list[:5]:
                cur.execute("""
INSERT INTO matches (team1, team2, status)
VALUES (%s, %s, %s)
ON CONFLICT (team1, team2, status) DO NOTHING
""", (
    match["team1"],
    match["team2"],
    match["status"]
))

            conn.commit()
            conn.close()

            st.success("✅ Saved Successfully!")

        else:
            st.error("❌ Database not connected")

# =========================
# SAVED MATCHES
# =========================
elif menu == "Saved Matches":

    conn = get_connection()

    if conn:
        df = pd.read_sql("SELECT * FROM matches", conn)
        conn.close()
        st.dataframe(df)
    else:
        st.error("Database not connected")

# =========================
# TOP PLAYERS
# =========================
elif menu == "Top Players":

    conn = get_connection()

    if conn:
        query = """
        SELECT name, team, runs, wickets
        FROM players
        ORDER BY runs DESC
        LIMIT 10;
        """

        df = pd.read_sql(query, conn)
        conn.close()

        st.table(df)
    else:
        st.error("Database not connected")

# =========================
# SQL ANALYTICS
# =========================
elif menu == "SQL Analytics":

    conn = get_connection()

    if conn:
        option = st.selectbox("Choose Query", [
            "Matches per Team",
            "Top Run Scorers",
            "All-rounders Performance",
            "Team Total Runs",
            "Top Wicket Takers",
            "Top All-Rounder (Combined Score)"   # ✅ NEW
        ])

        if option == "Matches per Team":
            query = """
            SELECT team, COUNT(*) AS matches
            FROM (
                SELECT team1 AS team FROM matches
                UNION ALL
                SELECT team2 FROM matches
            ) t
            GROUP BY team
            ORDER BY matches DESC;
            """

        elif option == "Top Run Scorers":
            query = """
            SELECT name, runs
            FROM players
            ORDER BY runs DESC
            LIMIT 5;
            """

        elif option == "All-rounders Performance":
            query = """
            SELECT name, runs, wickets
            FROM players
            WHERE role = 'All-rounder'
            ORDER BY runs DESC;
            """

        elif option == "Team Total Runs":
            query = """
            SELECT team, SUM(runs) as total_runs
            FROM players
            GROUP BY team
            ORDER BY total_runs DESC;
            """

        elif option == "Top Wicket Takers":
            query = """
            SELECT name, wickets
            FROM players
            ORDER BY wickets DESC
            LIMIT 5;
            """

        elif option == "Top All-Rounder (Combined Score)":   # ✅ NEW LOGIC
            query = """
            SELECT name,
                   (runs * 0.01 + wickets * 2) AS performance_score
            FROM players
            ORDER BY performance_score DESC
            LIMIT 5;
            """

        df = pd.read_sql(query, conn)
        conn.close()

        st.dataframe(df)

        # 🔥 INSIGHT LINE
        if not df.empty:
            st.write(f"📊 Insight: Top result → {df.iloc[0][0]}")

    else:
        st.error("Database not connected")

# =========================
# CRUD OPERATIONS
# =========================
elif menu == "CRUD":

    st.subheader("Add Player")

    name = st.text_input("Name")
    team = st.text_input("Team")
    role = st.selectbox("Role", ["Batsman", "Bowler", "All-rounder"])
    runs = st.number_input("Runs", 0)
    wickets = st.number_input("Wickets", 0)

    if st.button("Add Player"):
        conn = get_connection()

        if conn:
            cur = conn.cursor()

            cur.execute("""
            INSERT INTO players (name, team, role, runs, wickets)
            VALUES (%s, %s, %s, %s, %s)
            """, (name, team, role, runs, wickets))

            conn.commit()
            conn.close()

            st.success("Player Added")
        else:
            st.error("Database not connected")

    # DELETE
    st.subheader("Delete Player")
    player_id = st.number_input("Player ID", 0)

    if st.button("Delete"):
        conn = get_connection()

        if conn:
            cur = conn.cursor()

            cur.execute("DELETE FROM players WHERE id=%s", (player_id,))
            conn.commit()
            conn.close()

            st.success("Deleted")
        else:
            st.error("Database not connected")

# =========================
# GRAPHS
# =========================
elif menu == "Graphs":

    conn = get_connection()

    if conn:
        df_runs = pd.read_sql("SELECT name, runs FROM players ORDER BY runs DESC", conn)
        df_wickets = pd.read_sql("SELECT name, wickets FROM players ORDER BY wickets DESC", conn)

        conn.close()

        st.subheader("🏏 Top Run Scorers")
        st.bar_chart(df_runs.set_index("name"))

        st.subheader("🎯 Top Wicket Takers")
        st.bar_chart(df_wickets.set_index("name"))

        # Insight
        if not df_runs.empty:
            st.write(f"🔥 Insight: {df_runs.iloc[0]['name']} is the highest run scorer")

    else:
        st.error("Database not connected")
