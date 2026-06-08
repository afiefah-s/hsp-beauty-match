import streamlit as st #Streamlit laden, hiermee maak je de website/app.
import pandas as pd #Pandas laden, hiermee verwerk je tabellen en CSV-bestanden.
import numpy as np #NumPy laden, voor wiskundige berekeningen.
import plotly.graph_objects as go #Plotly laden, hiermee maak je interactieve grafieken.

st.set_page_config(page_title="HSP Beauty Match", layout="wide")

st.title("HSP Compatibiliteit Tool voor Cosmetica")

st.sidebar.title("Menu")
pagina = st.sidebar.radio(
    "Ga naar:",
    ["Informatie", "Compatibiliteitsanalyse", "Oplosmiddelenbibliotheek"]
)

# Voorbeelddata
data = pd.DataFrame([
    {"Oplosmiddel": "Ethanol", "D": 15.8, "P": 8.8, "H": 19.4},
    {"Oplosmiddel": "Water", "D": 15.5, "P": 16.0, "H": 42.3},
    {"Oplosmiddel": "Acetone", "D": 15.5, "P": 10.4, "H": 7.0},
    {"Oplosmiddel": "DMSO", "D": 18.4, "P": 16.4, "H": 10.2},

    {"Oplosmiddel": "Pyridine", "D": 19.0, "P": 8.8, "H": 5.9},
    {"Oplosmiddel": "N-Methyl-2-Pyrrolidone", "D": 18.0, "P": 12.3, "H": 7.2},
    {"Oplosmiddel": "Methylene Chloride", "D": 17.0, "P": 7.3, "H": 7.1},
    {"Oplosmiddel": "1,3-Dioxolane", "D": 18.1, "P": 6.6, "H": 9.3},
    {"Oplosmiddel": "Methyl Ethyl Ketone", "D": 16.0, "P": 9.0, "H": 5.1},
    {"Oplosmiddel": "Tetrahydrofuran", "D": 16.8, "P": 5.7, "H": 8.0},
    {"Oplosmiddel": "Chloroform", "D": 17.8, "P": 3.1, "H": 5.7},
    {"Oplosmiddel": "Dimethyl Formamide", "D": 17.4, "P": 13.7, "H": 11.3},
    {"Oplosmiddel": "1,4-Dioxane", "D": 17.5, "P": 1.8, "H": 9.0},
    {"Oplosmiddel": "Ethyl Acetate", "D": 15.8, "P": 5.3, "H": 7.2},
    {"Oplosmiddel": "Furan", "D": 17.0, "P": 1.8, "H": 5.3},
    {"Oplosmiddel": "m-Cresol", "D": 18.5, "P": 6.5, "H": 13.7},
    {"Oplosmiddel": "Toluene", "D": 18.0, "P": 1.4, "H": 2.0},
    {"Oplosmiddel": "Xylene", "D": 17.8, "P": 1.0, "H": 3.1}
])


def bereken_ra(row, gekozen):
    return np.sqrt(
        4 * (row["D"] - gekozen["D"]) ** 2 +
        (row["P"] - gekozen["P"]) ** 2 +
        (row["H"] - gekozen["H"]) ** 2
    )


if pagina == "Informatie":
    st.header("Wat zijn HSP-waarden?")
    st.write("""
    Hansen Solubility Parameters bestaan uit drie waarden:

    **D** = dispersiekrachten  
    **P** = polaire krachten  
    **H** = waterstofbruggen  

    Met deze waarden kun je voorspellen of oplosmiddelen goed bij elkaar passen.
    De Ra-waarde geeft de afstand tussen twee stoffen in de HSP-ruimte.
    """)

    st.latex(r"Ra^2 = 4(\delta D_1-\delta D_2)^2 + (\delta P_1-\delta P_2)^2 + (\delta H_1-\delta H_2)^2") #formule Ra

    st.subheader("Beoordeling van compatibiliteit")

    st.write("""
    De beoordeling wordt gebaseerd op de Hansen-afstand (Ra):

    | Ra-waarde | Beoordeling |
    |-----------|-------------|
    | Ra < 5 | Goed compatibel |
    | 5 ≤ Ra ≤ 10 | Matig compatibel |
    | Ra > 10 | Incompatibel |
    """)

    st.link_button("Meer informatie over HSP", "https://www.hansen-solubility.com/HSP-science/basics.php")

elif pagina == "Oplosmiddelenbibliotheek":
    st.header("Oplosmiddelenbibliotheek")
    st.dataframe(data)

elif pagina == "Compatibiliteitsanalyse":
    st.header("Compatibiliteitsanalyse")

    keuze = st.selectbox("Kies een oplosmiddel:", data["Oplosmiddel"])
    gekozen = data[data["Oplosmiddel"] == keuze].iloc[0]

    resultaten = data.copy()
    resultaten["Ra"] = resultaten.apply(
        lambda row: bereken_ra(row, gekozen),
        axis=1
    )

    def beoordeling_kleur(ra):
        if ra < 5:
            return "🟢 Goed compatibel"
        elif ra <= 10:
            return "🟠 Matig compatibel"
        else:
            return "🔴 Incompatibel"

    resultaten["Beoordeling"] = resultaten["Ra"].apply(beoordeling_kleur)

    st.subheader("Resultaten")
    st.dataframe(resultaten)

    goed = len(resultaten[resultaten["Ra"] < 5])
    matig = len(resultaten[
        (resultaten["Ra"] >= 5) &
        (resultaten["Ra"] <= 10)
    ])
    slecht = len(resultaten[resultaten["Ra"] > 10])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="
            background-color:#eaf8ef;
            border-left:6px solid #22c55e;
            padding:1px;
            border-radius:12px;
            text-align:center;
        ">
            <h1 style="color:#16a34a;">{goed}</h1>
            <p>Goed compatibel<br>(Ra &lt; 5)</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="
            background-color:#fff7e6;
            border-left:6px solid #f97316;
            padding:1px;
            border-radius:12px;
            text-align:center;
        ">
            <h1 style="color:#ea580c;">{matig}</h1>
            <p>Matig compatibel<br>(Ra 5 - 10)</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="
            background-color:#fdecec;
            border-left:6px solid #dc2626;
            padding:1px;
            border-radius:12px;
            text-align:center;
        ">
            <h1 style="color:#dc2626;">{slecht}</h1>
            <p>Incompatibel<br>(Ra &gt; 10)</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("3D HSP-sphere")


    def maak_bol(center_d, center_p, center_h, radius):
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)

        x = center_d + radius * np.outer(np.cos(u), np.sin(v))
        y = center_p + radius * np.outer(np.sin(u), np.sin(v))
        z = center_h + radius * np.outer(np.ones(len(u)), np.cos(v))

        return x, y, z


    fig = go.Figure()

    # Oranje bol: Ra <= 10 rondom gekozen oplosmiddel
    x10, y10, z10 = maak_bol(gekozen["D"], gekozen["P"], gekozen["H"], 10)
    fig.add_trace(go.Surface(
        x=x10,
        y=y10,
        z=z10,
        opacity=0.15,
        colorscale=[[0, "#f59e0b"], [1, "#f59e0b"]],
        showscale=False,
        name="Ra ≤ 10"
    ))

    # Groene bol: Ra <= 5 rondom gekozen oplosmiddel
    x5, y5, z5 = maak_bol(gekozen["D"], gekozen["P"], gekozen["H"], 5)
    fig.add_trace(go.Surface(
        x=x5,
        y=y5,
        z=z5,
        opacity=0.28,
        colorscale=[[0, "#22c55e"], [1, "#22c55e"]],
        showscale=False,
        name="Ra ≤ 5"
    ))

    goed_df = resultaten[resultaten["Ra"] < 5]
    matig_df = resultaten[(resultaten["Ra"] >= 5) & (resultaten["Ra"] <= 10)]
    slecht_df = resultaten[resultaten["Ra"] > 10]

    # Groene bolletjes: goed compatibele oplosmiddelen
    fig.add_trace(go.Scatter3d(
        x=goed_df["D"],
        y=goed_df["P"],
        z=goed_df["H"],
        mode="markers+text",
        text=goed_df["Oplosmiddel"],
        marker=dict(size=8, color="#22c55e", symbol="circle"),
        name="Goed compatibel"
    ))

    # Oranje bolletjes: matig compatibele oplosmiddelen
    fig.add_trace(go.Scatter3d(
        x=matig_df["D"],
        y=matig_df["P"],
        z=matig_df["H"],
        mode="markers+text",
        text=matig_df["Oplosmiddel"],
        marker=dict(size=8, color="#f59e0b", symbol="circle"),
        name="Matig compatibel"
    ))

    # Rode vierkanten: incompatibele oplosmiddelen
    fig.add_trace(go.Scatter3d(
        x=slecht_df["D"],
        y=slecht_df["P"],
        z=slecht_df["H"],
        mode="markers+text",
        text=slecht_df["Oplosmiddel"],
        marker=dict(size=8, color="#dc2626", symbol="square"),
        name="Incompatibel"
    ))

    # Gekozen oplosmiddel: blauwe diamant
    fig.add_trace(go.Scatter3d(
        x=[gekozen["D"]],
        y=[gekozen["P"]],
        z=[gekozen["H"]],
        mode="markers+text",
        text=[gekozen["Oplosmiddel"]],
        marker=dict(size=15, color="#0ea5e9", symbol="diamond"),
        name="Gekozen oplosmiddel"
    ))

    fig.update_layout(
        title="Hansen-ruimte: gekozen oplosmiddel vs andere oplosmiddelen",
        scene=dict(
            xaxis=dict(title="δD", range=[0, 45]),
            yaxis=dict(title="δP", range=[0, 45]),
            zaxis=dict(title="δH", range=[0, 45]),
            aspectmode="cube"
        ),
        height=700
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Eigen CSV-bestand uploaden")

    bestand = st.file_uploader("Upload een CSV met HSP waarden van oplosmiddelen/cosmetica producten", type="csv")





