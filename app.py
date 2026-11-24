import streamlit as st
import pandas as pd
import numpy as np
import statistics
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from clustergram import Clustergram
import os

# Налаштування сторінки
st.set_page_config(
    page_title="Лабораторні роботи №9–12 | Варіант 12",
    page_icon="📊",
    layout="wide"
)

# Глобальний стиль графіків
sns.set_theme(style="whitegrid", palette="muted")

# Бокова панель (Sidebar)
with st.sidebar:
    st.title("🎓 Практикум з ІЗАД")
    st.markdown("**Дисципліна:** Інструментальні засоби аналізу даних")
    st.markdown("**Варіант:** №12")
    st.markdown("**Роботи:** Лабораторні №9 – №12 (Python)")
    st.divider()
    st.info(
        "Оберіть потрібну лабораторну роботу на вкладках праворуч. "
        "Усі таблиці та параметри моделювання є інтерактивними."
    )

st.title("📊 Інтерактивний дашборд лабораторних робіт (№9–12)")
st.caption("Реалізація завдань варіанту 12 засобами Python, Pandas, Seaborn, Scikit-Learn та Clustergram")

# Створення вкладок для кожної лабораторної роботи
tab9, tab10, tab11, tab12 = st.tabs([
    "⚖️ Лаб №9: Адвокатська контора",
    "🌳 Лаб №10: Паркова архітектура",
    "🚢 Лаб №11: Titanic та акції Apple",
    "💎 Лаб №12: Кластеризація (Clustergram)"
])

# ==============================================================================
# ЛАБОРАТОРНА РОБОТА №9
# ==============================================================================
with tab9:
    st.header("Лабораторна робота №9. Розрахунок заробітної плати адвокатів")
    st.markdown(
        "**Завдання (варіант 12):** Побудувати Series та DataFrame для розрахунку місячної заробітної плати "
        "8 працівників адвокатської контори з урахуванням вартості послуг по категоріях, кількості справ "
        "та персональної надбавки."
    )

    col_settings, col_data = st.columns([1, 2])

    with col_settings:
        st.subheader("⚙️ Налаштування тарифів (Series)")
        t_civil = st.number_input("Цивільне право (грн)", value=8000, step=500)
        t_crim = st.number_input("Кримінальне право (грн)", value=15000, step=500)
        t_comm = st.number_input("Господарське право (грн)", value=12000, step=500)
        t_fam = st.number_input("Сімейне право (грн)", value=6000, step=500)

    tariffs = pd.Series(
        {
            "Цивільне право": t_civil,
            "Кримінальне право": t_crim,
            "Господарське право": t_comm,
            "Сімейне право": t_fam
        },
        name="Тариф_за_справу"
    )

    df_lawyers = pd.DataFrame({
        "Працівник": [
            "Коваль О. В.", "Мельник Т. І.", "Шевченко Д. М.", "Бондаренко С. О.",
            "Бойко І. В.", "Ткаченко В. М.", "Кравченко А. П.", "Олійник Н. С."
        ],
        "Категорія": [
            "Цивільне право", "Кримінальне право", "Господарське право", "Сімейне право",
            "Кримінальне право", "Цивільне право", "Господарське право", "Сімейне право"
        ],
        "Кількість_справ": [5, 3, 4, 6, 2, 4, 3, 5],
        "Персональна_надбавка": [3500, 5000, 4200, 2500, 4500, 3000, 4000, 2000]
    })

    with col_data:
        st.subheader("📝 Редагування даних працівників")
        df_lawyers = st.data_editor(df_lawyers, num_rows="fixed", use_container_width=True)

    # Розрахунки
    df_lawyers["Вартість_послуги"] = df_lawyers["Категорія"].map(tariffs)
    df_lawyers["Місячний_дохід"] = (
        df_lawyers["Кількість_справ"] * df_lawyers["Вартість_послуги"]
        + df_lawyers["Персональна_надбавка"]
    )

    max_income = df_lawyers["Місячний_дохід"].max()
    min_income = df_lawyers["Місячний_дохід"].min()
    max_lawyer = df_lawyers.loc[df_lawyers["Місячний_дохід"] == max_income, "Працівник"].values[0]
    min_lawyer = df_lawyers.loc[df_lawyers["Місячний_дохід"] == min_income, "Працівник"].values[0]
    total_payout = df_lawyers["Місячний_дохід"].sum()

    mean_income_stat = statistics.mean(df_lawyers["Місячний_дохід"])
    median_income_stat = statistics.median(df_lawyers["Місячний_дохід"])
    stdev_income_stat = statistics.stdev(df_lawyers["Місячний_дохід"])

    st.divider()
    st.subheader("📈 Підсумкові показники та статистика (statistics)")

    m1, m2, m3 = st.columns(3)
    m1.metric("Найбільший дохід", f"{max_income:,.2f} грн", f"Працівник: {max_lawyer}")
    m2.metric("Найменший дохід", f"{min_income:,.2f} грн", f"Працівник: {min_lawyer}", delta_color="inverse")
    m3.metric("Сумарна величина виплат", f"{total_payout:,.2f} грн")

    s1, s2, s3 = st.columns(3)
    s1.metric("Середній дохід (mean)", f"{mean_income_stat:,.2f} грн")
    s2.metric("Медіана виплат (median)", f"{median_income_stat:,.2f} грн")
    s3.metric("Стандартне відхилення (stdev)", f"{stdev_income_stat:,.2f} грн")

    st.subheader("📋 Підсумкова відомість")
    st.dataframe(df_lawyers, use_container_width=True)


# ==============================================================================
# ЛАБОРАТОРНА РОБОТА №10
# ==============================================================================
with tab10:
    st.header("Лабораторна робота №10. Аналіз даних фірми паркової архітектури (Excel)")
    st.markdown(
        "**Завдання (варіант 12):** Імпортувати таблицю MS Excel у Python, визначити найбільшу та найменшу "
        "вартість робіт, середню величину оплати та побудувати діаграму оплати."
    )

    uploaded_excel = st.file_uploader("Завантажте файл IZADLAB10.xlsx (або використайте вбудований)", type=["xlsx"])

    if uploaded_excel is not None:
        df_park = pd.read_excel(uploaded_excel)
    elif os.path.exists("IZADLAB10.xlsx"):
        df_park = pd.read_excel("IZADLAB10.xlsx")
    else:
        st.info("Файл `IZADLAB10.xlsx` не знайдено у репозиторії — завантажено демонстраційну таблицю за умовою варіанту 12.")
        df_park = pd.DataFrame({
            "Працівник": [
                "Мельник І. П.", "Коваленко О. С.", "Бондар В. М.", "Ткачук А. В.",
                "Савченко Д. О.", "Руденко М. І.", "Мороз С. П.", "Лисенко К. В."
            ],
            "Базова_вартість_робіт": [14500, 18200, 12000, 21000, 16800, 13400, 19500, 15200],
            "Доїзд_грн": [1200, 1500, 900, 1800, 1100, 1000, 1600, 1300],
            "Надбавка_складні_умови": [2500, 3200, 1800, 4000, 2900, 2100, 3500, 2400]
        })
        df_park["Загальна_оплата"] = (
            df_park["Базова_вартість_робіт"] + df_park["Доїзд_грн"] + df_park["Надбавка_складні_умови"]
        )

    st.subheader("📋 Таблиця розрахунку оплати послуг")
    st.dataframe(df_park, use_container_width=True)

    # Обчислення
    max_base_cost = df_park["Базова_вартість_робіт"].max()
    min_base_cost = df_park["Базова_вартість_робіт"].min()
    worker_max_base = df_park.loc[df_park["Базова_вартість_робіт"] == max_base_cost, "Працівник"].values[0]
    worker_min_base = df_park.loc[df_park["Базова_вартість_робіт"] == min_base_cost, "Працівник"].values[0]

    max_total_pay = df_park["Загальна_оплата"].max()
    min_total_pay = df_park["Загальна_оплата"].min()
    mean_total_pay = df_park["Загальна_оплата"].mean()
    total_payout_sum = df_park["Загальна_оплата"].sum()
    worker_max_pay = df_park.loc[df_park["Загальна_оплата"] == max_total_pay, "Працівник"].values[0]
    worker_min_pay = df_park.loc[df_park["Загальна_оплата"] == min_total_pay, "Працівник"].values[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Макс. базова вартість", f"{max_base_cost:,.2f} грн", worker_max_base)
    c2.metric("Мін. базова вартість", f"{min_base_cost:,.2f} грн", worker_min_base, delta_color="inverse")
    c3.metric("Середня загальна оплата", f"{mean_total_pay:,.2f} грн")
    c4.metric("Сумарний фонд оплати", f"{total_payout_sum:,.2f} грн")

    st.caption(
        f"Підсумкова оплата з урахуванням умов: найбільша — **{max_total_pay:,.2f} грн** ({worker_max_pay}), "
        f"найменша — **{min_total_pay:,.2f} грн** ({worker_min_pay})."
    )

    # Графік
    bar_color = st.color_picker("Оберіть колір стовпців діаграми", "#2e7d32")
    fig10, ax10 = plt.subplots(figsize=(11, 5))
    bars = ax10.bar(
        df_park["Працівник"],
        df_park["Загальна_оплата"],
        color=bar_color,
        edgecolor="black",
        alpha=0.85,
        width=0.55,
        label="Підсумкова оплата працівника"
    )
    ax10.axhline(
        mean_total_pay,
        color="#d32f2f",
        linestyle="--",
        linewidth=2,
        label=f"Середня оплата ({mean_total_pay:,.2f} грн)"
    )
    for bar in bars:
        height = bar.get_height()
        ax10.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + (max_total_pay * 0.02),
            f"{int(height):,} грн".replace(",", " "),
            ha="center", va="bottom", fontsize=9, fontweight="bold"
        )
    ax10.set_title("Діаграма оплати послуг працівників фірми паркової архітектури", fontsize=13, pad=12)
    ax10.set_xlabel("Працівники")
    ax10.set_ylabel("Розмір оплати (грн)")
    plt.xticks(rotation=25, ha="right")
    ax10.set_ylim(0, max_total_pay * 1.18)
    ax10.grid(axis="y", linestyle=":", alpha=0.7)
    ax10.legend(loc="upper right")
    plt.tight_layout()
    st.pyplot(fig10)


# ==============================================================================
# ЛАБОРАТОРНА РОБОТА №11
# ==============================================================================
with tab11:
    st.header("Лабораторна робота №11. Аналіз наборів даних Titanic та акцій Apple")

    subtab_titanic, subtab_apple = st.tabs(["🚢 Частина 1: Titanic", "🍏 Частина 2: Акції Apple"])

    # --- TITANIC ---
    with subtab_titanic:
        up_titanic = st.file_uploader("Завантажте titanic.csv (або використається стандартний датасет)", type=["csv"])
        if up_titanic is not None:
            titanic = pd.read_csv(up_titanic)
        elif os.path.exists("titanic.csv"):
            titanic = pd.read_csv("titanic.csv")
        else:
            titanic = sns.load_dataset("titanic")

        with st.expander("Переглянути перші 10 записів таблиці Titanic"):
            st.dataframe(titanic.head(10), use_container_width=True)

        survived_by_sex = (
            titanic.groupby(['sex', 'survived'])['age']
            .count()
            .reset_index()
            .rename(columns={'age': 'Кількість'})
        )
        survived_by_sex['Стан'] = survived_by_sex['survived'].map({0: 'Загинули', 1: 'Вижили'})
        survived_by_sex['Стать'] = survived_by_sex['sex'].map({'female': 'Жінки', 'male': 'Чоловіки'})

        passengers_by_class_sex = (
            titanic.groupby(['pclass', 'sex'])['age']
            .count()
            .reset_index()
            .rename(columns={'age': 'Кількість_пасажирів'})
        )
        passengers_by_class_sex['Клас'] = passengers_by_class_sex['pclass'].astype(str) + "-й клас"
        passengers_by_class_sex['Стать'] = passengers_by_class_sex['sex'].map({'female': 'Жінки', 'male': 'Чоловіки'})

        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.subheader("1. Виживання за статтю")
            st.dataframe(survived_by_sex[['Стать', 'Стан', 'Кількість']], use_container_width=True)
        with col_t2:
            st.subheader("2. Пасажири за класами та статтю")
            st.dataframe(passengers_by_class_sex[['Клас', 'Стать', 'Кількість_пасажирів']], use_container_width=True)

        fig11_1, axes = plt.subplots(1, 2, figsize=(14, 5))
        sns.barplot(
            data=survived_by_sex, x='Стать', y='Кількість', hue='Стан',
            palette={'Вижили': '#2ca02c', 'Загинули': '#d62728'}, ax=axes[0]
        )
        axes[0].set_title("Кількість вцілілих та загиблих за статтю")
        axes[0].set_ylabel("Кількість людей")

        sns.barplot(
            data=titanic, x='pclass', y='survived', hue='sex',
            palette='Blues_d', errorbar=None, ax=axes[1]
        )
        axes[1].set_title("Частка вцілілих за класом корабля та статтю")
        axes[1].set_xlabel("Клас квитка (pclass)")
        axes[1].set_ylabel("Частка вижилих (0–1)")
        axes[1].set_xticklabels(['1-й клас', '2-й клас', '3-й клас'])
        plt.tight_layout()
        st.pyplot(fig11_1)

    # --- APPLE ---
    with subtab_apple:
        up_apple = st.file_uploader("Завантажте apple.csv (обов'язково для реальних біржових даних)", type=["csv"])
        if up_apple is not None:
            apple = pd.read_csv(up_apple)
        elif os.path.exists("apple.csv"):
            apple = pd.read_csv("apple.csv")
        else:
            st.warning("Файл `apple.csv` не завантажено. Згенеровано синтетичний часовий ряд за 2012–2018 рр. для демонстрації.")
            dates = pd.date_range("2012-01-01", "2018-12-31", freq="B")
            np.random.seed(42)
            base_price = np.linspace(65, 175, len(dates)) + np.random.normal(0, 8, len(dates))
            apple = pd.DataFrame({
                "Date": dates,
                "Open": np.round(base_price, 2),
                "Close": np.round(base_price + np.random.normal(0, 1.5, len(dates)), 2)
            })

        apple['Date'] = pd.to_datetime(apple['Date'])
        apple['Year'] = apple['Date'].dt.year

        apple_weekly_close = (
            apple.resample('W-Mon', on='Date')['Close']
            .mean()
            .reset_index()
            .rename(columns={'Close': 'Середня_ціна_тижня_Close'})
        )

        threshold = st.slider("Поріг ціни відкриття (Open, $)", min_value=80.0, max_value=150.0, value=110.2, step=0.1)
        years_above = sorted(apple[apple['Open'] > threshold]['Year'].unique())

        st.success(f"**Роки, в яких торги починалися з ціни Open > {threshold}$:** {', '.join(map(str, years_above)) if years_above else 'Не знайдено'}")

        with st.expander("3. Середня ціна закриття ('Close') за тиждень (перші 15 тижнів)"):
            st.dataframe(apple_weekly_close.head(15), use_container_width=True)

        year_range = st.slider("Діапазон років для графіка", int(apple['Year'].min()), int(apple['Year'].max()), (2015, 2018))
        apple_filtered = apple[(apple['Year'] >= year_range[0]) & (apple['Year'] <= year_range[1])].sort_values('Date')

        fig11_2, ax11_2 = plt.subplots(figsize=(13, 5))
        sns.lineplot(
            data=apple_filtered, x='Date', y='Open',
            color='#1f77b4', linewidth=1.8, label="Ціна відкриття (Open, $)", ax=ax11_2
        )
        ax11_2.axhline(threshold, color='#d62728', linestyle='--', linewidth=1.5, label=f"Поріг ціни: {threshold} $")
        ax11_2.set_title(f"Динаміка вартості акцій Apple при відкритті торгів у {year_range[0]}–{year_range[1]} рр.")
        ax11_2.set_xlabel("Дата торгів")
        ax11_2.set_ylabel("Ціна відкриття ($)")
        ax11_2.legend(loc="upper left")
        plt.tight_layout()
        st.pyplot(fig11_2)


# ==============================================================================
# ЛАБОРАТОРНА РОБОТА №12
# ==============================================================================
with tab12:
    st.header("Лабораторна робота №12. Візуалізація кластерного аналізу (Clustergram)")
    st.markdown(
        "**Індивідуальне завдання:** Кластерний аналіз бази даних `diamonds` із використанням пакету `clustergram` "
        "(алгоритми **K-Means** та **Gaussian Mixture Model**), оцінка Silhouette і Calinski-Harabasz та проєкція PCA."
    )

    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        sample_size = st.slider("Розмір вибірки diamonds", 500, 5000, 2000, step=500)
    with col_p2:
        max_k = st.slider("Максимальна кількість кластерів (k)", 4, 10, 8)
    with col_p3:
        selected_k = st.slider("Обране k для профілю та PCA", 2, max_k, 3)

    @st.cache_data
    def load_and_scale_diamonds(n_samples):
        diamonds = sns.load_dataset("diamonds")
        sample = diamonds.sample(n=n_samples, random_state=42).reset_index(drop=True)
        features = ['carat', 'depth', 'table', 'price', 'x', 'y', 'z']
        X_raw = sample[features].dropna()
        X_raw = X_raw[(X_raw['x'] > 0) & (X_raw['y'] > 0) & (X_raw['z'] > 0)]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X_raw)
        return X_raw, X_scaled

    X_raw, X_scaled = load_and_scale_diamonds(sample_size)

    with st.spinner("Обчислення кластерограм K-Means та GMM..."):
        cgram_kmeans = Clustergram(range(1, max_k + 1), n_init=30, random_state=42)
        cgram_kmeans.fit(X_scaled)

        cgram_gmm = Clustergram(range(1, max_k + 1), method="gmm", n_init=5, random_state=42)
        cgram_gmm.fit(X_scaled)

    # Кластерограми поруч
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        st.subheader("1. Кластерограма K-Means")
        fig12_1, ax12_1 = plt.subplots(figsize=(8, 6))
        cgram_kmeans.plot(
            ax=ax12_1,
            line_style=dict(color="#1f77b4", alpha=0.6),
            cluster_style=dict(color="#d9534f", s=70)
        )
        ax12_1.set_title("K-Means (k-середніх)")
        ax12_1.set_xlabel("Кількість кластерів (k)")
        ax12_1.set_ylabel("PCA-зважене середнє")
        ax12_1.yaxis.grid(False)
        sns.despine(offset=10)
        plt.tight_layout()
        st.pyplot(fig12_1)

    with g_col2:
        st.subheader("2. Кластерограма GMM")
        fig12_2, ax12_2 = plt.subplots(figsize=(8, 6))
        cgram_gmm.plot(
            ax=ax12_2,
            line_style=dict(color="#2ca02c", alpha=0.6),
            cluster_style=dict(color="#9467bd", s=70)
        )
        ax12_2.set_title("Gaussian Mixture Model (GMM)")
        ax12_2.set_xlabel("Кількість кластерів (k)")
        ax12_2.set_ylabel("PCA-зважене середнє")
        ax12_2.yaxis.grid(False)
        sns.despine(offset=10)
        plt.tight_layout()
        st.pyplot(fig12_2)

    # Метрики якості та PCA
    st.divider()
    m_col1, m_col2 = st.columns(2)

    with m_col1:
        st.subheader("3. Метрики якості кластеризації")
        fig12_3, axs = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
        cgram_kmeans.silhouette_score().plot(
            xlabel="Кількість кластерів (k)", ylabel="Silhouette score",
            color="#2ca02c", linewidth=2, marker="o", ax=axs[0]
        )
        axs[0].set_title("Оцінка силуету (Silhouette Score)")

        cgram_kmeans.calinski_harabasz_score().plot(
            xlabel="Кількість кластерів (k)", ylabel="Calinski-Harabasz",
            color="#ff7f0e", linewidth=2, marker="s", ax=axs[1]
        )
        axs[1].set_title("Оцінка Калінського-Харабаша")
        sns.despine(offset=10)
        plt.tight_layout()
        st.pyplot(fig12_3)

    with m_col2:
        st.subheader(f"4. Проєкція кластерів у простір PCA (k = {selected_k})")
        labels_k = cgram_kmeans.labels[selected_k]
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)

        fig12_4, ax12_4 = plt.subplots(figsize=(8, 6))
        sns.scatterplot(
            x=X_pca[:, 0], y=X_pca[:, 1], hue=labels_k,
            palette="Set1", alpha=0.75, s=40, ax=ax12_4
        )
        ax12_4.set_title(f"Розподіл кластерів діамантів у просторі PCA (k = {selected_k})")
        ax12_4.set_xlabel("Перша головна компонента (PCA 1)")
        ax12_4.set_ylabel("Друга головна компонента (PCA 2)")
        ax12_4.legend(title="Кластер")
        plt.tight_layout()
        st.pyplot(fig12_4)

    # Характеристика кластерів
    st.subheader(f"📋 Характеристика кластерів діамантів при k = {selected_k}")
    X_raw_clustered = X_raw.copy()
    X_raw_clustered['Кластер'] = labels_k
    cluster_profile = X_raw_clustered.groupby('Кластер').agg(
        Кількість=('carat', 'count'),
        Середня_вага_carat=('carat', 'mean'),
        Середня_ціна_USD=('price', 'mean'),
        Середня_довжина_x=('x', 'mean'),
        Середній_майданчик_table=('table', 'mean')
    ).round(2)
    st.dataframe(cluster_profile, use_container_width=True)
