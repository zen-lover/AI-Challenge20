#بسم الله الرحمن الرحیم
import random

from model import *
import datetime
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






        '''sahar log'''
        now = datetime.datetime.now().strftime("%d%B%Y-%I%M%p") + str(random.randint(0,10000))
        # now = 'log\\' + now       # sahar to ino bzn va khat paiin o coment kon
        now = 'log/' + now          # mn o parsa ino mizanim
        now = now + '.txt'
        self.f = open(now, "w+")
    ''' sahar log'''




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
        # choosing hand
        all_base_units = world.get_all_base_units()

        # [base_unit for base_unit in all_base_units if not base_unit.is_flying]
        my_hand = [all_base_units[1], all_base_units[2], all_base_units[6], all_base_units[7], all_base_units[0]]

        self.f.write('HAND: ')
        for base_unit in my_hand:
            self.f.write(' ' + str(base_unit.type_id))
        self.f.write('\n')

        # picking the chosen deck - rest of the deck will automatically be filled with random base_units
        world.choose_hand(base_units = my_hand)
                           # (base_units=my_deck)


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
        self.dade = 0
        self.state_of_tele = 1
        all_base_units = world.get_all_base_units()
        print('#####################################')
        print('turn:')
        print(world.get_current_turn())
        print('ap')
        print(world.get_me().ap)
        print('hand')
        for item in world.get_me().hand:
            print(item.type_id)
        print('*************************')


        f = self.f
        f.write('-------------------------------Turn-----------------------------------\n')
        f.write(f"turn {world.get_current_turn()} started\n")

        f.write(f'REMAINING TURNS TO UPGRADE: {world.get_remaining_turns_to_upgrade()}\n')
        f.write(f'AP: {world.get_me().ap}\n')
        f.write(f'HAND: ')
        for base_unit in world.get_me().hand:
            f.write(f'{base_unit.type_id} ')
        f.write('\n')

        myself = world.get_me()

        enemy_units = world.get_first_enemy().units
        enemy_units.append(world.get_second_enemy())

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




        if world.get_current_turn() == 1 :
            self.dade = 1
            world.put_unit(base_unit=all_base_units[1], path=world.get_me().paths_from_player[0])
            f.write(f'PUT UNIT {all_base_units[1].type_id} ON PATH {world.get_me().paths_from_player[0].id}\n')

            world.put_unit(base_unit=all_base_units[0], path=world.get_me().paths_from_player[0])
            f.write(f'PUT UNIT {all_base_units[0].type_id} ON PATH {world.get_me().paths_from_player[0].id}\n')

            world.put_unit(base_unit=all_base_units[6], path=world.get_me().paths_from_player[0])
            f.write(f'PUT UNIT {all_base_units[6].type_id} ON PATH {world.get_me().paths_from_player[0].id}\n')





        if  self.check_unit_in_hand(world.get_me().hand , all_base_units[0]) and self.dade == 0 :
            print('0dadam')
            world.put_unit(base_unit=all_base_units[0], path=world.get_me().paths_from_player[0])
            f.write(f'PUT UNIT {all_base_units[0].type_id} ON PATH {world.get_me().paths_from_player[0].id}\n')
            self.dade = 1



        if self.check_unit_in_hand(world.get_me().hand , all_base_units[1]) and self.dade == 0:
            print('1dadam')
            world.put_unit(base_unit=all_base_units[1], path=world.get_me().paths_from_player[0])
            f.write(f'PUT UNIT {all_base_units[1].type_id} ON PATH {world.get_me().paths_from_player[0].id}\n')
            self.dade = 1


        if self.check_unit_in_hand(world.get_me().hand , all_base_units[6]) and self.dade == 0:
            print('2dadam')
            world.put_unit(base_unit=all_base_units[6], path=world.get_me().paths_from_player[0])
            f.write(f'PUT UNIT {all_base_units[6].type_id} ON PATH {world.get_me().paths_from_player[0].id}\n')
            self.dade = 1


        if self.check_unit_in_hand(world.get_me().hand , all_base_units[2]) and self.dade == 0:
            print('6dadam')
            world.put_unit(base_unit=all_base_units[2], path=world.get_me().paths_from_player[0])
            f.write(f'PUT UNIT {all_base_units[2].type_id} ON PATH {world.get_me().paths_from_player[0].id}\n')
            self.dade = 1


        if self.check_unit_in_hand(world.get_me().hand , all_base_units[5]) and self.dade == 0:
            print('5dadam')
            world.put_unit(base_unit=all_base_units[5], path=world.get_me().paths_from_player[0])
            f.write(
                f'PUT UNIT {all_base_units[5].type_id} ON PATH {world.get_me().paths_from_player[0].id}\n')
            self.dade = 1










            # if self.state == 6:
        #     for max_hp_unit in world.get_me().hand:
        #         if max_hp_unit.max_hp >= max_hp and max_hp_unit.type_id != 4:
        #             max_hp = max_hp_unit.max_hp
        #             max_hp_unit_select = max_hp_unit
        #     world.put_unit(base_unit=max_hp_unit_select, path=world.get_me().paths_from_player[0])
        #     f.write(f'PUT UNIT {max_hp_unit_select.type_id} ON PATH {world.get_me().paths_from_player[0].id}\n')
        #     self.state = 7
        #
        #
        # if self.state == 7:
        #     for max_damage_unit in world.get_me().hand:
        #         if max_damage_unit.base_attack >= max_damage:
        #             max_damage = max_damage_unit.base_attack
        #             max_damage_unit_select = max_damage_unit
        #     world.put_unit(base_unit=max_damage_unit_select, path=world.get_me().paths_from_player[0])
        #     f.write(f'PUT UNIT {max_hp_unit_select.type_id} ON PATH {world.get_me().paths_from_player[0].id}\n')
        #     self.state = 8
        #
        # if self.state == 8:
        #
        #     for max_range_unit in world.get_me().hand:
        #         if max_range_unit.base_range >= max_range:
        #             max_range = max_range_unit.base_range
        #             max_range_unit_select = max_range_unit
        #     world.put_unit(base_unit=max_range_unit_select, path=world.get_me().paths_from_player[0])
        #     #f.write(f'PUT UNIT {max_hp_unit_select.type_id} ON PATH {world.get_me().paths_from_player[0].id}\n')
        #     self.status = 9
        #
        #
        # if self.state == 9 :
        #
        #     for max_range_unit in world.get_me().hand:
        #         if max_range_unit.base_range >= max_range:
        #             max_range = max_range_unit.base_range
        #             max_range_unit_select = max_range_unit
        #     world.put_unit(base_unit=max_range_unit_select, path=world.get_me().paths_from_player[0])
        #     f.write(f'PUT UNIT {max_hp_unit_select.type_id} ON PATH {world.get_me().paths_from_player[0].id}\n')
        #     self.status = 6

        print('each turn')
        print(world._current_turn)



        # for range upgrade
        if world.get_range_upgrade_number() > 0:

            if len(myself.units) > 0:
                units_max_range = []
                for unit_range in myself.units:
                    if unit_range.range >= 4:
                        units_max_range.append(unit_range)
                unit = self.get_max_hp(units_max_range)
                if unit is not None:
                    world.upgrade_unit_range(unit_id=unit.unit_id)
                    self.unit_that_have_range_upgrade = unit


        # for damage upgrade
        if world.get_damage_upgrade_number() > 0:

            if len(myself.units) > 0:
                units_max_damage = []
                for unit_damage in myself.units:
                    if unit_damage.attack >= 12:
                        units_max_damage.append(unit_damage)
                unit = self.get_max_hp(units_max_damage)
                if unit is not None:
                    world.upgrade_unit_damage(unit_id=unit.unit_id)
                    self.unit_that_have_damage_upgrade = unit




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

                my_units = myself.units         # hame unit hamoon
                unit = self.find_max_hp_between_our_unit(my_units)      #max hp ro dar unit mirizim dashte bashim
                my_paths = myself.paths_from_player                     #hame rah haro mirizim toosh
                path = my_paths[random.randint(0, len(my_paths) - 1)]# yeki ro random entekhab mikonim

                size = len(path.cells)
                cell = path.cells[(int((size + 1) / 2))-3]# jolo tarin cell esh ro bedast miarim

                self.state_of_tele = 1

                if (self.unit_that_have_range_upgrade  is not  None and self.state_of_tele == 1  ):


                    if self.unit_that_have_range_upgrade.path.cells.index(self.unit_that_have_range_upgrade.cell)  < path.cells.index(cell):

                        world.cast_unit_spell(unit=self.unit_that_have_range_upgrade, path=path, cell=cell, spell=received_spell  )
                        self.state_of_tele = 2


                if (self.unit_that_have_damage_upgrade is not None  and self.state_of_tele == 1 ):
                    print(self.unit_that_have_damage_upgrade.unit_id)
                    if  self.unit_that_have_damage_upgrade.path.cells.index(self.unit_that_have_damage_upgrade.cell)  < path.cells.index(cell) :

                        self.unit_that_have_damage_upgrade.path.cells.index(self.unit_that_have_damage_upgrade.cell)

                        world.cast_unit_spell(unit=self.unit_that_have_damage_upgrade, path=path, cell=cell, spell=received_spell)
                        self.state_of_tele = 2


                if (self.state_of_tele == 1) :

                    world.cast_unit_spell(unit=unit, path=path, cell=cell, spell=received_spell)

                    self.state_of_tele = 2


    # it is called after the game ended and it does not affect the game.
    # using this function you can access the result of the game.
    # scores is a map from int to int which the key is player_id and value is player_score
    def end(self, world: World, scores):
        print("end started!")
        print("My score:", scores[world.get_me().player_id])

        self.f.close()


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

                    number_of_unit_in_best_cell = len(
                        world.get_area_spell_targets(row=row_index, col=column_index, center=cell_for_our_loop,
                                                     spell=received_spell))
                    row_of_best_cell = row_index
                    col_of_best_cell = column_index

                    best_cell_we_can_choose = Cell(row_of_best_cell, col_of_best_cell)
        return best_cell_we_can_choose

    def last_unit_enemy (self,units_1,units_2):
        units = units_1 + units_2
        return units[-1]

    def check_unit_in_hand(self , hand , unit):
        for item in hand:
            if  item.type_id == unit.type_id:
                return True

        return  False












