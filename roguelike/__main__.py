class Character:

    def __init__(self, name='Hero', strength=10, intelligence=10, dexterity=10):
        self.name = name
        self.strength = strength
        self.intelligence = intelligence
        self.dexterity = dexterity
        self.equip = Equipment('limbs', 1, 1, 1, 0)
        self.inventory = {}
        self._event_log = ''

    def character_info(self) -> str:
        dmg = self.equip.compute_damage(self)
        return f"{self.name}\nstr {self.strength}\ndex {self.dexterity}\nint {self.intelligence}\n{self.equip.display_name()} {dmg} dmg"

    def determine_best_equipment(self):
        best_equipment = Equipment('limbs', 1, 1, 1, 0)
        for item in self.inventory.values():
            print(
                f"new item {item.name} {item.compute_damage(self)} :::: best item so far {best_equipment.name} {best_equipment.compute_damage(self)}")
            # TODO: pick the best of equals by first alphabetically
            if item.compute_damage(self) > best_equipment.compute_damage(self):
                print(item.name)
                best_equipment = item
        return best_equipment

    def add_item_to_inventory(self, item):
        if item.name in self.inventory.keys():
            print('enhancing')
            original_item = self.inventory[item.name]
            enhanced_item = Equipment(
                item.name,
                max(item.strength, original_item.strength),
                max(item.dexterity, original_item.dexterity),
                max(item.intellect, original_item.intellect),
                damage_modifier=max(item.damage_modifier, original_item.damage_modifier),
                enhanced=True
            )
            self.inventory[item.name] = enhanced_item
        else:
            self.inventory[item.name] = item

    def handle_new_item(self, formatted_name, *args):
        event_details = f"{self.name} finds '{formatted_name}'\n"
        self._event_log = self._event_log + event_details
        new_item = Equipment(formatted_name, *args)
        self.add_item_to_inventory(new_item)

    def handle_random_event(self, formatted_name, *args):
        event = RandomEvent(formatted_name, *args)
        self._event_log = self._event_log + event.eventify()
        self.partake_in(event)

    def partake_in(self, event):
        self.strength = self.strength + event.str
        self.dexterity = self.dexterity + event.dex
        self.intelligence = self.intelligence + event.int

    def event_log(self):
        return self._event_log

    def format_name(self, name):
        split_name = name.split('_')
        formatted_name = ' '.join(split_name)
        chars = list(formatted_name)
        return chars[0].capitalize() + ''.join(chars[1:])

    def __getattr__(self, name):
        def _missing(*args, **kwargs):
            formatted_name = self.format_name(name)
            if len(args) == 4:
                # this is probably a weapon - lets see if we'll equip it
                self.handle_new_item(formatted_name, *args)
            else:
                # woot! stat enhancer
                self.handle_random_event(formatted_name, *args)

            self.equip = self.determine_best_equipment()

            print("The object was %r, the method was %r. " % (self, name))
            print("It was called with %r and %r as arguments" % (args, kwargs))

        return _missing


class RandomEvent:
    def __init__(self, name, str, dex, int):
        self.name = name
        self.str = str
        self.dex = dex
        self.int = int

    def eventify(self):
        event = f"{self.name}: "
        stat_mods = []
        if self.str != 0:
            stat_mods.append(f"strength {'+' if self.str > 0 else ''}{self.str}")
        if self.dex != 0:
            stat_mods.append(f"dexterity {'+' if self.dex > 0 else ''}{self.dex}")
        if self.int != 0:
            stat_mods.append(f"intelligence {'+' if self.int > 0 else ''}{self.int}")
        event = event + ', '.join(stat_mods)
        return event


class Equipment:
    def __init__(self, name, strength, dexterity, intellect, damage_modifier=0, enhanced=False):
        self.name = name
        self.strength = strength
        self.dexterity = dexterity
        self.intellect = intellect
        self.damage_modifier = damage_modifier
        self.enhanced = enhanced

    def compute_damage(self, character):
        return self.strength * character.strength + self.dexterity * character.dexterity + self.intellect * character.intelligence + self.damage_modifier

    def display_name(self):
        return self.name if not self.enhanced else f"{self.name}(enhanced)"
