#بسم الله الرحمن الرحیم
import random

from model import *
# import datetime
from world import World


class AI:



    def __init__(self):

        self.rows = 0
        self.cols = 0
        self.path_for_my_units = None


        self.state = 1
        self.state_of_tele = 1
        self.unit_that_have_damage_upgrade = None
        self.unit_that_have_range_upgrade = None
        self.dade = 0
        self.number_of_unit_in_best_cell = 0
        self.best_cell_we_can_choose = Cell()





        #
        #     '''sahar log'''
        #     now = datetime.datetime.now().strftime("%d%B%Y-%I%M%p") + str(random.randint(0,10000))
        #     # now = 'log\\' + now       # sahar to ino bzn va khat paiin o coment kon
        #     now = 'log/' + now          # mn o parsa ino mizanim
        #     now = now + '.txt'
        #     self.f = open(now, "w+")
        #     ''' sahar log'''




    # this function is called in the beginning for deck picking and pre process
    def pick(self, world: World):
        #self.f.write('----------------------------Pick-------------------------------\n')
        map = world.get_map()
        self.rows = map.row_num
        self.cols = map.col_num
        #self.f.write('Player id: ' + str(world.get_me().player_id) + '\n')
        #self.f.write(f'MAP SIZE:{self.rows}*{self.cols}\n')
        print("pick started!")
        world.get_cast_spell_by_id(id = 1.1)

        # pre process
        # #self.f.write("ALL PATHS:\n")
        # for path in  map.paths:
        #     #self.f.write(f'PATH ID: {path.id}\n     PATH CELLS: ')
        #     for cell in path.cells:
        #         self.f.write(f'({cell.row}, {cell.col}), ')
        #     self.f.write('\n')
        # self.f.write('\n')
        # choosing hand
        all_base_units = world.get_all_base_units()

        # [base_unit for base_unit in all_base_units if not base_unit.is_flying]
        my_hand = [all_base_units[1], all_base_units[2], all_base_units[6], all_base_units[5], all_base_units[0]]

        # self.f.write('HAND: ')
        # for base_unit in my_hand:
        #     self.f.write(' ' + str(base_unit.type_id))
        # self.f.write('\n')

        # picking the chosen deck - rest of the deck will automatically be filled with random base_units
        world.choose_hand(base_units = my_hand)
                           # (base_units=my_deck)


        # other preprocess
        # khodemun bayad path ro entekhab konim
        if len(world.get_me().paths_from_player) > 1:
            self.path_for_my_units = world.get_friend().paths_from_player[0]
        else:
            self.path_for_my_units = world.get_friend().paths_from_player[0]
        #self.f.write("Paths from my palyer: ")

        # for i in world.get_friend().paths_from_player:
        #     self.f.write(str(i.id))
        # self.f.write('\n')

    # it is called every turn for doing process during the game
    def turn(self, world: World):
        self.dade = 0
        self.state_of_tele = 1
        all_base_units = world.get_all_base_units()
        print('#####################################')
        print('turn:')
        print(world.get_current_turn())


        # f = self.f
        # f.write('-------------------------------Turn-----------------------------------\n')
        # f.write(f"turn {world.get_current_turn()} started\n")
        #
        # f.write(f'REMAINING TURNS TO UPGRADE: {world.get_remaining_turns_to_upgrade()}\n')
        # f.write(f'AP: {world.get_me().ap}\n')
        # f.write(f'HAND: ')
        # for base_unit in world.get_me().hand:
        #     f.write(f'{base_unit.type_id} ')
        # f.write('\n')

        myself = world.get_me()

        enemy_units = world.get_first_enemy().units
        enemy_units.append(world.get_second_enemy())

        # self.logger(world)

        my_units = world.get_me().units


        if world.get_current_turn() == 1:
            self.dade = 1
            world.put_unit(base_unit=all_base_units[1], path=world.get_me().paths_from_player[0])
           # f.write(f'PUT UNIT {all_base_units[1].type_id} ON PATH {world.get_me().paths_from_player[0].id}\n')

        if  self.check_unit_in_hand(world.get_me().hand , all_base_units[0]) and self.dade == 0 :
            # print('0dadam')
            world.put_unit(base_unit=all_base_units[0], path=world.get_me().paths_from_player[0])
            #f.write(f'PUT UNIT {all_base_units[0].type_id} ON PATH {world.get_me().paths_from_player[0].id}\n')
            self.dade = 1

        if self.check_unit_in_hand(world.get_me().hand , all_base_units[1]) and self.dade == 0:
            # print('1dadam')
            world.put_unit(base_unit=all_base_units[1], path=world.get_me().paths_from_player[0])
            #f.write(f'PUT UNIT {all_base_units[1].type_id} ON PATH {world.get_me().paths_from_player[0].id}\n')
            self.dade = 1

        if self.check_unit_in_hand(world.get_me().hand , all_base_units[6]) and self.dade == 0:
            # print('2dadam')
            world.put_unit(base_unit=all_base_units[6], path=world.get_me().paths_from_player[0])
            #f.write(f'PUT UNIT {all_base_units[6].type_id} ON PATH {world.get_me().paths_from_player[0].id}\n')
            self.dade = 1

        if self.check_unit_in_hand(world.get_me().hand , all_base_units[2]) and self.dade == 0:
            # print('6dadam')
            world.put_unit(base_unit=all_base_units[2], path=world.get_me().paths_from_player[0])
            #f.write(f'PUT UNIT {all_base_units[2].type_id} ON PATH {world.get_me().paths_from_player[0].id}\n')
            self.dade = 1

        if self.check_unit_in_hand(world.get_me().hand , all_base_units[5]) and self.dade == 0:
            # print('5dadam')
            world.put_unit(base_unit=all_base_units[5], path=world.get_me().paths_from_player[0])
            #f.write(
                #f'PUT UNIT {all_base_units[5].type_id} ON PATH {world.get_me().paths_from_player[0].id}\n')
            self.dade = 1





        # for range upgrade
        if world.get_range_upgrade_number() > 0:

            if len(myself.units) > 0:
                units_max_range = []
                for unit_range in myself.units:
                    if unit_range.base_unit.type_id == 0:
                        units_max_range.append(unit_range)
                unit = self.get_max_hp(units_max_range)
                if unit is not None:
                    world.upgrade_unit_range(unit_id=unit.unit_id)
                    self.unit_that_have_range_upgrade = unit
                    # print(f'range dadam be {unit.unit_id}')

        # for damage upgrade
        if world.get_damage_upgrade_number() > 0:

            if len(myself.units) > 0:
                units_max_damage = []
                for unit_damage in myself.units:
                    if unit_damage.base_unit.type_id == 0:
                        units_max_damage.append(unit_damage)
                unit = self.get_max_hp(units_max_damage)
                if unit is not None:
                    world.upgrade_unit_damage(unit_id=unit.unit_id)
                    self.unit_that_have_damage_upgrade = unit


        if self.check_spell_in_spells(myself.spells, 0):
            # print('haste darimaaaaaaaaa---------------------------------------------------------------')
            if self.check_unit_in_units(world.get_me().units, all_base_units[0]):
                last_unit = my_units[-2]
                received_spell = self.spell_in_spells(myself.spells, 0)
                if last_unit.base_unit.type_id == 0:
                    world.cast_area_spell(center=last_unit.cell, spell=received_spell)
                    # print(f'{last_unit.unit_id} haste khord')

        if self.check_spell_in_spells(myself.spells, 1):
            # print('damage darimaaaaaaaaa---------------------------------------------------------------')
            last_unit = my_units[0].target
            if last_unit is not None:
                print(last_unit.unit_id)
            received_spell = self.spell_in_spells(myself.spells, 1)
            if last_unit is not None:
                world.cast_area_spell(center=last_unit.cell, spell=received_spell)
                # print(f'{last_unit.unit_id} damage khord')

        if self.check_spell_in_spells(myself.spells, 2):
            # print('heal darimaaaaaaaaa---------------------------------------------------------------')
            last_unit = my_units[1]
            received_spell = self.spell_in_spells(myself.spells, 2)
            if last_unit.hp < last_unit.base_unit.max_hp-1:
                world.cast_area_spell(center=last_unit.cell, spell=received_spell)
                # print(f'{last_unit.unit_id} heal khord')

        if self.check_spell_in_spells(myself.spells, 3):
            # print('tele darimaaaaaaaaa---------------------------------------------------------------')
            if self.check_unit_in_units(world.get_me().units, all_base_units[0]):
                last_unit = my_units[-1]
                first_unit = my_units[0]
                my_paths = myself.paths_from_player
                path = my_paths[random.randint(0, len(my_paths) - 1)]
                size = len(path.cells)
                cell = path.cells[(int((size + 1) / 2)) - 3]
                received_spell = self.spell_in_spells(myself.spells, 3)
                if last_unit.base_unit.type_id == 0:
                    if self.distance_from_my_king(first_unit.cell, world) > self.distance_from_my_king(path.cells[(int((size + 1) / 2))-3], world):
                        world.cast_unit_spell(unit=last_unit, path=path, cell=cell, spell=received_spell)
                        # print(f'{last_unit.unit_id}raft max')
                    else:
                        world.cast_unit_spell(unit=last_unit, path=path, cell=first_unit.cell, spell=received_spell)
                        # print(f'{last_unit.unit_id}raft khat')

        if self.check_spell_in_spells(myself.spells, 4):
            # print('duplicate darimaaaaaaaaa---------------------------------------------------------------')
            received_spell = self.spell_in_spells(myself.spells, 4)
            cell = self.return_best_cell_for_spell(world, received_spell)
            # print(f'number duplicate {self.number_of_unit_in_best_cell}')
            if self.number_of_unit_in_best_cell >= 3:
                received_spell = self.spell_in_spells(myself.spells, 4)
                world.cast_area_spell(center=cell, spell=received_spell)
            # print(f'{last_unit.unit_id} duplicate khord')

        if self.check_spell_in_spells(myself.spells, 5):
            # print('poison darimaaaaaaaaa---------------------------------------------------------------')
            last_unit = my_units[0].target
            if last_unit is not None:
                print(last_unit.unit_id)
            received_spell = self.spell_in_spells(myself.spells, 5)
            if last_unit is not None:
                world.cast_area_spell(center=last_unit.cell, spell=received_spell)
                # print(f'{last_unit.unit_id} poison khord')



    def end(self, world: World, scores):
        print("end started!")
        print("My score:", scores[world.get_me().player_id])

        # self.f.close()



     # added function

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



    def find_max_hp_between_our_unit(self, my_units):
        max_hp = 0
        unit_of_max_hp = my_units[0]
        for unit in my_units:
            if unit.hp > max_hp:
                max_hp = unit.hp
                unit_of_max_hp = unit
        return unit_of_max_hp

    def return_best_cell_for_spell(self, world, received_spell):
        self.number_of_unit_in_best_cell = 0
        self.best_cell_we_can_choose = 0
        map = world.get_map()
        row_of_map = map.row_num
        column_of_map = map.col_num
        row_of_best_cell = 0
        col_of_best_cell = 0

        for column_index in range(0, column_of_map):
            for row_index in range(0, row_of_map):
                cell_for_our_loop = Cell(row_index, column_index)       #cell e marboot be in halghe
                if self.number_of_unit_in_best_cell < len(
                        world.get_area_spell_targets(row=row_index, col=column_index, center=cell_for_our_loop,
                                                     spell=received_spell)):

                    self.number_of_unit_in_best_cell = len(
                        world.get_area_spell_targets(row=row_index, col=column_index, center=cell_for_our_loop,
                                                     spell=received_spell))

                    row_of_best_cell = row_index
                    col_of_best_cell = column_index


        self.best_cell_we_can_choose = Cell(row_of_best_cell, col_of_best_cell)

        return self.best_cell_we_can_choose


    def last_unit_enemy (self,units_1,units_2):
        units = units_1 + units_2
        return units[-1]

    def check_unit_in_hand(self , hand , unit):
        for item in hand:
            if  item.type_id == unit.type_id:
                return True
        return  False

    def check_unit_in_units(self , units , unit):
        for item in units:
            if  item.base_unit.type_id == unit.type_id:
                return True
        return  False

    def check_spell_in_spells(self , spells , spell_type_id):
        for item in spells:
            if item.type_id == spell_type_id:
                return True
        return False

    def spell_in_spells(self,spells, spell_type_id):
        for item in spells:
            if item.type_id == spell_type_id:
                return item

    def distance_from_my_king(self,cell,world):
        return abs(cell.col - world.get_me().king.center.col) + abs(cell.row - world.get_me().king.center.row)


    def logger(self,world):
        f = self.f
        f.write('Enemy Units:\n')
        first_enemy_units = world.get_first_enemy().units
        for unit in first_enemy_units:
            if type(unit) == Unit:
                f.write(f'Id: {unit.unit_id}    Cell: ({unit.cell.row}, {unit.cell.col})       BaseUnit: {unit.base_unit.type_id}      HP: {unit.hp}      Spells: {unit.affected_spells} 1st enemy\n')
        second_enemy_units = world.get_second_enemy().units
        for unit in second_enemy_units:
            if type(unit) == Unit:
                f.write(f'Id: {unit.unit_id}    Cell: ({unit.cell.row}, {unit.cell.col})        BaseUnit: {unit.base_unit.type_id}      HP: {unit.hp}      Spells: {unit.affected_spells} 2nd enemy\n')
        f.write('\n')

        f.write('My Units:\n')
        my_units = world.get_me().units
        for unit in my_units:
            if type(unit) == Unit:
                f.write(f'Id: {unit.unit_id}    Cell: ({unit.cell.row}, {unit.cell.col})        BaseUnit: {unit.base_unit.type_id}      HP: {unit.hp}      Spells: {unit.affected_spells} \n')
        f.write('\n')

        f.write('Friend Units:\n')
        friend_units = world.get_friend().units
        for unit in friend_units:
            if type(unit) == Unit:
                f.write(f'Id: {unit.unit_id}    Cell: ({unit.cell.row}, {unit.cell.col})        BaseUnit: {unit.base_unit.type_id}      HP: {unit.hp}      Spells: {unit.affected_spells} \n')
        f.write('\n')
