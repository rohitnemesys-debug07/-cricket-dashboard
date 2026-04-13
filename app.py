
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

# =========================
# HOME
# =========================
if menu == "Home":
    st.header("🏏 Welcome to Cricket Analytics Dashboard")
    st.write("Use the sidebar to navigate")

# =========================
# LIVE MATCHES
# =========================
elif menu == "Live Matches":

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

                    matches_list.append({
                        "Team 1": team1,
                        "Team 2": team2,
                        "Status": status
                    })

                    count += 1

        # =========================
        # DISPLAY + SAVE BUTTON
        # =========================
        if matches_list:
            df = pd.DataFrame(matches_list)
            st.table(df)

            # ✅ SAVE BUTTON
            if st.button("Save Matches to Database"):
                conn = get_connection()
                cur = conn.cursor()

                for match in matches_list:
                    cur.execute("""
                    INSERT INTO matches (team1, team2, status)
                    VALUES (?, ?, ?)
                    """, (match["Team 1"], match["Team 2"], match["Status"]))

                conn.commit()
                conn.close()

                st.success("Matches saved successfully!")

        else:
            st.warning("No matches found")

    except Exception as e:
        st.error(e)

# =========================
# SAVED MATCHES
# =========================
elif menu == "Saved Matches":

    conn = get_connection()
    df = pd.read_sql("SELECT * FROM matches", conn)
    conn.close()

    if not df.empty:
        st.table(df)
    else:
        st.warning("No saved data found")

# =========================
# ANALYTICS
# =========================
elif menu == "Analytics":

    conn = get_connection()

    query = """
    SELECT team1 as team FROM matches
    UNION ALL
    SELECT team2 FROM matches
    """

    df = pd.read_sql(query, conn)
    conn.close()

    if not df.empty:
        result = df["team"].value_counts().reset_index()
        result.columns = ["Team", "Matches Played"]
        st.table(result)
    else:
        st.warning("No data found")

# =========================
# GRAPHS
# =========================
elif menu == "Graphs":

    conn = get_connection()

    query = """
    SELECT team1 as team FROM matches
    UNION ALL
    SELECT team2 FROM matches
    """

    df = pd.read_sql(query, conn)
    conn.close()

    if not df.empty:
        result = df["team"].value_counts()
        st.bar_chart(result)
    else:
        st.warning("No data to display")

