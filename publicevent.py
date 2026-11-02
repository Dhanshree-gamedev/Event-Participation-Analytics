
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ---------------- DATA GENERATION ----------------

def load_data():

    np.random.seed(10)

    event_names = [
        "Music Festival",
        "Tech Conference",
        "Food Festival",
        "Sports Event",
        "Book Fair",
        "Cultural Fest",
        "Science Exhibition",
        "Art Exhibition",
        "Health Camp",
        "Career Fair",
        "Dance Competition",
        "Workshop"
    ]

    categories = [
        "Entertainment", "Technology", "Food",
        "Sports", "Education", "Cultural",
        "Education", "Cultural", "Health",
        "Education", "Entertainment", "Technology"
    ]

    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    registered = np.random.randint(100, 500, 12)

    attended = np.array([
        int(r * np.random.uniform(0.60, 0.95))
        for r in registered
    ])

    data = {
        "Event": event_names,
        "Category": categories,
        "Month": months,
        "Registered": registered,
        "Attended": attended
    }

    df = pd.DataFrame(data)

    return df


df = load_data()


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Public Event Participation Analytics")
root.geometry("1200x750")
root.config(bg="#edf2f7")


# ---------------- SUMMARY FUNCTION ----------------

def calculate_summary():

    total_events = len(df)

    total_registered = df["Registered"].sum()

    total_attended = df["Attended"].sum()

    attendance_rate = (
        total_attended / total_registered
    ) * 100

    return (
        total_events,
        total_registered,
        total_attended,
        attendance_rate
    )


# ---------------- DASHBOARD CARDS ----------------

def create_card(parent, title, value, color, column):

    card = tk.Frame(
        parent,
        bg="white",
        width=250,
        height=110,
        highlightbackground="#dbe3ef",
        highlightthickness=1
    )

    card.grid(
        row=0,
        column=column,
        padx=12,
        pady=15
    )

    card.pack_propagate(False)

    tk.Label(
        card,
        text=title,
        font=("Arial", 11, "bold"),
        bg="white",
        fg="#64748b"
    ).pack(pady=(18, 5))

    tk.Label(
        card,
        text=value,
        font=("Arial", 23, "bold"),
        bg="white",
        fg=color
    ).pack()


def show_summary():

    total_events, registered, attended, rate = calculate_summary()

    create_card(
        card_frame,
        "TOTAL EVENTS",
        str(total_events),
        "#2563eb",
        0
    )

    create_card(
        card_frame,
        "REGISTERED PARTICIPANTS",
        str(registered),
        "#7c3aed",
        1
    )

    create_card(
        card_frame,
        "TOTAL ATTENDED",
        str(attended),
        "#16a34a",
        2
    )

    create_card(
        card_frame,
        "ATTENDANCE RATE",
        str(round(rate, 2)) + "%",
        "#ea580c",
        3
    )


# ---------------- GRAPH FUNCTION ----------------

def show_graph():

    global canvas

    if canvas is not None:
        canvas.get_tk_widget().destroy()

    fig, axes = plt.subplots(1, 3, figsize=(13, 4))

    fig.suptitle(
        "Public Event Participation Analysis",
        fontsize=15,
        fontweight="bold"
    )

    # 1. Event-wise participation

    axes[0].bar(
        df["Event"],
        df["Attended"],
        color="skyblue"
    )

    axes[0].set_title("Event-wise Attendance")
    axes[0].set_ylabel("Participants")
    axes[0].tick_params(axis="x", rotation=90, labelsize=7)

    # 2. Category-wise participation

    category_data = df.groupby("Category")["Attended"].sum()

    axes[1].pie(
        category_data,
        labels=category_data.index,
        autopct="%1.1f%%",
        startangle=90
    )

    axes[1].set_title("Category-wise Participation")

    # 3. Monthly participation trend

    monthly_data = df.groupby("Month")["Attended"].sum()

    axes[2].plot(
        monthly_data.index,
        monthly_data.values,
        marker="o",
        linewidth=2
    )

    axes[2].set_title("Monthly Participation Trend")
    axes[2].set_ylabel("Participants")
    axes[2].tick_params(axis="x", rotation=90, labelsize=7)
    axes[2].grid(True)

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )

    plt.close(fig)


# ---------------- TABLE FUNCTION ----------------

def show_table():

    for item in table.get_children():
        table.delete(item)

    for index, row in df.iterrows():

        rate = (
            row["Attended"] / row["Registered"]
        ) * 100

        table.insert(
            "",
            "end",
            values=(
                row["Event"],
                row["Category"],
                row["Registered"],
                row["Attended"],
                str(round(rate, 2)) + "%"
            )
        )


# ---------------- REFRESH FUNCTION ----------------

def refresh_dashboard():

    global df

    df = load_data()

    for widget in card_frame.winfo_children():
        widget.destroy()

    show_summary()
    show_table()
    show_graph()

    messagebox.showinfo(
        "Dashboard",
        "Dashboard refreshed successfully!"
    )


# ---------------- HEADER ----------------

header = tk.Frame(
    root,
    bg="#172554",
    height=90
)

header.pack(fill="x")

tk.Label(
    header,
    text="PUBLIC EVENT PARTICIPATION ANALYTICS",
    font=("Arial", 22, "bold"),
    bg="#172554",
    fg="white"
).pack(pady=(15, 5))

tk.Label(
    header,
    text="Event Statistics and Participation Monitoring System",
    font=("Arial", 10),
    bg="#172554",
    fg="#bfdbfe"
).pack()


# ---------------- SUMMARY SECTION ----------------

tk.Label(
    root,
    text="Dashboard Overview",
    font=("Arial", 18, "bold"),
    bg="#edf2f7",
    fg="#172554"
).pack(anchor="w", padx=25, pady=(15, 0))


card_frame = tk.Frame(
    root,
    bg="#edf2f7"
)

card_frame.pack()

canvas = None


# ---------------- GRAPH SECTION ----------------

graph_frame = tk.Frame(
    root,
    bg="white",
    highlightbackground="#dbe3ef",
    highlightthickness=1
)

graph_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=10
)


# ---------------- TABLE SECTION ----------------

tk.Label(
    root,
    text="Event Participation Details",
    font=("Arial", 15, "bold"),
    bg="#edf2f7",
    fg="#172554"
).pack(anchor="w", padx=25, pady=5)


table_frame = tk.Frame(root, bg="white")

table_frame.pack(
    fill="x",
    padx=25,
    pady=5
)

columns = (
    "Event",
    "Category",
    "Registered",
    "Attended",
    "Attendance Rate"
)

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=4
)

for col in columns:

    table.heading(col, text=col)

    table.column(
        col,
        width=200,
        anchor="center"
    )

table.pack(fill="x")


# ---------------- BUTTON SECTION ----------------

button_frame = tk.Frame(
    root,
    bg="#edf2f7"
)

button_frame.pack(pady=12)

tk.Button(
    button_frame,
    text="Refresh Dashboard",
    font=("Arial", 11, "bold"),
    bg="#2563eb",
    fg="white",
    relief="flat",
    width=20,
    command=refresh_dashboard
).pack(side="left", padx=10)


tk.Button(
    button_frame,
    text="Exit",
    font=("Arial", 11, "bold"),
    bg="#dc2626",
    fg="white",
    relief="flat",
    width=12,
    command=root.destroy
).pack(side="left", padx=10)


# ---------------- RUN DASHBOARD ----------------

show_summary()
show_table()
show_graph()

root.mainloop()
