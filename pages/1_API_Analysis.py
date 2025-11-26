import streamlit as st
import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

st.title("Comparing NBA players")

if "num_players" not in st.session_state:
    st.session_state.num_players = 2

    
if "chosen_players" not in st.session_state:
    st.session_state.chosen_players = []

with st.container():
    st.markdown("Choose Your Players")

    num = st.slider("How many players do you want to compare? (2-5)", 2, 5, st.session_state.num_players)
    st.session_state.num_players = num

    player_list = players.get_players()
    names = [p["full_name"] for p in player_list]

    cols = st.columns(num)
    chosen = []
    for i in range(num):
        with cols[i]:

            pick = st.selectbox(f"Player {i+1}", names, key=f"player_{i}")
            chosen.append(pick)

    st.session_state.chosen_players = chosen

all_data = []
avg_rows = []
for name in st.session_state.chosen_players:

    pid = next(player["id"] for player in player_list if player["full_name"] == name)
    data = playercareerstats.PlayerCareerStats(player_id=pid)
    df = data.get_data_frames()[0]


    df["Player"] = name
    all_data.append(df)

    avg = df[["PTS", "AST", "REB"]].mean()/82
    avg_rows.append({"Player": name, "PTS": avg["PTS"], "AST": avg["AST"], "REB": avg["REB"]})

if len(all_data) > 0:
    combined = pd.concat(all_data)

    avg_df = pd.DataFrame(avg_rows)

    tab1, tab2, tab3 = st.tabs(["Career Avgs", "Points over time", "Raw Data"])

    with tab1:
        st.markdown("Career Averages per Game")

        st.bar_chart(avg_df.set_index("Player"))


        with st.expander("Exact numbers"):
            st.dataframe(avg_df, use_container_width=True)
    with tab2:
        st.markdown("Points per Season Comparison")
        
        chart_cols = st.columns(2)

        for num, name in enumerate(st.session_state.chosen_players):
            player_df = combined[combined["Player"] == name]
            pts_data = player_df[["SEASON_ID", "PTS"]].set_index("SEASON_ID")

            with chart_cols[num % 2]:
                st.write(f"{name}")
                st.line_chart(pts_data)

    with tab3:
        st.markdown("Complete Career Statistics")

        player_to_show = st.selectbox("Select Player for stats", st.session_state.chosen_players)
        player_data = combined[combined["Player"] == player_to_show]


        st.dataframe(player_data, use_container_width=True)

else:
    with st.container():
        st.info("Select players to see stats!")
