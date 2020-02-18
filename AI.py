import random

from model import *
import datetime


class AI:
    def __init__(self):
        self.rows = 0
        self.cols = 0
        self.path_for_my_units = None
        now = datetime.datetime.now().strftime("%d%B%Y-%I%M%p") + str(random.randint(0,10000))
        now = 'log\\' + now
        now = now + '.txt'
        self.f = open(now, "w+")
      #  f = open(now, "w+")

    # this function is called in the beginning for deck picking and pre process
    def pick(self, world):
        self.f.write('player id: ' + str(world.get_me().player_id) + '\n')
        print("pick started!")

        # preprocess
        map = world.get_map()
        self.rows = map.row_num
        self.cols = map.col_num

        # choosing all flying units
        all_base_units = world.base_units
        my_deck = [all_base_units[4], all_base_units[0], all_base_units[2], all_base_units[8], all_base_units[6], all_base_units[3], all_base_units[5], all_base_units[7], all_base_units[1]]#[base_unit for base_unit in all_base_units if not base_unit.is_flying]
        for i in my_deck:
            print(i.type_id)

        # picking the chosen deck - rest of the deck will automatically be filled with random base_units
        world.choose_deck(base_units = all_base_units)  # (base_units=my_deck)

        print('After choose deck:')
        for i in my_deck:
            print(i.type_id)
        # other preprocess
        # khodemun bayad path ro entekhab konim
        if len(world.get_me().paths_from_player) > 1:
            self.path_for_my_units = world.get_me().paths_from_player[random.randint(0,1)]
        else:
            self.path_for_my_units = world.get_me().paths_from_player[0]
        self.f.write("Paths from my palyer:")
        for i in world.get_me().paths_from_player:
            self.f.write(str(i.id))

    # it is called every turn for doing process during the game
    def turn(self, world):
        f = self.f
        f.write(f"turn started:{world.get_current_turn()}\n")
        myself = world.get_me()
        max_ap = world.game_constants.max_ap

        f.write('Enemy Units:\n')
        enemy_units = world.get_first_enemy().units
        min_enemy_health_unit_value = 100000
        best_path = world.get_me().paths_from_player[0]
        for unit in enemy_units:
            f.write(f'\nunit id is: {unit.unit_id}, unit cell is: {unit.cell}\n')
            enemy_unit_cell = unit.cell
            # print(world.get_paths_crossing_cell(enemy_unit_cell))
            if unit.hp < min_enemy_health_unit_value:
                for path_can_choose in world.get_me().paths_from_player :
                    for path_to_enemy in world.get_paths_crossing_cell(unit.cell):
                        f.write(f'  our path: {path_can_choose.id} path to enemy: {path_to_enemy.id}\n')
                        if path_can_choose == path_to_enemy:
                            min_enemy_health_unit_value = unit.hp
                            min_enemy_health_unit_cell = unit.cell
                            best_path = path_to_enemy

        f.write(f'best path id: {best_path.id}\n')
        # play all of hand once your ap reaches maximum. if ap runs out, putUnit doesn't do anything
        f.write('\nPath for my units in turn: ')
        if myself.ap == max_ap:
            for base_unit in myself.hand:
                world.put_unit(base_unit=base_unit, path=best_path)
                f.write(str(best_path.id) + ' ')
        f.write('\n\n------------------------------------------------------------\n\n')
        # this code tries to cast the received spell
        received_spell = world.get_received_spell()
        if received_spell is not None:
            if received_spell.is_area_spell():
                if received_spell.target == SpellTarget.ENEMY:
                    enemy_units = world.get_first_enemy().units
                    if len(enemy_units) > 0:
                        world.cast_area_spell(center=enemy_units[0].cell, spell=received_spell)
                elif received_spell.target == SpellTarget.ALLIED:
                    friend_units = world.get_friend().units
                    if len(friend_units) > 0:
                        world.cast_area_spell(center=friend_units[0].cell, spell=received_spell)
                elif received_spell.target == SpellTarget.SELF:
                    my_units = myself.units
                    if len(my_units) > 0:
                        world.cast_area_spell(center=my_units[0].cell, spell=received_spell)
            else:
                my_units = myself.units
                if len(my_units) > 0:
                     unit = my_units[0]
                     my_paths = myself.paths_from_player
                     path = my_paths[random.randint(0, len(my_paths) - 1)]
                     size = len(path.cells)
                     cell = path.cells[int((size + 1) / 2)]
                     world.cast_unit_spell(unit=unit, path=path, cell=cell, spell=received_spell)

        # this code tries to upgrade damage of first unit. in case there's no damage token, it tries to upgrade range
        if len(myself.units) > 0:
            unit = myself.units[0]
            world.upgrade_unit_damage(unit=unit)
            world.upgrade_unit_range(unit=unit)

    # it is called after the game ended and it does not affect the game.
    # using this function you can access the result of the game.
    # scores is a map from int to int which the key is player_id and value is player_score
    def end(self, world, scores):
        print("end started!")
        print("My score:" ,scores[world.get_me().player_id])
#        self.f.close()
