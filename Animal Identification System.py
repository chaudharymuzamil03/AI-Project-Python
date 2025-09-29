import tkinter as tk

class AnimalExpertSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Animal Identifier (Python Only)")
        self.root.geometry("500x350")
        self.reset()

    def reset(self):
        self.known = {}
        self.current_trait = None

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
        question = f"Does the animal {self.traits[trait]}?"
        label = tk.Label(self.root, text=question, font=("Arial", 14), wraplength=400)
        label.pack(pady=20)

        yes_btn = tk.Button(self.root, text="Yes", width=12, command=lambda: self.record_answer(True))
        no_btn = tk.Button(self.root, text="No", width=12, command=lambda: self.record_answer(False))
        yes_btn.pack(pady=5)
        no_btn.pack(pady=5)

    def record_answer(self, answer):
        self.known[self.current_trait] = answer
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
            msg = f"I think your animal is a {animal}!"
            label = tk.Label(self.root, text=msg, font=("Arial", 16), fg="green")
        else:
            label = tk.Label(self.root, text="Sorry, I could not identify your animal.", font=("Arial", 14), fg="red")
        label.pack(pady=30)

        restart_btn = tk.Button(self.root, text="Try Again", command=self.reset)
        restart_btn.pack(pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimalExpertSystem(root)
    root.mainloop()
