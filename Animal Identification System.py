import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # pip install pillow

class AnimalExpertSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("🐾 Animal Identifier")
        self.root.geometry("600x450")
        self.root.configure(bg="#f0f8ff")

        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 12), padding=6)
        style.configure("TLabel", font=("Segoe UI", 12), background="#f0f8ff")

        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.reset()

    def reset(self):
        self.known = {}
        self.current_trait = None
        self.answers_log = []

        self.traits = {
            "has_fur": "have fur",
            "has_feathers": "have feathers",
            "has_scales": "have scales",
            "has_smooth_skin": "have smooth skin",
            "lives_in_water": "live in water",
            "lays_eggs": "lay eggs",
            "cold_blooded": "have cold blood",
            "eats_meat": "eat meat",
            "eats_plants": "eat plants",
            "has_mane": "have a mane",
            "has_trunk": "have a trunk",
            "has_sharp_teeth": "have sharp teeth",
            "can_fly": "fly",
            "cannot_fly": "not fly",
            "can_jump": "jump",
            "barks": "bark",
            "meows": "meow",
            "gives_milk": "give milk",
            "can_cluck": "cluck",
            "has_shell": "have a shell",
            "moves_slow": "move slowly",
            "no_legs": "have no legs",
            "slithers": "slither"
        }

        self.rules = [
            ("lion",     lambda: self.verify("has_fur") and self.verify("eats_meat") and self.verify("has_mane")),
            ("elephant", lambda: self.verify("has_fur") and self.verify("eats_plants") and self.verify("has_trunk")),
            ("shark",    lambda: self.verify("has_scales") and self.verify("lives_in_water") and self.verify("eats_meat") and self.verify("has_sharp_teeth")),
            ("eagle",    lambda: self.verify("has_feathers") and self.verify("eats_meat") and self.verify("can_fly")),
            ("penguin",  lambda: self.verify("has_feathers") and self.verify("eats_meat") and self.verify("cannot_fly")),
            ("frog",     lambda: self.verify("has_smooth_skin") and self.verify("lives_in_water") and self.verify("can_jump")),
            ("dog",      lambda: self.verify("has_fur") and self.verify("eats_meat") and self.verify("barks")),
            ("cat",      lambda: self.verify("has_fur") and self.verify("eats_meat") and self.verify("meows")),
            ("cow",      lambda: self.verify("has_fur") and self.verify("eats_plants") and self.verify("gives_milk")),
            ("chicken",  lambda: self.verify("has_feathers") and self.verify("can_cluck") and self.verify("cannot_fly")),
            ("turtle",   lambda: self.verify("has_scales") and self.verify("eats_plants") and self.verify("has_shell") and self.verify("moves_slow")),
            ("snake",    lambda: self.verify("has_scales") and self.verify("eats_meat") and self.verify("no_legs") and self.verify("slithers"))
        ]

        self.question_index = 0
        self.total_questions = len(self.traits)
        self.ask_next_question()

    def verify(self, trait):
        if trait in self.known:
            return self.known[trait]
        else:
            self.ask_question(trait)
            return None

    def ask_question(self, trait):
        self.clear_screen()
        self.current_trait = trait

        # Question counter
        self.question_index += 1
        counter_label = ttk.Label(self.root, text=f"Question {self.question_index} of {self.total_questions}")
        counter_label.pack(pady=5)

        question = f"Does the animal {self.traits[trait]}?"
        label = ttk.Label(self.root, text=question, font=("Segoe UI", 16, "bold"), wraplength=500)
        label.pack(pady=20)

        yes_btn = ttk.Button(self.root, text="✅ Yes", command=lambda: self.record_answer(True))
        no_btn = ttk.Button(self.root, text="❌ No", command=lambda: self.record_answer(False))
        yes_btn.pack(pady=5)
        no_btn.pack(pady=5)

    def record_answer(self, answer):
        self.known[self.current_trait] = answer
        ans_text = "Yes" if answer else "No"
        self.answers_log.append(f"{self.traits[self.current_trait]} → {ans_text}")
        self.ask_next_question()

    def ask_next_question(self):
        for name, rule in self.rules:
            result = rule()
            if result is None:
                return
            elif result:
                self.show_result(name)
                return

        if all(trait in self.known for trait in self.traits):
            self.show_result(None)

    def show_result(self, animal):
        self.clear_screen()

        if animal:
            msg = f"🎉 I think your animal is a {animal.upper()}!"
            label = tk.Label(self.root, text=msg, font=("Segoe UI", 18, "bold"), fg="green", bg="#f0fff0")
            label.pack(pady=20)

            # Try to load image if available
            try:
                img = Image.open(f"images/{animal}.png").resize((200, 200))
                photo = ImageTk.PhotoImage(img)
                img_label = tk.Label(self.root, image=photo, bg="#f0fff0")
                img_label.image = photo
                img_label.pack(pady=10)
            except:
                pass
        else:
            label = tk.Label(self.root, text="❌ Sorry, I could not identify your animal.",
                             font=("Segoe UI", 16), fg="red", bg="#f0fff0")
            label.pack(pady=20)

        # Show answers history
        history_label = tk.Label(self.root, text="Your Answers:", font=("Segoe UI", 12, "bold"), bg="#f0fff0")
        history_label.pack(pady=5)
        for ans in self.answers_log:
            tk.Label(self.root, text=ans, bg="#f0fff0").pack()

        ttk.Button(self.root, text="🔄 Try Again", command=self.reset).pack(pady=10)
        ttk.Button(self.root, text="🚪 Exit", command=self.root.quit).pack(pady=5)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_about(self):
        messagebox.showinfo("About", "Animal Identification Expert System\n"
                                     "Created by Muzamil Munir (FA22-BSE-111)\n"
                                     "Uses Rule-Based Reasoning with Tkinter UI.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimalExpertSystem(root)
    root.mainloop()
