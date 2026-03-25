import streamlit as st
from activity import get_activities, destination_options

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
.small-muted {
    color: #a0a0a0;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# --- TITLE ---
st.title("Nordic Itinerary Builder")

# --- DATA ---
DESTINATIONS = destination_options()

TRANSPORT_OPTIONS = {
    "Bergen": [
        {"name": "Norway in a Nutshell (Recommended)", "adult": 390, "kid": 290},
        {"name": "Direct Train", "adult": 120, "kid": 80},
    ]
}

RECOMMENDED_NIGHTS = {
    "Oslo": "Recommended: 1–2 nights",
    "Bergen": "Recommended: 2 nights",
}


# --- HELPERS ---
def field(item, key, default=None):
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)


def activity_name(activity):
    return field(activity, "name", "Unnamed activity")


def activity_adult_price(activity):
    return field(activity, "adult", 0) or 0


def activity_kid_price(activity):
    return field(activity, "kid", 0) or 0


def activity_description(activity):
    return field(activity, "description", "")


def destination_activity_options(destination):
    return get_activities(destination) or []


def show_price_card(adult_price, kid_price, description=""):
    st.markdown(
        f"""
        <div class='card'>
            <div class='price'>{adult_price}€ adult / {kid_price}€ kid</div>
            {f"<div class='small-muted'>{description}</div>" if description else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_destination_activities(destination, nights, key_prefix):
    selected_labels = []
    total = 0

    activities = destination_activity_options(destination)

    st.subheader(f"Experiences in {destination}")

    if not activities:
        st.markdown("<div class='card'>No activities available yet.</div>", unsafe_allow_html=True)
        return ["No activity selected"] * nights, total

    labels = [activity_name(a) for a in activities]

    for day in range(1, nights + 1):
        st.markdown(f"**Day {day}**")

        selected_label = st.selectbox(
            "",
            labels,
            key=f"{key_prefix}_{destination}_{day}",
        )
        selected_labels.append(selected_label)

        selected_activity = next(
            a for a in activities if activity_name(a) == selected_label
        )

        adult_price = activity_adult_price(selected_activity)
        kid_price = activity_kid_price(selected_activity)
        description = activity_description(selected_activity)

        show_price_card(adult_price, kid_price, description)
        total += adult_price

    return selected_labels, total


# --- LAYOUT ---
col1, col2 = st.columns([2, 1])

total_price = 0
bergen_selected = []
bergen_nights = 0
add_flam = False

with col1:
    # --- START ---
    st.subheader("Start your journey")
    destination = st.selectbox("Starting destination", DESTINATIONS)

    if destination in RECOMMENDED_NIGHTS:
        st.caption(RECOMMENDED_NIGHTS[destination])

    nights = st.number_input("Number of nights", min_value=1, max_value=5, step=1)

    selected_activities, section_total = render_destination_activities(
        destination=destination,
        nights=nights,
        key_prefix="start",
    )
    total_price += section_total

    # --- NEXT DESTINATION ---
    st.subheader("Continue your journey")

    next_destination = st.selectbox("Next destination", list(TRANSPORT_OPTIONS.keys()))

    transport_list = TRANSPORT_OPTIONS[next_destination]
    transport_labels = [field(t, "name", "Unnamed transport") for t in transport_list]

    transport_choice = st.selectbox("Travel option", transport_labels)

    selected_transport = next(
        t for t in transport_list if field(t, "name") == transport_choice
    )

    transport_adult = field(selected_transport, "adult", 0) or 0
    transport_kid = field(selected_transport, "kid", 0) or 0

    show_price_card(transport_adult, transport_kid)
    total_price += transport_adult

    # --- FLÅM OPTION ---
    if "Nutshell" in transport_choice:
        add_flam = st.checkbox("Add overnight stay in Flåm")

        if add_flam:
            st.markdown("<div class='card'>Flåm overnight stay added</div>", unsafe_allow_html=True)

    # --- BERGEN ---
    if next_destination == "Bergen":
        st.subheader("Stay in Bergen")

        if "Bergen" in RECOMMENDED_NIGHTS:
            st.caption(RECOMMENDED_NIGHTS["Bergen"])

        bergen_nights = st.number_input("Nights in Bergen", min_value=1, max_value=5, step=1)

        bergen_selected, bergen_total = render_destination_activities(
            destination="Bergen",
            nights=bergen_nights,
            key_prefix="bergen",
        )
        total_price += bergen_total

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
