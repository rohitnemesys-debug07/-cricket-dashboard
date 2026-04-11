from db import get_connection
import streamlit as st
import pandas as pd
from api import get_matches

# =========================
# CREATE DATABASE TABLE
# =========================
conn = get_connection()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS matches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    team1 TEXT,
    team2 TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()

# =========================
# UI
# =========================
st.title("🏏 Cricket Project")
st.write("Hello Rohit! Project started successfully 🚀")
menu = st.sidebar.selectbox(
    "Select Option",
    ["Home", "Live Matches", "Saved Matches", "Analytics", "Graphs"]
)
if menu == "Home":
    st.header("🏏 Welcome to Cricket Analytics Dashboard")
    st.write("Use the sidebar to navigate")

# =========================
# BUTTON 1 - PLAYERS
# =========================
if st.button("Show Players"):

    data = {
        "Player": ["Virat Kohli", "Rohit Sharma", "MS Dhoni"],
        "Country": ["India", "India", "India"],
        "Role": ["Batsman", "Batsman", "Wicketkeeper"]
    }

    df = pd.DataFrame(data)
    st.table(df)

# =========================
# BUTTON 2 - LIVE MATCHES
# =========================
if menu == "Live Matches":

    data = get_matches()

    try:
        matches_list = []
        count = 0

        for match_type in data["typeMatches"]:
            for series in match_type.get("seriesMatches", []):

                matches = series.get("seriesAdWrapper", {}).get("matches", [])

                for match in matches:

                    if count >= 5:
                        break

                    info = match["matchInfo"]

                    team1 = info["team1"]["teamName"]
                    team2 = info["team2"]["teamName"]
                    status = info["status"]

                    # =========================
                    # SHOW DATA IN UI
                    # =========================
                    matches_list.append({
                        "Team 1": team1,
                        "Team 2": team2,
                        "Status": status
                    })

                    # =========================
                    # SAVE INTO DATABASE
                    # =========================
                    conn = get_connection()
                    cur = conn.cursor()

                    cur.execute("""
                    INSERT INTO matches (team1, team2, status)
                    VALUES (?, ?, ?)
                    """, (team1, team2, status))

                    conn.commit()
                    conn.close()

                    count += 1

        # =========================
        # DISPLAY TABLE
        # =========================
        if matches_list:
            df = pd.DataFrame(matches_list)
            st.table(df)
        else:
            st.warning("No matches found")

    except Exception as e:
        st.error(e)
# SHOW SAVED MATCHES (DB)
# =========================
if menu == "Saved Matches":

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT team1, team2, status FROM matches")
    data = cur.fetchall()

    conn.close()

    if data:
        df = pd.DataFrame(data, columns=["Team 1", "Team 2", "Status"])
        st.table(df)
    else:
        st.warning("No saved data found")

# =========================
# TEAM ANALYTICS
# =========================
if menu == "Analytics":

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT team1 FROM matches
    UNION ALL
    SELECT team2 FROM matches
    """)

    data = cur.fetchall()
    conn.close()

    if data:
        df = pd.DataFrame(data, columns=["Team"])
        result = df["Team"].value_counts().reset_index()
        result.columns = ["Team", "Matches Played"]
        st.table(result)
    else:
        st.warning("No data found")

# =========================
# STATUS ANALYTICS
# =========================
if st.button("📊 Status Analytics"):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT status FROM matches")
    data = cur.fetchall()

    conn.close()

    if data:
        df = pd.DataFrame(data, columns=["Status"])
        result = df["Status"].value_counts().reset_index()
        result.columns = ["Status", "Count"]
        st.table(result)
    else:
        st.warning("No data found")
        
if menu == "Graphs":

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT team1 FROM matches
    UNION ALL
    SELECT team2 FROM matches
    """)

    data = cur.fetchall()
    conn.close()

    df = pd.DataFrame(data, columns=["Team"])

    result = df["Team"].value_counts()

    st.bar_chart(result)