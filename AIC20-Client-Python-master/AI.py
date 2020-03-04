# بسم الله الرحمن الرحیم
import random

from model import *
# import datetime
from world import World


class AI:
    closest_enemy_path: Path

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
        self.could_help_friend_while_hp_is_low = 1
        self.could_put_unit_on_friends_path = 1
        self.number_of_turns_after_friends_death = 0
        self.number_of_turns_after_last_put_to_friend = 0
        self.last_friend_unit_on_my_way = None
        self.turn_of_last_friend_unit_on_my_way = -1
        self.number_of_units_put_yet = 0
        self.closest_enemy_path = Path(-1, None, None)

        self.bayadbfrstm = False
        self.masir = Path(-1, None, None)
        self.baredoshman = 0
        self.barekhali = 0
        self.rukhalibfrstm = False
        self.masirekhali = Path(-1, None, None)
        self.faselealanedoshman =1000
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
        # self.f.write('----------------------------Pick-------------------------------\n')
        map = world.get_map()
        self.rows = map.row_num
        self.cols = map.col_num
        # self.f.write('Player id: ' + str(world.get_me().player_id) + '\n')
        # self.f.write(f'MAP SIZE:{self.rows}*{self.cols}\n')
        # print("pick started!")
        world.get_cast_spell_by_id(id=1.1)
        self.closest_enemy_path = world.get_me().paths_from_player[0]
        self.masir = world.get_me().paths_from_player[0]
        self.masirekhali = world.get_me().paths_from_player[0]

        # choosing hand
        all_base_units = world.get_all_base_units()

        # [base_unit for base_unit in all_base_units if not base_unit.is_flying]
        my_hand = [all_base_units[1], all_base_units[2], all_base_units[6], all_base_units[5], all_base_units[0]]

        # self.f.write('HAND: ')
        # for base_unit in my_hand:
        #     self.f.write(' ' + str(base_unit.type_id))
        # self.f.write('\n')

        # picking the chosen deck - rest of the deck will automatically be filled with random base_units
        world.choose_hand(base_units=my_hand)
        # (base_units=my_deck)

        # other preprocess
        # khodemun bayad path ro entekhab konim
        if len(world.get_me().paths_from_player) > 1:
            self.path_for_my_units = world.get_friend().paths_from_player[0]
        else:
            self.path_for_my_units = world.get_friend().paths_from_player[0]
        # self.f.write("Paths from my palyer: ")

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
        if world.get_current_turn() > 2:
            self.myfunction(world)
        elif world.get_current_turn() == 1:
            shortesttaking = self.minemasirbeshah(world)
            world.put_unit(base_unit=all_base_units[5], path=shortesttaking)
            world.put_unit(base_unit=all_base_units[1], path=shortesttaking)
        elif world.get_current_turn() == 2:
            shortesttaking = self.minemasirbeshah(world)
            world.put_unit(base_unit=all_base_units[6], path=shortesttaking)
            world.put_unit(base_unit=all_base_units[0], path=shortesttaking)

        # self.put_x_units_on_closest(world, 5)
        # if self.could_help_friend_while_hp_is_low == 0:
        #     if self.put_the_most_damage_on_friend_path(world):
        #         # print('could put the previous one')
        #         self.could_help_friend_while_hp_is_low = 1
        # if self.friend_is_empty(world) or world.get_friend().king.hp < 80:
        #     # print(f'friends hp: {world.get_friend().king.hp}')
        #     self.help_friend(world) #agar unit nadasht ya hp sh kam shod
        # self.should_put_unit_on_friends_path(world) #agar ru masire ma gozasht
        # self.check_friends_king(world) #agar shahesh morde bud
        # # self.choose_and_put_unit(world,all_base_units)

        # for range upgrade
        if world.get_range_upgrade_number() > 0:

            if len(myself.units) > 0 and world.get_current_turn() > 70:
                units_max_range = []
                for unit_range in myself.units:
                    if unit_range.base_unit.type_id == 0:
                        units_max_range.append(unit_range)
                unit = self.get_max_hp(units_max_range)
                if unit is not None and world.get_current_turn() > 75:
                    for unit_range in myself.units:
                        if unit_range.base_unit.type_id == 6:
                            units_max_range.append(unit_range)
                    unit = self.get_max_hp(units_max_range)
                if unit is not None:
                    for i in range(0, world.get_range_upgrade_number()):
                        world.upgrade_unit_range(unit_id=unit.unit_id)
                    # self.unit_that_have_range_upgrade = unit
                    #     print(f'range dadam be {unit.unit_id}')

        # for damage upgrade
        if world.get_damage_upgrade_number() > 0:

            if len(myself.units) > 0 and world.get_current_turn() > 70:
                units_max_damage = []
                for unit_damage in myself.units:
                    if unit_damage.base_unit.type_id == 0:
                        units_max_damage.append(unit_damage)
                unit = self.get_max_hp(units_max_damage)
                if unit is not None and world.get_current_turn() > 75:
                    for unit_damage in myself.units:
                        if unit_damage.base_unit.type_id == 6:
                            units_max_damage.append(unit_damage)
                    unit = self.get_max_hp(units_max_damage)
                if unit is not None:
                    for i in range(0, world.get_damage_upgrade_number()):
                        world.upgrade_unit_damage(unit_id=unit.unit_id)
                    # self.unit_that_have_damage_upgrade = unit
                    #     print(f'damage dadam be {unit.unit_id}')

        if self.check_spell_in_spells(myself.spells, 0):
            # print('haste darimaaaaaaaaa---------------------------------------------------------------')
            if self.check_unit_in_units(world.get_me().units, all_base_units[0]):
                haste_units = my_units + world.get_friend().units
                if len(haste_units) > 2:
                    for unit in haste_units:
                        if self.distance_from_king(unit.cell, world.get_first_enemy().king.center) < 7 or\
                                self.distance_from_king(unit.cell, world.get_second_enemy().king.center) < 7:
                            last_unit = unit
                            received_spell = self.spell_in_spells(myself.spells, 0)
                            if last_unit.base_unit.type_id != 5:
                                world.cast_area_spell(center=last_unit.cell, spell=received_spell)
                                # print(f'{last_unit.unit_id} haste khord')

        if self.check_spell_in_spells(myself.spells, 1):
            # print('damage darimaaaaaaaaa---------------------------------------------------------------')
            if len(my_units) > 1:
                last_unit = my_units[0].target
                if last_unit is not None:
                    print(last_unit.unit_id)
                received_spell = self.spell_in_spells(myself.spells, 1)
                if last_unit is not None:
                    world.cast_area_spell(center=last_unit.cell, spell=received_spell)
                    # print(f'{last_unit.unit_id} damage khord')

        if self.check_spell_in_spells(myself.spells, 2):
            # print('heal darimaaaaaaaaa---------------------------------------------------------------')
            if len(my_units) > 2:
                last_unit = my_units[1]
                received_spell = self.spell_in_spells(myself.spells, 2)
                if last_unit.hp < last_unit.base_unit.max_hp - 1:
                    world.cast_area_spell(center=last_unit.cell, spell=received_spell)
                    # print(f'{last_unit.unit_id} heal khord')

        if self.check_spell_in_spells(myself.spells, 3):
            # print('tele darimaaaaaaaaa---------------------------------------------------------------')
            if self.check_unit_in_units(world.get_me().units, all_base_units[0]):
                if len(my_units) > 1:
                    last_unit = my_units[-1]
                    first_unit = my_units[0]
                    my_paths = myself.paths_from_player
                    path = my_paths[random.randint(0, len(my_paths) - 1)]
                    size = len(path.cells)
                    cell = path.cells[(int((size + 1) / 2)) - 3]
                    received_spell = self.spell_in_spells(myself.spells, 3)
                    if last_unit.base_unit.type_id == 0:
                        if self.distance_from_my_king(first_unit.cell, world) > self.distance_from_my_king(
                                path.cells[(int((size + 1) / 2)) - 3], world):
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
            if len(my_units) > 0:
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
    def get_max_hp(self, units):
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
                cell_for_our_loop = Cell(row_index, column_index)  # cell e marboot be in halghe
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

    def last_unit_enemy(self, units_1, units_2):
        units = units_1 + units_2
        return units[-1]

    def check_unit_in_hand(self, hand, unit):
        for item in hand:
            if item.type_id == unit.type_id:
                return True
        return False

    def check_unit_in_units(self, units, unit):
        for item in units:
            if item.base_unit.type_id == unit.type_id:
                return True
        return False

    def check_spell_in_spells(self, spells, spell_type_id):
        for item in spells:
            if item.type_id == spell_type_id:
                return True
        return False

    def spell_in_spells(self, spells, spell_type_id):
        for item in spells:
            if item.type_id == spell_type_id:
                return item

    def distance_from_my_king(self, cell, world):
        return abs(cell.col - world.get_me().king.center.col) + abs(cell.row - world.get_me().king.center.row)

    def logger(self, world):
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

    def check_friends_king(self, world):
        self.number_of_turns_after_last_put_to_friend += 1
        if not world.get_friend().king.is_alive:
            self.number_of_turns_after_friends_death += 1

        if self.number_of_turns_after_friends_death <= 3 and self.number_of_turns_after_friends_death > 0:
            if not self.put_the_most_damage_on_friend_path(world):
                self.put_the_cheapest_on_friend_path(world)
        elif self.number_of_turns_after_friends_death > 4:
            # print(f'{self.number_of_turns_after_last_put_to_friend} turns after friends last put')
            if self.number_of_turns_after_last_put_to_friend >= 4:
                if not self.put_the_most_damage_on_friend_path(world):
                    self.put_the_cheapest_on_friend_path(world)

    def put_the_cheapest_on_friend_path(self, world):
        cheapest_base_unit = world.get_me().hand[0]
        for base_unit in world.get_me().hand:
            if base_unit.ap < cheapest_base_unit.ap:
                cheapest_base_unit = base_unit
        if world.get_me().ap >= cheapest_base_unit.ap:
            world.put_unit(base_unit=cheapest_base_unit, path=world.get_friend().paths_from_player[0])
            self.number_of_turns_after_last_put_to_friend = 0
            return True
        return False

    def put_the_most_damage_on_friend_path(self, world):
        hand = world.get_me().hand
        sorted_hand = sorted(hand, key=lambda x: x.base_attack, reverse=True)
        my_ap = world.get_me().ap
        for base_unit in sorted_hand:
            if base_unit.ap <= my_ap:
                world.put_unit(base_unit=base_unit, path=world.get_friend().paths_from_player[0])
                self.number_of_turns_after_last_put_to_friend = 0
                return True
        return False

    def choose_and_put_unit(self, world, all_base_units):
        if world.get_current_turn() == 1:
            self.dade = 1
            world.put_unit(base_unit=all_base_units[1], path=world.get_me().paths_from_player[0])
            world.put_unit(base_unit=all_base_units[5], path=world.get_me().paths_from_player[0])

        if self.check_unit_in_hand(world.get_me().hand,
                                   all_base_units[0]) and self.dade == 0 and world.get_me().ap >= 4:
            world.put_unit(base_unit=all_base_units[0], path=world.get_me().paths_from_player[0])
            self.dade = 1

        if self.check_unit_in_hand(world.get_me().hand,
                                   all_base_units[1]) and self.dade == 0 and world.get_me().ap >= 3:
            world.put_unit(base_unit=all_base_units[1], path=world.get_me().paths_from_player[0])
            self.dade = 1

        if self.check_unit_in_hand(world.get_me().hand,
                                   all_base_units[6]) and self.dade == 0 and world.get_me().ap >= 2:
            world.put_unit(base_unit=all_base_units[6], path=world.get_me().paths_from_player[0])
            self.dade = 1

        if self.check_unit_in_hand(world.get_me().hand,
                                   all_base_units[2]) and self.dade == 0 and world.get_me().ap >= 4:
            world.put_unit(base_unit=all_base_units[2], path=world.get_me().paths_from_player[0])
            self.dade = 1

        if self.check_unit_in_hand(world.get_me().hand,
                                   all_base_units[5]) and self.dade == 0 and world.get_me().ap >= 3:
            world.put_unit(base_unit=all_base_units[5], path=world.get_me().paths_from_player[0])
            self.dade = 1

    '''agar yaremun roo masire ma chizi gozasht, ma ham roo masiresh yeki bezarim'''

    def should_put_unit_on_friends_path(self, world):
        if not self.could_put_unit_on_friends_path:
            # print('''agar as serie ghabl uniti moonde ke nazashti, bezar''')
            if self.put_the_most_damage_on_friend_path(world):
                # print('''agar tunest bezare''')
                self.could_put_unit_on_friends_path = 1

        if len(world.get_friend().units) > 0:
            friends_last_unit = world.get_friend().units[-1]
            my_paths = world.get_me().paths_from_player
            if self.last_friend_unit_on_my_way != None:
                # print('''Agar ta be hal roo masire man unit gozashte bud''')
                if self.last_friend_unit_on_my_way.unit_id != friends_last_unit.unit_id:
                    # print('''agar id e un ghablie ba id e akharin uniti ke tu bazi gozashte yeki nabud''')
                    '''(yani unit jadid gozashte bud)'''
                    if friends_last_unit.path == world.get_friend().path_to_friend or friends_last_unit.path in my_paths:
                        # print('''agar in jadide roo masire man bud''')
                        self.last_friend_unit_on_my_way = friends_last_unit  # update kon uno
                        if self.put_the_most_damage_on_friend_path(world):
                            # print('''agar poolet resid o gozashti''')
                            self.could_put_unit_on_friends_path = 1
                        else:
                            # print('''agar poolet naresid o nazashti''')
                            self.could_put_unit_on_friends_path = 0

            elif self.last_friend_unit_on_my_way == None:
                if friends_last_unit.path == world.get_friend().path_to_friend or friends_last_unit.path in my_paths:
                    '''agar ru masire man gozashte bud doostam'''
                    self.last_friend_unit_on_my_way = friends_last_unit
                    if self.put_the_most_damage_on_friend_path(world):
                        '''agar poolet resid o gozashti'''
                        self.could_put_unit_on_friends_path = 1
                    else:
                        '''agar poolet naresid o nazashti'''
                        self.could_put_unit_on_friends_path = 0

    def friend_is_empty(self, world):
        if len(world.get_friend().units) == 0:
            return True
        return False

    def help_friend(self, world):
        # print(f'number of turns after last put on friends way {self.number_of_turns_after_last_put_to_friend}')
        if self.number_of_turns_after_last_put_to_friend >= 3:
            if self.put_the_most_damage_on_friend_path(world):
                self.could_help_friend_while_hp_is_low = 1
                # print('could help')
            else:
                # print("couldn't help")
                self.could_help_friend_while_hp_is_low = 0

    def get_closest_enemy_path_and_dist(self, world, player):
        paths = player.paths_from_player
        nearest_cell = paths[0].cells[-1]
        nearest_path = paths[0]
        min_fasele = 10000
        for path in paths:
            cells = path.cells
            for cell in cells:
                # print(f'in cell ({cell.row} , {cell.col})')
                for unit in cell.units:
                    # print(f'on unit {unit.unit_id}')
                    if (unit.player_id != player.player_id) and (unit.player_id != world.get_friend().player_id):
                        print('the unit is an enemy')
                        fasele = self.faselecelltaking(world, cell)
                        if fasele < min_fasele:
                            print(f'min fasele ta alan ({min_fasele}) bigger than fasele alan({fasele})')
                            '''havaset bashe i < index ro didi faghat <= ro nazadi'''
                            min_fasele = fasele
                            nearest_cell = cell
                            nearest_path = path
                            print(f'nearest enemy of path {path.id} is on cell ({cell.row} , {cell.col})')
        t = (nearest_path, min_fasele)
        print(t)

        return t

    def get_friend(self, world, player):
        if player.player_id == 0:
            return world.get_player_by_id(2)
        elif player.player_id == 1:
            return world.get_player_by_id(3)
        elif player.player_id == 2:
            return world.get_player_by_id(0)
        elif player.player_id == 3:
            return world.get_player_by_id(1)

    def put_x_units_on_closest(self, world, x):
        if self.number_of_units_put_yet == x:
            self.closest_enemy_path = self.get_closest_enemy_path(world, world.get_me())
            self.number_of_units_put_yet = 0
        if self.number_of_units_put_yet < x:
            if self.put_unit_on_path(world, self.closest_enemy_path):
                print(f'put on path {self.closest_enemy_path.id}')
                self.number_of_units_put_yet += 1

    def put_unit_on_path(self, world, path):
        # 0>1>2>6>5
        all_base_units = world.get_all_base_units()
        if self.check_unit_in_hand(world.get_me().hand, all_base_units[0]) and world.get_me().ap >= 4:
            world.put_unit(base_unit=all_base_units[0], path=path)
            # print(f"put {0}")
            return True
        elif self.check_unit_in_hand(world.get_me().hand, all_base_units[1]) and world.get_me().ap >= 3:
            world.put_unit(base_unit=all_base_units[1], path=path)
            # print(f"put {1}")
            return True
        elif self.check_unit_in_hand(world.get_me().hand, all_base_units[2]) and world.get_me().ap >= 4:
            world.put_unit(base_unit=all_base_units[2], path=path)
            # print(f"put {2}")
            return True
        elif self.check_unit_in_hand(world.get_me().hand, all_base_units[6]) and world.get_me().ap >= 2:
            world.put_unit(base_unit=all_base_units[6], path=path)
            # print(f"put {6}")
            return True
        elif self.check_unit_in_hand(world.get_me().hand, all_base_units[5]) and world.get_me().ap >= 3:
            world.put_unit(base_unit=all_base_units[5], path=path)
            # print(f"put {5}")
            return True

        return False

    def myfunction(self, world):
        '''agar ye doshmani 8 ta ya kamtar fasele dasht, 3 ta befrest'''
        '''bayadbfrstm mige ke bayad ruye masire doshman befresti'''
        ''' '''
        if self.bayadbfrstm == True:
            """alan umade inja ke bfreste baraye defa"""
            """mikhaym ye bar dg nazdik tarin doshman ro peyda konim. shayad umade bashe tu ye masire dg nazdik tar"""
            minealan = self.get_closest_enemy_path_and_dist(world, world.get_me())
            if minealan[1] <= self.faselealanedoshman and minealan[0] != self.masir: #havasamam hast ke hamin masir ro dar nazar nagire
                self.faselealanedoshman = minealan[1]
                self.masir = minealan[0]
                self.bayadbfrstm = True #ghaedatan true e vali mahze ehtiat True kardamesh
                self.baredoshman = 0
            if self.put_defa(world, self.masir):
                self.baredoshman += 1
                print(f'be samte doshman ferestadam bare {self.baredoshman}om')
                if self.baredoshman == 3:
                    print('3 bar tamum shod')
                    self.bayadbfrstm = False
                    self.baredoshman = 0
                return
        elif self.bayadbfrstm == False:
            print('''hala bayad masir entekhab koni''')
            t = self.get_closest_enemy_path_and_dist(world, world.get_me())
            if t[1] <= 11:
                print(f'ye masire jadid baraye doshman peyda kardam: {t[0].id}')
                # print('''in yani bayad beshe masire jadidet''')
                self.faselealanedoshman = t[1]
                self.masir = t[0]
                self.bayadbfrstm = True
                # self.barekhali = 0
                # self.rukhalibfrstm = False
                '''hala ru masire jadid shoroo kon be gozashtan'''
                if self.put_defa(world, self.masir):
                    self.baredoshman += 1
                    print(f'be samte doshman ferestadam bare {self.baredoshman} om')
                return

            print('''hala farz kon nabayad befreste ru doshman o bazam true nashode bayadbfrstm''')
            if self.rukhalibfrstm == True:
                print('''bayad alan ru masire khale unit befrestim''')
                if self.put_unit_on_path(world, self.masirekhali):
                    self.barekhali += 1
                    print(f'ru masire khali ({self.masirekhali.id}) ferestadam bare {self.barekhali} om')
                    if self.barekhali == 3:
                        print('3 bare khali tamum shod')
                        self.rukhalibfrstm = False
                        self.barekhali = 0
                        return
            elif self.rukhalibfrstm == False:
                '''hala bayad masir entekhab koni'''
                print('vase khali hala mikham masir entekhab konam')
                masir = self.get_masirekhali(world)
                print(f'id e masire khali: {masir}')
                if masir.id != -1:
                    print(f'masire jadid vase khali entekhab kardam: {masir.id}')
                    '''masire jadid dari'''
                    self.masirekhali = masir
                    self.rukhalibfrstm = True
                    if self.put_unit_on_path(world, self.masirekhali):
                        self.barekhali = 1
                        print(f'ru masire khali gozashtam bare {self.barekhali} om')
                    return
                print('masiri khali nabud')

                '''hala farzkon khali ham nabud'''

                if self.put_unit_on_path(world, self.get_masireaslieyar(world)):
                    print('roo masire doostam gozashtam')

    def get_masirekhali(self, world):
        cut = 0
        myteampath = world.get_me().paths_from_player
        myteampath += world.get_friend().paths_from_player
        myteampath.append(world.get_me().path_to_friend)
        for path in myteampath:
            cut = 0
            print(f'masire {path.id}')
            for cell in path.cells:
                for unit in cell.units:
                    # print(f'ruye unit e {unit.unit_id}')
                    '''agar khasti begi kolan khali bashe, in sharto avaz kon'''
                    if unit.player_id == world.get_first_enemy().player_id or unit.player_id == world.get_second_enemy().player_id:
                        print('''yani ye doshman hast inja''')
                        if cell != world.get_first_enemy().king.center and cell != world.get_second_enemy().king.center:
                            cut = 1
                            print('shah ham nabud. cut 1 shod baghie unitaye cell ro dg lazem nist begardi')
                            break
                if cut == 1:
                    # print('baghie cell haye path ro lazem nist begardi')
                    break
            # if cut == 0:
            #     if path == world.get_me().path_to_friend:
            #         path = world.get_friend().paths_from_player[0]
            #     return path
        return Path(-1, [])

    def get_masireaslieyar(self, world):
        units = world.get_friend().units
        paths = []
        for path in world.get_map().paths:
            paths.append([path, 0])
        for unit in units:
            for item in paths:
                if item[0].id == unit.path.id:
                    item[1] += 1
        max = 0
        path = None
        for item in paths:
            if item[1] >= max:
                max = item[1]
                path = item[0]
        print(f'masire aslie yar: {path.id}')
        if max == 0:
            print("yar masire asli nadasht. be masire 0sh ferestadim")
            path = world.get_friend().paths_from_player[0]
        return path

    def fasele2tacell(self, avali, dovomi):
        return abs(avali.row - dovomi.row) + abs(avali.col - dovomi.col)

    def faselecelltaking(self,world,cell):
        row = world.get_me().king.center.row
        col = world.get_me().king.center.col
        king_area = [Cell(row-1,col-1), Cell(row-1, col), Cell(row-1, col+1), Cell(row, col-1), Cell(row, col), Cell(row, col+1), Cell(row+1, col-1), Cell(row+1, col), Cell(row+1, col+1)]
        min = 5000
        for khoone in king_area:
            fasele = self.fasele2tacell(cell, khoone)
            if fasele < min:
                min = fasele
        return min

    def distance_from_king(self,cell, king_cell):
        return abs(cell.col - king_cell.col) + abs(cell.row - king_cell.row)

    def minemasirbeshah(self,world):
        shortest = world.get_me().paths_from_player[0]
        length = len(world.get_me().paths_from_player[0].cells)
        for path in world.get_me().paths_from_player:
            pathlen = len(path.cells)
            if pathlen < length:
                '''ina dar soorati javab mide ke ma har masiri ke darim, tahesh doshman bashe'''
                '''agar tahe har masiri doshman nabud, bayad hamin kar ro beyne un masirayimun koni k tahesh doshmane'''
                length = pathlen
                shortest = path
        lenemasirbedoost = len(world.get_me().path_to_friend.cells)
        for path in world.get_friend().paths_from_player:
            pathlen = len(path.cells)
            if pathlen+lenemasirbedoost < length:
                length = pathlen+lenemasirbedoost
                shortest = path
        print(f'shorteste king {shortest.id} ba toole {length}')
        return shortest

    def put_defa(self, world, path):
        all_base_units = world.get_all_base_units()
        if self.check_unit_in_hand(world.get_me().hand, all_base_units[0]) and world.get_me().ap >= 4:
            world.put_unit(base_unit=all_base_units[0], path=path)
            # print(f"put {0}")
            return True
        elif self.check_unit_in_hand(world.get_me().hand, all_base_units[6]) and world.get_me().ap >= 2:
            world.put_unit(base_unit=all_base_units[6], path=path)
            # print(f"put {6}")
            return True
        elif self.check_unit_in_hand(world.get_me().hand, all_base_units[1]) and world.get_me().ap >= 3:
            world.put_unit(base_unit=all_base_units[1], path=path)
            # print(f"put {1}")
            return True
        elif self.check_unit_in_hand(world.get_me().hand, all_base_units[7]) and world.get_me().ap >= 5:
            world.put_unit(base_unit=all_base_units[7], path=path)
            return True
        elif self.check_unit_in_hand(world.get_me().hand, all_base_units[2]) and world.get_me().ap >= 4:
            world.put_unit(base_unit=all_base_units[2], path=path)
            # print(f"put {2}")
            return True
        return False