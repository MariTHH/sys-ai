from pyswip import Prolog
from pyswip.prolog import PrologError


class KnowledgeBaseInteractor:
    def __init__(self, path_to_base):
        self.prolog = Prolog()
        try:
            self.prolog.consult(path_to_base)
        except PrologError:
            print(f"Could not read knowledge base by path: {path_to_base}.")
            exit(22)

    def get_available_roles(self):
        request = "role(Role)."
        available_roles = self.prolog.query(request)
        return [role["Role"] for role in available_roles]

    def get_available_factions(self):
        request = "has_faction(_, Faction)."
        available_factions = self.prolog.query(request)
        return list(set([faction["Faction"] for faction in available_factions]))

    def get_available_heroes(self):
        request = "hero(Hero)."
        available_heroes = self.prolog.query(request)
        return [hero["Hero"] for hero in available_heroes]

    def get_heroes_by_role(self, role):
        query = f"has_role(Hero, {role})."
        return [hero["Hero"] for hero in self.prolog.query(query)]

    def get_heroes_by_faction(self, faction):
        query = f"has_faction(Hero, {faction})."
        return [hero["Hero"] for hero in self.prolog.query(query)]

    def get_allies(self, hero):
        query = f"is_ally({hero}, Ally)."
        return [ally["Ally"] for ally in self.prolog.query(query)]

    def get_enemies(self, hero):
        query = f"is_enemy({hero}, Enemy)."
        return [enemy["Enemy"] for enemy in self.prolog.query(query)]

    def get_heroes_by_enemy(self, enemy):
        query = f"is_enemy(Hero, {enemy})."
        return [hero["Hero"] for hero in self.prolog.query(query)]

    def recommend_heroes(self, roles=None, factions=None, allies=None, enemies=None):
        heroes = self.get_available_heroes()

        if roles:
            role_heroes = []
            for role in roles:
                role_heroes += self.get_heroes_by_role(role)
            heroes = list(set(heroes) & set(role_heroes))

        if factions:
            faction_heroes = []
            for faction in factions:
                faction_heroes += self.get_heroes_by_faction(faction)
            heroes = list(set(heroes) & set(faction_heroes))

        if allies:
            ally_heroes = []
            for ally in allies:
                ally_heroes += self.get_allies(ally)
            heroes = list(set(heroes) & set(ally_heroes))

        if enemies:
            enemy_heroes = []
            for enemy in enemies:
                enemy_heroes += self.get_heroes_by_enemy(enemy)
            heroes = list(set(heroes) & set(enemy_heroes))

        return heroes


class UserInteractor:
    def __init__(self, knowledge_base_interactor):
        self.kb_interactor = knowledge_base_interactor

    def learn_user_roles(self):
        available_roles = self.kb_interactor.get_available_roles()
        print("Available roles:", ", ".join(available_roles))
        roles_input = input("Please enter your preferred roles (comma separated): ").lower().split(',')
        chosen_roles = [role.strip() for role in roles_input if role.strip() in available_roles]

        if chosen_roles:
            print(f"Great, you chose these roles: {', '.join(chosen_roles)}.")
        else:
            print("Apparently role doesn't matter to you.")

        return chosen_roles

    def learn_user_factions(self):
        available_factions = self.kb_interactor.get_available_factions()
        print("Available factions:", ", ".join(available_factions))
        factions_input = input(
            "Please enter your preferred factions (comma separated or press Enter if none): ").lower().split(',')
        if not factions_input or factions_input == ['']:
            print("Apparently faction doesn't matter to you.")
            return None
        chosen_factions = [faction.strip() for faction in factions_input if faction.strip() in available_factions]

        if chosen_factions:
            print(f"Great, you chose these factions: {', '.join(chosen_factions)}.")
        else:
            print("Apparently faction doesn't matter to you.")

        return chosen_factions

    def learn_user_allies(self):
        available_heroes = self.kb_interactor.get_available_heroes()
        print("Available heroes for allies:", ", ".join(available_heroes))
        allies_input = input(
            "Please enter your preferred allies (comma separated or press Enter if none): ").lower().split(',')
        if not allies_input or allies_input == ['']:
            print("Apparently allies don't matter to you.")
            return None
        chosen_allies = [ally.strip() for ally in allies_input if ally.strip() in available_heroes]

        if chosen_allies:
            print(f"Great, you chose these allies: {', '.join(chosen_allies)}.")
        else:
            print("Apparently allies don't matter to you.")

        return chosen_allies

    def learn_user_enemies(self):
        available_heroes = self.kb_interactor.get_available_heroes()
        print("Available heroes for enemies:", ", ".join(available_heroes))
        enemies_input = input(
            "Please enter your preferred enemies (comma separated or press Enter if none): ").lower().split(',')
        if not enemies_input or enemies_input == ['']:
            print("Apparently enemies don't matter to you.")
            return None
        chosen_enemies = [enemy.strip() for enemy in enemies_input if enemy.strip() in available_heroes]

        if chosen_enemies:
            print(f"Great, you chose these enemies: {', '.join(chosen_enemies)}.")
        else:
            print("Apparently enemies don't matter to you.")

        return chosen_enemies

    def recommend_heroes(self, roles, factions, allies, enemies):
        heroes = self.kb_interactor.recommend_heroes(roles=roles, factions=factions, allies=allies, enemies=enemies)
        if not heroes:
            print("Sorry, no heroes match your preferences.")
        else:
            print("Recommended heroes:", ", ".join(heroes))

    def check_team_for_conflicts(self, team):
        allies_conflicts = {}
        enemies_conflicts = {}

        for hero in team:
            for ally in self.kb_interactor.get_allies(hero):
                if ally not in team:
                    continue
                if hero not in allies_conflicts:
                    allies_conflicts[hero] = []
                allies_conflicts[hero].append(ally)

            for enemy in self.kb_interactor.get_enemies(hero):
                if enemy in team:
                    if hero not in enemies_conflicts:
                        enemies_conflicts[hero] = []
                    enemies_conflicts[hero].append(enemy)

        return allies_conflicts, enemies_conflicts

    def resolve_enemy_conflicts(self, conflicts):
        enemies_to_remove = set()
        for hero, enemies in conflicts.items():
            for enemy in enemies:
                enemies_to_remove.add(enemy)

        return list(enemies_to_remove)


def main():
    prolog_file_path = 'sysAIlab1.pl'
    prolog_interactor = KnowledgeBaseInteractor(prolog_file_path)
    user_interactor = UserInteractor(prolog_interactor)

    print("Welcome to the Mobile Legends Hero Recommendation System!")

    introduction = input("Tell us a bit about yourself (for example, 'My name is NAME and I need a hero/team'): ")

    if introduction.lower().startswith("my name is ") and (
            "and i need a hero" in introduction.lower() or "and i need a team" in introduction.lower()):
        name = introduction.split(" ")[3]
        preference = "hero" if "and i need a hero" in introduction.lower() else "team"

        print(f"Hello, {name}! Let's proceed to get a recommendation for a {preference}.")
    else:
        print("Please tell us if you want to get a recommendation.")

    while True:
        recommendation_prompt = input("Do you want to get a recommendation? Enter: yes/no: ").lower()
        if recommendation_prompt == '' or recommendation_prompt == 'yes':
            recommendation_prompt = 'yes'
        elif recommendation_prompt == 'no':
            print("Goodbye!")
            return
        else:
            print(
                "Invalid input. Please enter 'yes' or 'no'. If you enter again incorrectly, it will be interpreted as 'no'.")

            recommendation_prompt = input("Do you want to get a recommendation? Enter: yes/no: ").lower()
            if recommendation_prompt == '' or recommendation_prompt == 'yes':
                recommendation_prompt = 'yes'
            elif recommendation_prompt == 'no':
                print("Goodbye!")
                return
            else:
                print("Goodbye!")
                return

        if 'preference' in locals():
            recommendation_type = preference
        else:
            recommendation_type = input(
                "Do you need a recommendation for a HERO or a TEAM? Enter (default: hero): hero/team: ").lower()

        if recommendation_type == '' or recommendation_type == 'hero':
            user_roles = user_interactor.learn_user_roles()
            user_factions = user_interactor.learn_user_factions()
            user_allies = user_interactor.learn_user_allies()
            user_enemies = user_interactor.learn_user_enemies()

            user_interactor.recommend_heroes(user_roles, user_factions, user_allies, user_enemies)

        elif recommendation_type == 'team':
            team_input = input(
                "Who do you already have in your team? List (separated by commas) heroes: ").lower().split(',')
            team = [hero.strip() for hero in team_input if hero.strip()]

            if len(team) == 1:
                single_hero = team[0]
                allies = user_interactor.kb_interactor.get_allies(single_hero)

                if allies:
                    print(f"You have only one hero: {single_hero}. Here are some potential allies:")
                    print(", ".join(allies))
                else:
                    print(f"You have only one hero: {single_hero}. You're alone in the field, warrior.")

            elif team:
                allies_conflicts, enemies_conflicts = user_interactor.check_team_for_conflicts(team)

                if enemies_conflicts:
                    print("Your team has the following enemies among themselves:")
                    for hero, enemies in enemies_conflicts.items():
                        print(f"{hero} is an enemy of {', '.join(enemies)}")
                    enemies_to_remove = user_interactor.resolve_enemy_conflicts(enemies_conflicts)
                    print("Consider removing the following enemies from your team:", ", ".join(enemies_to_remove))

                    removal_input = input(
                        "Select enemies to remove (comma separated, or press Enter to skip): ").lower().split(',')
                    enemies_selected = [enemy.strip() for enemy in removal_input if enemy.strip() in enemies_to_remove]

                    new_team = [hero for hero in team if hero not in enemies_selected]

                    if new_team:
                        print("Your new team:", ", ".join(new_team))
                    else:
                        print("No heroes remain in your team after removing enemies.")
                else:
                    print("Great! No internal conflicts in your team!")

                if not enemies_selected and enemies_conflicts:
                    print("Warning: Your team may not succeed with enemies present.")

            else:
                print("You need to have at least one hero in your team.")

        satisfied = input("Were you satisfied with the recommendations? (yes/no): ").lower()
        if satisfied == '' or satisfied == 'yes':
            print("The system is glad to help you! Looking forward to assisting you again. Goodbye!")
            break
        else:
            print("Let's start over!")


if __name__ == "__main__":
    main()
