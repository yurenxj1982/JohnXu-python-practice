#! /usr/bin/env python3
# -*- coding: utf-8 -*-

r'''

这是一个随机发牌程序的练习
问题描述：
    1) 程序的使用方法:
    $ poker-dealer  [-h | --help] [-p|--number players] [--with[out]-joker]
        -p --players           how many player, default is 4
           --with[out]-joker   enable joker, default is --with-joker
        -h                     show this
目的:
    熟悉随机函数
    熟悉Enum的使用
    熟悉命令行getopt操作

'''

__author__ = 'xujun'


from enum import Enum
import random


def usage(name):

    ''' print usage '''

    helpstr = '''usage:
{0}  [-h | --help] [-p|--number players] [--with[out]-joker]
       -p  --players           how many player, default is 4
           --without-joker     without joker
       -h  --help              show this
    '''.format(name)
    print(helpstr)



Pointer = Enum(
    'Pointer',
    ['Joker', 'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'],
    module=__name__
    )

Color = Enum(
    'Color',
    ['Black', 'Color', 'Spade', 'Heart', 'Diamond', 'Club'],
    module=__name__
    )

class PokerCard(object):
    r'''
    Poker Card
    '''
    def __init__(self, pointer, color):
        self.pointer = pointer
        self.color = color

    def __repr__(self):
        return "{0}:{1}".format(self.color.name, self.pointer.name)




class PokerFactory(object):
    r'''
        The Poker Factory
    '''

    def __init__(self, enable_joker=True):
        r'''
            PokerFactory __init__
        '''
        self.cards = [PokerCard(x, y) for x in list(Pointer)[1:] for y in list(Color)[2:]]

        if enable_joker:
            self.cards += [PokerCard(Pointer.Joker, Color.Black),
                           PokerCard(Pointer.Joker, Color.Color)]

    def getPoker(self):
        r'''
            get a poker copy
        '''

        return self.cards[:]




def deal(cards, player_counts=4):
    r'''
    deal function

    '''

    players = {}
    for i in range(player_counts):
        players['Player_{0}'.format(i + 1)] = []

    player_index = 0
    while cards:
        card = cards.pop(random.randrange(len(cards)))
        players['Player_{0}'.format(player_index + 1)].append(card)
        player_index = (player_index + 1) % player_counts

    return players



if __name__ == '__main__':
    import sys
    import os
    import getopt
    dirname, filename = os.path.split(sys.argv[0])

    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "hp:", ["help", "numbers=", "without-joker"])
    except getopt.GetoptError as err:
        print(err)
        usage(filename)
        sys.exit(2)

    params = {
        'players': 4,
        'with-joker': True
        }

    for o, a in opts:
        if o in ('-h', '--help'):
            usage(filename)
            sys.exit()
        elif o in ('-p', '--players'):
            params['players'] = int(a)
        elif o == '--without-joker':
            params['with-joker'] = False

    pokerFactory = PokerFactory(params['with-joker'])

    players_cards = deal(cards=pokerFactory.getPoker(), player_counts=params['players'])


    for player, cards in players_cards.items():
        print(player, "has {0} cards".format(len(cards)), ":", cards, end='\n\n')
