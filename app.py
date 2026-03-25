import streamlit as st
from activity import DESTINATIONS, get_activities

# --- PAGE CONFIG ---
st.set_page_config(page_title="Nordic Itinerary Builder", layout="wide")

# --- STYLING ---
st.markdown("""
<style>
body { background-color: #0e1117; }
h1, h2, h3 { color: #ffffff; }
.block-container { padding-top: 2rem; }
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
}
.price {
    color: #f9c74f;
    font-weight: bold;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# --- TITLE ---
st.title("Nordic Itinerary Builder")

# --- DATA (STRUCTURED – EASY TO MOVE TO EXCEL LATER) ---

destinations = ["Oslo", "Stockholm", "Copenhagen", "Helsinki", "Reykjavik"]

activities = {
    "Oslo": [
        {"name": "Fjord Sightseeing Cruise (Electric Boat)", "adult": 50, "kid": 30},
        {"name": "Essential Oslo Walking Tour", "adult": 40, "kid": 25}
    ],
    "Bergen": [
        {"name": "Walking Tour of Bergen Past & Present", "adult": 40, "kid": 25},
        {"name": "Mostraumen Fjord & Waterfall Cruise", "adult": 80, "kid": 60},
        {"name": "Fløibanen Funicular Tickets", "adult": 25, "kid": 15}
    ]
}

transport_options = {
    "Bergen": [
        {"name": "Norway in a Nutshell (Recommended)", "adult": 390, "kid": 290},
        {"name": "Direct Train", "adult": 120, "kid": 80}
    ]
}

# --- LAYOUT ---
col1, col2 = st.columns([2, 1])

total_price = 0

with col1:

    # --- START ---
    st.subheader("Start your journey")
    destination = st.selectbox("Starting destination", destinations)

    if destination == "Oslo":
        st.caption("Recommended: 1–2 nights")

    nights = st.number_input("Number of nights", min_value=1, max_value=5, step=1)

    # --- ACTIVITIES ---
    st.subheader(f"Experiences in {destination}")

    selected_activities = []

    for day in range(1, nights + 1):
        st.markdown(f"**Day {day}**")

        options = activities.get(destination, [])
        labels = [a["name"] for a in options]

        choice = st.selectbox("", labels, key=f"{destination}_{day}")
        selected_activities.append(choice)

        for a in options:
            if a["name"] == choice:
                st.markdown(f"<div class='card'>"
                            f"<div class='price'>{a['adult']}€ adult / {a['kid']}€ kid</div>"
                            f"</div>", unsafe_allow_html=True)
                total_price += a["adult"]

    # --- NEXT DESTINATION ---
    st.subheader("Continue your journey")

    next_destination = st.selectbox("Next destination", list(transport_options.keys()))

    transport_list = transport_options[next_destination]
    transport_labels = [t["name"] for t in transport_list]

    transport_choice = st.selectbox("Travel option", transport_labels)

    selected_transport = next(t for t in transport_list if t["name"] == transport_choice)

    st.markdown(f"<div class='card'>"
                f"<div class='price'>{selected_transport['adult']}€ adult / {selected_transport['kid']}€ kid</div>"
                f"</div>", unsafe_allow_html=True)

    total_price += selected_transport["adult"]

    # --- FLÅM OPTION ---
    add_flam = False
    if "Nutshell" in transport_choice:
        add_flam = st.checkbox("Add overnight stay in Flåm")

        if add_flam:
            st.markdown("<div class='card'>Flåm overnight stay added</div>", unsafe_allow_html=True)

    # --- BERGEN ---
    if next_destination == "Bergen":
        st.subheader("Stay in Bergen")
        st.caption("Recommended: 2 nights")

        bergen_nights = st.number_input("Nights in Bergen", min_value=1, max_value=5, step=1)

        st.subheader("Experiences in Bergen")

        bergen_selected = []

        for day in range(1, bergen_nights + 1):
            st.markdown(f"**Day {day}**")

            options = activities["Bergen"]
            labels = [a["name"] for a in options]

            choice = st.selectbox("", labels, key=f"bergen_{day}")
            bergen_selected.append(choice)

            for a in options:
                if a["name"] == choice:
                    st.markdown(f"<div class='card'>"
                                f"<div class='price'>{a['adult']}€ adult / {a['kid']}€ kid</div>"
                                f"</div>", unsafe_allow_html=True)
                    total_price += a["adult"]

with col2:

    st.subheader("Your itinerary")

    st.markdown(f"**Start:** {destination}")
    st.markdown(f"**Nights:** {nights}")

    for i, act in enumerate(selected_activities, start=1):
        st.markdown(f"Day {i}: {act}")

    st.markdown(f"**Next:** {next_destination}")
    st.markdown(f"**Travel:** {transport_choice}")

    if add_flam:
        st.markdown("Includes: Flåm overnight stay")

    if next_destination == "Bergen":
        st.markdown(f"**Bergen nights:** {bergen_nights}")

        for i, act in enumerate(bergen_selected, start=1):
            st.markdown(f"Bergen Day {i}: {act}")

    st.markdown("---")

    st.subheader("Estimated price")

    st.markdown(f"### {total_price} € per adult")

    end_trip = st.radio("End itinerary?", ["No", "Yes"])

    if end_trip == "Yes":
        transfer = st.radio("Airport transfer", ["No", "Yes"])
        st.markdown(f"Transfer: {transfer}")

    st.button("Confirm itinerary")
