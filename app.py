import streamlit as st
import pandas as pd
from db import get_connection
from api import get_matches

# ✅ STEP 1: Page config (ONLY ONCE)
st.set_page_config(page_title="🏏 Cricbuzz Pro Dashboard", layout="wide")

# ✅ STEP 2: PASTE CSS HERE (IMPORTANT)
st.markdown("""
<style>

/* MAIN BACKGROUND */
[data-testid="stAppViewContainer"] {
    background-color: #0E1117;
    color: white;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #111827;
}

/* TEXT */
[data-testid="stMarkdownContainer"] {
    color: white;
}

/* CARD */
.card {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 15px;
}

/* HEADINGS */
h1, h2, h3 {
    color: #00FFAA;
}

</style>
""", unsafe_allow_html=True)

# ✅ STEP 3: THEN your sidebar
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
            status TEXT,
            UNIQUE(team1, team2, status)
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
# MENU
# =========================
menu = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Live Matches", "Saved Matches", "Top Players", "SQL Analytics", "SQL Practice", "CRUD", "Graphs"]
)

# =========================
# HOME
# =========================
if menu == "Home":
    st.title("🏏 Cricbuzz LiveStats Dashboard")

    st.markdown("""
    ### 📌 Project Overview
    - Live cricket data using API
    - SQL-based analytics
    - CRUD operations
    - Interactive dashboard

    ### 🛠️ Tech Stack
    Python • Streamlit • PostgreSQL • REST API
    """)

    conn = get_connection()

    if conn:
        try:
            matches_count = pd.read_sql("SELECT COUNT(*) as count FROM matches", conn).iloc[0]["count"]
        except:
            matches_count = 0

        try:
            players_count = pd.read_sql("SELECT COUNT(*) as count FROM players", conn).iloc[0]["count"]
        except:
            players_count = 0

        conn.close()

        col1, col2 = st.columns(2)
        col1.metric("Total Matches", matches_count)
        col2.metric("Total Players", players_count)

    else:
        st.error("Database not connected")

# =========================
# LIVE MATCHES
# =========================
elif menu == "Live Matches":

    st.subheader("🏏 Live Matches")

    data = get_matches()

    for match in data[:6]:

        name = match.get("name", "")
        status = match.get("status", "Unknown")
        venue = match.get("venue", "N/A")

        if " vs " in name:
            team1, team2 = name.split(" vs ")
        else:
            team1, team2 = name, ""

        
        if "Live" in status or "Progress" in status:
            color = "green"
        elif "Upcoming" in status:
            color = "orange"
        else:
            color = "red"

        st.markdown(f"""
        <div class="card">
            <h3>{team1} 🆚 {team2}</h3>
            <p><b>Status:</b> <span style="color:{color};">{status}</span></p>
            <p><b>Venue:</b> {venue}</p>
        </div>
        """, unsafe_allow_html=True)
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

    if st.button("Load Sample Players"):
        conn = get_connection()
        if conn:
            cur = conn.cursor()

            cur.execute("""
            INSERT INTO players (name, team, role, runs, wickets) VALUES
            ('Virat Kohli', 'India', 'Batsman', 12000, 4),
            ('Rohit Sharma', 'India', 'Batsman', 10000, 8),
            ('Ben Stokes', 'England', 'All-rounder', 6000, 200),
            ('Hardik Pandya', 'India', 'All-rounder', 4000, 150),
            ('Jasprit Bumrah', 'India', 'Bowler', 200, 300)
            ON CONFLICT DO NOTHING;
            """)

            conn.commit()
            conn.close()

            st.success("Sample Players Loaded ✅")

    search = st.text_input("Search Player")

    conn = get_connection()

    if conn:
        df = pd.read_sql("""
        SELECT name, team, runs, wickets
        FROM players
        ORDER BY runs DESC
        """, conn)

        conn.close()

        if search:
            df = df[df["name"].str.contains(search, case=False)]

        st.table(df.head(10))

        if not df.empty:
            st.write(f"🔥 Top Player: {df.iloc[0]['name']}")

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
            "All-rounders",
            "Team Runs",
            "Top Wickets",
            "Best All-rounder"
        ])

        queries = {
            "Matches per Team": """
            SELECT team, COUNT(*) FROM (
                SELECT team1 AS team FROM matches
                UNION ALL
                SELECT team2 FROM matches
            ) t GROUP BY team ORDER BY COUNT(*) DESC
            """,

            "Top Run Scorers": "SELECT name, runs FROM players ORDER BY runs DESC LIMIT 5",

            "All-rounders": "SELECT name, runs, wickets FROM players WHERE role='All-rounder'",

            "Team Runs": "SELECT team, SUM(runs) FROM players GROUP BY team",

            "Top Wickets": "SELECT name, wickets FROM players ORDER BY wickets DESC LIMIT 5",

            "Best All-rounder": """
            SELECT name, (runs*0.01 + wickets*2) AS score
            FROM players ORDER BY score DESC LIMIT 5
            """
        }

        df = pd.read_sql(queries[option], conn)
        conn.close()

        st.dataframe(df)

        if not df.empty:
            st.success(f"🔥 Insight: {df.iloc[0][0]} is leading")

    else:
        st.error("Database not connected")

# =========================
# SQL PRACTICE
# =========================
elif menu == "SQL Practice":

    st.subheader("🧠 SQL Practice")

    query = st.text_area("Write your SQL query:")

    if st.button("Run Query"):
        conn = get_connection()
        if conn:
            try:
                df = pd.read_sql(query, conn)
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error: {e}")
            conn.close()

# =========================
# CRUD
# =========================
elif menu == "CRUD":

    st.title("🛠️ Player Management (CRUD)")

    conn = get_connection()

    # =========================
    # READ (SHOW DATA)
    # =========================
    if conn:
        df = pd.read_sql("SELECT * FROM players", conn)
        st.subheader("📋 Existing Players")
        st.dataframe(df)
    else:
        st.error("Database not connected")

    st.divider()

    # =========================
    # CREATE
    # =========================
    st.subheader("➕ Add Player")

    name = st.text_input("Name")
    team = st.text_input("Team")
    role = st.selectbox("Role", ["Batsman", "Bowler", "All-rounder"])
    runs = st.number_input("Runs", 0)
    wickets = st.number_input("Wickets", 0)

    if st.button("Add Player"):
        if conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO players (name, team, role, runs, wickets)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, team, role, runs, wickets))
            conn.commit()
            st.success("✅ Player Added")

    st.divider()

    # =========================
    # UPDATE
    # =========================
    st.subheader("✏️ Update Player")

    if conn:
        player_ids = df["id"].tolist()

        if player_ids:
            selected_id = st.selectbox("Select Player ID", player_ids)

            new_runs = st.number_input("New Runs", 0)
            new_wickets = st.number_input("New Wickets", 0)

            if st.button("Update Player"):
                cur = conn.cursor()
                cur.execute("""
                    UPDATE players
                    SET runs=%s, wickets=%s
                    WHERE id=%s
                """, (new_runs, new_wickets, selected_id))
                conn.commit()
                st.success("✅ Updated Successfully")
        else:
            st.warning("No players available to update")

    st.divider()

    # =========================
    # DELETE
    # =========================
    st.subheader("❌ Delete Player")

    if conn and not df.empty:
        delete_id = st.selectbox("Select Player ID to Delete", df["id"].tolist())

        if st.button("Delete Player"):
            cur = conn.cursor()
            cur.execute("DELETE FROM players WHERE id=%s", (delete_id,))
            conn.commit()
            st.success("✅ Deleted Successfully")

    if conn:
        conn.close()

# =========================
# GRAPHS
# =========================
elif menu == "Graphs":

    conn = get_connection()

    if conn:
        df_runs = pd.read_sql("SELECT name, runs FROM players ORDER BY runs DESC", conn)
        df_wickets = pd.read_sql("SELECT name, wickets FROM players ORDER BY wickets DESC", conn)

        conn.close()

        st.subheader("🏏 Runs")
        st.bar_chart(df_runs.set_index("name"))

        st.subheader("🎯 Wickets")
        st.bar_chart(df_wickets.set_index("name"))

    else:
        st.error("Database not connected")