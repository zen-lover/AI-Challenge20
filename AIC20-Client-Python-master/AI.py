
import random
from typing import List, Any

from model import *
import datetime
from world import World


class AI:



    def __init__(self):

        self.all_units_in_game = []
        self.rows = 0
        self.cols = 0
        self.path_for_my_units = None
        self.state = 1
        self.first_unit_added = False
        self.second_unit_added = False

        '''sahar log'''
        now = datetime.datetime.now().strftime("%d%B%Y-%I%M%p") + str(random.randint(0, 1000))
        now = 'log\\' + now       # sahar to ino bzn va khat paiin o coment kon
#        now = 'log/' + now          # mn o parsa ino mizanim
        now = now + '.txt'
        self.f = open(now, "w+")
        ''' sahar log'''

        '''AI LOG'''
        self.data_log = open('data\\' + str(datetime.datetime.now().strftime("%d%B%Y-%I%M%p") + str(random.randint(1000, 10000))) + '.txt', "w+")
        self.damages_log = open('data\\damages.txt', "a")

    # this function is called in the beginning for deck picking and pre process
    def pick(self, world: World):
        self.f.write('----------------------------Pick-------------------------------\n')
        map = world.get_map()
        self.rows = map.row_num
        self.cols = map.col_num
        self.f.write('Player id: ' + str(world.get_me().player_id) + '\n')
        self.f.write(f'MAP SIZE:{self.rows}*{self.cols}\n')
        print("pick started!")
        world.get_cast_spell_by_id(id = 1.1)

        # pre process
        self.f.write("ALL PATHS:\n")
        for path in  map.paths:
            self.f.write(f'PATH ID: {path.id}\n     PATH CELLS: ')
            for cell in path.cells:
                self.f.write(f'({cell.row}, {cell.col}), ')
            self.f.write('\n')
        self.f.write('\n')
        # choosing all flying units
        all_base_units = world.get_all_base_units()
        my_hand = [all_base_units[1], all_base_units[5], all_base_units[0], all_base_units[6], all_base_units[2]]#[base_unit for base_unit in all_base_units if not base_unit.is_flying]
        # for i in my_deck:
        #     print(i.type_id)
        self.f.write('HAND: ')
        for base_unit in my_hand:
            self.f.write(' ' + str(base_unit.type_id))
        self.f.write('\n')

        # picking the chosen deck - rest of the deck will automatically be filled with random base_units
        world.choose_hand(base_units = my_hand)
                           # (base_units=my_deck)

        print('After choose hand:')
        for i in my_hand:
            print(i.type_id)
        # other preprocess
        # khodemun bayad path ro entekhab konim
        if len(world.get_me().paths_from_player) > 1:
            self.path_for_my_units = world.get_friend().paths_from_player[0]
        else:
            self.path_for_my_units = world.get_friend().paths_from_player[0]
        self.f.write("Paths from my palyer: ")

        for i in world.get_friend().paths_from_player:
            self.f.write(str(i.id))
        self.f.write('\n')

    # it is called every turn for doing process during the game
    def turn(self, world: World):
        f = self.f
        f.write('-------------------------------Turn-----------------------------------\n')
        f.write(f"turn {world.get_current_turn()} started\n")
        print("----------------------------------------------------turn started:", world.get_current_turn())
        # print('turn to upgrade')
        # print(world.get_remaining_turns_to_upgrade())
        f.write(f'REMAINING TURNS TO UPGRADE: {world.get_remaining_turns_to_upgrade()}\n')
        f.write(f'AP: {world.get_me().ap}\n')
        f.write(f'HAND: ')
        for base_unit in world.get_me().hand:
            f.write(f'{base_unit.type_id} ')
        f.write('\n')

        myself = world.get_me()
        self.log(world)
        self.choose_and_put_unit(world)
        # enter first hand

        #
        # if  self.state == 1:
        #     world.put_unit(base_unit=world._base_units[1], path=world.get_me().paths_from_player[0])
        #     print('hero 1')
        #     self.state = 2
        # elif self.state == 2:
        #     world.put_unit(base_unit=world._base_units[5], path=world.get_me().paths_from_player[0])
        #     print('hero 2')
        #     self.state = 3
        # elif self.state == 3:
        #     world.put_unit(base_unit=world._base_units[0], path=world.get_me().paths_from_player[0])
        #     print('hero 3')
        #     self.state = 4
        # elif self.state == 4:
        #     world.put_unit(base_unit=world._base_units[6], path=world.get_me().paths_from_player[0])
        #     print('hero 4')
        #     self.state = 5
        # elif self.state == 5:
        #     world.put_unit(base_unit=world._base_units[2], path=world.get_me().paths_from_player[0])
        #     print('hero 5')
        #     self.state = 6
        #
        # max_hp = 0
        # max_damage = 0
        # max_range = 0
        # if self.state == 6:
        #     for max_hp_unit in world.get_me().hand:
        #         if max_hp_unit.max_hp >= max_hp and max_hp_unit.type_id != 4:
        #             max_hp = max_hp_unit.max_hp
        #             max_hp_unit_select = max_hp_unit
        #     world.put_unit(base_unit=max_hp_unit_select, path=world.get_me().paths_from_player[0])
        #     f.write(f'PUT UNIT {max_hp_unit_select.type_id} ON PATH {world.get_me().paths_from_player[0].id} WITH COST {max_hp_unit_select.ap}\n')
        #     self.status = 7
        # if self.state == 7:
        #     for max_damage_unit in world.get_me().hand:
        #         if max_damage_unit.base_attack >= max_damage:
        #             max_damage = max_damage_unit.base_attack
        #             max_damage_unit_select = max_damage_unit
        #     world.put_unit(base_unit=max_damage_unit_select, path=world.get_me().paths_from_player[0])
        #     f.write(f'PUT UNIT {max_hp_unit_select.type_id} ON PATH {world.get_me().paths_from_player[0].id} WITH COST {max_hp_unit_select.ap}\n')
        #     self.status = 8
        # if self.state == 8:
        #     for max_range_unit in world.get_me().hand:
        #         if max_range_unit.base_range >= max_range:
        #             max_range = max_range_unit.base_range
        #             max_range_unit_select = max_range_unit
        #     world.put_unit(base_unit=max_range_unit_select, path=world.get_me().paths_from_player[0])
        #     f.write(f'PUT UNIT {max_hp_unit_select.type_id} ON PATH {world.get_me().paths_from_player[0].id} WITH COST {max_hp_unit_select.ap}\n')
        #     self.status = 6

        # print('each turn')
        # print(world._current_turn)
        # print(world.get_me().ap)
        ## berim soraghe in ke spell bendazim :))

        received_spell = world.get_received_spell()
        if received_spell is not None:
            if received_spell.is_area_spell():  # age area bood              :  hame be joz tele
                # spell enemy               : damage va poison bood         : zarar be doshman
                if received_spell.target == SpellTarget.ENEMY:
                    world.cast_area_spell(center=self.return_best_cell_for_spell(world, received_spell),
                                          spell=received_spell)
                # spell allied          : ye khoobi bara khodemoon dasht
                elif received_spell.target == SpellTarget.ALLIED:
                    world.cast_area_spell(center=self.return_best_cell_for_spell(world, received_spell),
                                          spell=received_spell)
                elif received_spell.target == SpellTarget.SELF:
                    world.cast_area_spell(center=self.return_best_cell_for_spell(world, received_spell),
                                          spell=received_spell)
                # age tele bood spell :) miad balatarin hp ro jolo tarin halate momken midaze !
            else:
                my_units = myself.units
                unit = self.find_max_hp_between_our_unit(my_units)
                my_paths = myself.paths_from_player
                path = my_paths[random.randint(0, len(my_paths) - 1)]
                size = len(path.cells)
                cell = path.cells[int((size + 1) / 2)]
                world.cast_unit_spell(unit=unit, path=path, cell=cell, spell=received_spell)

        # this code tries to upgrade damage of first unit. in case there's no damage token, it tries to upgrade range
        # for range upgrade
        if world.get_range_upgrade_number() > 0:
            # print(f'\nwe have {world.get_range_upgrade_number()} range upgrade')
            if len(myself.units) > 0:
                units_max_range = []
                for unit_range in myself.units:
                    if unit_range.range == 4:
                        units_max_range.append(unit_range)
                # print(units_max_range)
                unit = self.get_max_hp(units_max_range)
                # for upgrade_unit in myself.units:
                #     unit = upgrade_unit
                if unit is not None:
                    world.upgrade_unit_range(unit_id=unit.unit_id)
                    print(world.upgrade_unit_range(unit_id=unit.unit_id))
                    print(f'range upgrade token {unit.unit_id}\n')

        # for damage upgrade
        if world.get_damage_upgrade_number() > 0:
            #print(f'\nwe have {world.get_damage_upgrade_number()} damage upgrade')
            if len(myself.units) > 0:
                units_max_damage = []
                for unit_damage in myself.units:
                    if unit_damage.range >= 15:
                        units_max_damage.append(unit_damage)
                unit = self.get_max_hp(units_max_damage)
                # for upgrade_unit in myself.units:
                #     unit = upgrade_unit
                if unit is not None:
                    world.upgrade_unit_damage(unit_id=unit.unit_id)
                    print(world.upgrade_unit_damage(unit_id=unit.unit_id))
                    # print(f'damage upgrade token {unit.unit_id}\n')



    # it is called after the game ended and it does not affect the game.
    # using this function you can access the result of the game.
    # scores is a map from int to int which the key is player_id and value is player_score
    def end(self, world: World, scores):
        self.f.write('---------------------------------END-------------------------------------\n')
        print("end started!")
        print("My score:", scores[world.get_me().player_id])
        self.f.write(f'MY SCORE: {scores[world.get_me().player_id]}\n')
        self.f.close()
        for unit in self.all_units_in_game:
            print(f"jdfhkfjhszkjhfksjhfkjhsd unit id:{unit.unit_id}")
            self.damages_log.write('unit_id:  '+ str(unit.unit_id)+ '  base_unit:  '+ str(unit.base_unit.type_id)+ '  damage_caused:  ' + str(unit.damage_caused) + '\n')


        self.damages_log.close()
        self.data_log.write(f'MY SCORE: {scores[world.get_me().player_id]}\n')
        self.data_log.close()

    '''------------------------Added Functions-----------------------'''

    def get_max_hp(self ,units):
        max_hp = 0
        if len(units) > 0:
            max_hp_unit_select = units[0]
            for max_hp_unit in units:
                if max_hp_unit.hp >= max_hp and max_hp_unit.base_unit.type_id != 4:
                    max_hp = max_hp_unit.hp
                    max_hp_unit_select = max_hp_unit
            if max_hp_unit_select is not None:
                return max_hp_unit_select
        else:
            return None

    def get_max_damage(self, units):
        max_damage = 0
        if len(units) > 0:
            max_damage_unit_select = units[0]
            for max_damage_unit in units:
                if max_damage_unit.attack >= max_damage:
                    max_damage = max_damage_unit.attack
                    max_damage_unit_select = max_damage_unit
            if max_damage_unit_select is not None:
                return max_damage_unit_select
        else:
            return None

    def get_max_range(self, units):
        max_range = 0
        if len(units) > 0:
            max_range_unit_select = units[0]
            for max_range_unit in units:
                if max_range_unit.range >= max_range:
                    max_range = max_range_unit.range
                    max_range_unit_select = max_range_unit
            if max_range_unit_select is not None:
                return max_range_unit_select
        else:
            return None

    def return_best_cell_for_spell(self, world, received_spell):
        map = world.get_map()
        row_of_map = map.row_num
        column_of_map = map.col_num
        number_of_unit_in_best_cell = 0
        row_of_best_cell = 0
        col_of_best_cell = 0
        best_cell_we_can_choose = Cell()

        for column_index in range(0, column_of_map):
            for row_index in range(0, row_of_map):
                if number_of_unit_in_best_cell < len(
                        world.get_area_spell_targets(row_index, column_index, received_spell)):
                    number_of_unit_in_best_cell = len(
                        world.get_area_spell_targets(row_index, column_index, received_spell))
                    row_of_best_cell = row_index
                    col_of_best_cell = column_index
                    best_cell_we_can_choose = Cell(row_of_best_cell, col_of_best_cell)
        return best_cell_we_can_choose

    def find_max_hp_between_our_unit(self, my_units):
        max_hp = 0
        unit_of_max_hp = my_units[0]
        for unit in my_units:
            if unit.hp > max_hp:
                max_hp = unit.hp
                unit_of_max_hp = unit
        return unit_of_max_hp

    def return_best_cell_for_spell(self, world, received_spell):
        map = world.get_map()
        row_of_map = map.row_num
        column_of_map = map.col_num
        number_of_unit_in_best_cell = 0
        row_of_best_cell = 0
        col_of_best_cell = 0
        best_cell_we_can_choose = Cell()
        for column_index in range(0, column_of_map):
            for row_index in range(0, row_of_map):
                cell_for_our_loop = Cell(row_index, column_index)
                if number_of_unit_in_best_cell < len(
                        world.get_area_spell_targets(row=row_index, col=column_index, center=cell_for_our_loop,
                                                     spell=received_spell)):
                    print('tedad niroo jaii ke mizanim')
                    print(len(world.get_area_spell_targets(row=row_index, col=column_index, center=cell_for_our_loop,
                                                           spell=received_spell)))
                    number_of_unit_in_best_cell = len(
                        world.get_area_spell_targets(row=row_index, col=column_index, center=cell_for_our_loop,
                                                     spell=received_spell))
                    row_of_best_cell = row_index
                    col_of_best_cell = column_index
                    print('jaii ke mizanim ')
                    best_cell_we_can_choose = Cell(row_of_best_cell, col_of_best_cell)
        print(best_cell_we_can_choose.row)
        print(best_cell_we_can_choose.col)
        return best_cell_we_can_choose

    def choose_and_put_unit(self, world):
        ap = world.get_me().ap
        print('AP: ' + str(ap) + '\n')
        data = self.data_log
        hand = world.get_me().hand
        first_random_unit = random.randint(0, 4)
        second_random_unit = random.randint(0, 4)
        paths = world.get_me().paths_from_player + world.get_friend().paths_from_player
        path_num = len(paths)
        rand_path1 = random.randint(0, path_num - 1)
        rand_path2 = random.randint(0, path_num - 1)

        if len(world.get_me().units) != 0:
            print(world.get_me().units)
            last_unit = world.get_me().units[-1]
            self.all_units_in_game.append(last_unit)
            data.write(
            f'id:  {last_unit.unit_id}  type:  {hand[first_random_unit].type_id}  path:  {paths[rand_path1].id}\n')

        if self.second_unit_added:
            last_unit = world.get_me().units[-2]
            self.all_units_in_game.append(last_unit)
            data.write(
                f'id:  {last_unit.unit_id}  type:  {hand[second_random_unit].type_id}  path:  {paths[rand_path2].id}\n')

        if(ap == 10):
            print('in if\n')
            world.put_unit(hand[first_random_unit].type_id, paths[rand_path1].id)
            self.first_unit_added = True
            ap = ap - hand[first_random_unit].ap

            if ap >= hand[second_random_unit].ap:
                world.put_unit(hand[second_random_unit].type_id, paths[rand_path2].id)
                self.second_unit_added = True

    def affected_units_by_this_unit(self, world, unit):
        target_type = unit.base_unit.target_type
        multi = unit.base_unit.is_multiple
        units_in_cell = []
        if(unit.target != None):
            units_in_cell.append(unit.target)
        # if multi:
        #     units_in_cell = self.units_on_this_cell(world, unit.cell)
        # if (len(units_in_cell) != 0):
        for soldier in units_in_cell:
            if soldier.player_id == world.get_first_enemy().player_id or soldier.player_id == world.get_second_enemy().player_id:
                # print(f'my unit type is {unit.base_unit.type_id} and target: {unit.base_unit.target_type}')
                # print(f'soldier: {soldier}')
                if target_type == UnitTarget.AIR and soldier.base_unit.is_flying:
                    unit.damage_caused = unit.damage_caused + unit.attack
                    # print(f'target type is {target_type} and is flying damage caused: {unit.damage_caused} and attack: {unit.attack}')
                elif target_type == UnitTarget.GROUND and not soldier.base_unit.is_flying:
                    unit.damage_caused = unit.damage_caused + unit.attack
                    # print(f'target type is {target_type} and is not flying damage caused: {unit.damage_caused} and attack: {unit.attack}')
                elif target_type == UnitTarget.BOTH:
                    unit.damage_caused = unit.damage_caused + unit.attack
                        # print(f'BOTH targets and the damage caused: {unit.damage_caused} and attack: {unit.attack}')

    def units_on_this_cell(self, world, cell):
        units = []
        for unit in world.get_map().units:
            if(unit.cell == cell):
                units.append(unit)
        print('units on this cell')
        for u in units:
            print(u.unit_id)
        return units

    def unit_is_in_this_area(self, world, from_row, to_row, from_col, to_col):
        units = world.get_map().units
        for unit in units:
            cell = unit.cell
            if(cell.row >= from_row and cell.row <= to_row and cell.col >= from_col and cell.col <= to_col ):
                return True
        return False

    def units_in_this_area(self, world, from_row, to_row, from_col, to_col):
        units = []
        for unit in world.get_map().units:
            if self.unit_is_in_this_area(world, from_row, to_row, from_col, to_col):
                units += unit
        return units

    def log(self, world):
        enemy_units = world.get_first_enemy().units
        enemy_units.append(world.get_second_enemy())
        f = self.f
        f.write('Enemy Units:\n')
        first_enemy_units = world.get_first_enemy().units
        for unit in first_enemy_units:
            if type(unit) == Unit:
                f.write(
                    f'Id: {unit.unit_id}    Cell: ({unit.cell.row}, {unit.cell.col})       BaseUnit: {unit.base_unit.type_id}      HP: {unit.hp}      Spells: {unit.affected_spells} 1st enemy\n')
        second_enemy_units = world.get_second_enemy().units
        for unit in second_enemy_units:
            if type(unit) == Unit:
                f.write(
                    f'Id: {unit.unit_id}    Cell: ({unit.cell.row}, {unit.cell.col})        BaseUnit: {unit.base_unit.type_id}      HP: {unit.hp}      Spells: {unit.affected_spells} 2nd enemy\n')
        f.write('\n')

        f.write('My Units:\n')
        my_units = world.get_me().units
        for unit in my_units:
            self.affected_units_by_this_unit(world, unit)
            if type(unit) == Unit:
                f.write(
                    f'Id: {unit.unit_id}    Cell: ({unit.cell.row}, {unit.cell.col})        BaseUnit: {unit.base_unit.type_id}      HP: {unit.hp}      Spells: {unit.affected_spells} \n')
        f.write('\n')

        f.write('Friend Units:\n')
        friend_units = world.get_friend().units
        for unit in friend_units:
            if type(unit) == Unit:
                f.write(
                    f'Id: {unit.unit_id}    Cell: ({unit.cell.row}, {unit.cell.col})        BaseUnit: {unit.base_unit.type_id}      HP: {unit.hp}      Spells: {unit.affected_spells} \n')
        f.write('\n')
        '''LOG'''
