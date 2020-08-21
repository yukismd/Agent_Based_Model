# -*- coding: utf-8 -*-
"""
Created on Tue May 12 15:05:35 2020

@author: jpnyvs
"""

import numpy as np
import pandas as pd


SIMULATION_TIME = 100
N_AGENTS = 3

STEP_SIZE = 1.5
RANGE_X = {'min':-30,'max':30}
RANGE_Y = {'min':-20,'max':20}

SAVE_CSV_NAME = 'sim3.csv'


class Agent():
    def __init__(self, agent_name=None, agent_type=0, step_size=STEP_SIZE):
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.step_size = step_size
        self.step = 0
        self.location = {'x': np.random.randint(RANGE_X['min'], RANGE_X['max']), 
                         'y': np.random.randint(RANGE_Y['min'], RANGE_Y['max'])}
        #self.location_next = {'x_next':0, 'y_next':0}
        self.location_history = {'time':[self.step], 'x':[self.location['x']], 'y':[self.location['y']]}

    def next_location(self):
        x_next = self.location['x'] + np.random.randn() * self.step_size
        y_next = self.location['y'] + np.random.randn() * self.step_size
        
        # 枠外へ移動しないようにブロック
        if (x_next < RANGE_X['min']) or (x_next > RANGE_X['max']):
            x_next = self.location['x']
        if (y_next < RANGE_Y['min']) or (y_next > RANGE_Y['max']):
            y_next = self.location['y']
        
        # 移動先に他エージェントがいると動かない設定
        # TODO：　他のエージェントへのアクセス？
        #print(sim.agents)  # mainのインスタンスは取得可能
        
        
        self.step += 1
        self.location['x'] = x_next
        self.location['y'] = y_next
        self.location_history['time'].append(self.step)
        self.location_history['x'].append(x_next)
        self.location_history['y'].append(y_next)
    
    def print_name_location(self):
        print( "name={}, x={}, y={}".format(self.agent_name, self.location['x'], self.location['y']) )


class PlaySimulation():
    def __init__(self, n_agents=N_AGENTS, n_steps=SIMULATION_TIME):
        self.n_agents = n_agents
        self.n_steps = n_steps
        # 全エージェントをインスタンス化
        self.agents = [Agent(agent_name=i) for i in range(self.n_agents)]
        # 全エージェントの位置取得
        self.agents_locations = {agent.agent_name:agent.location for agent in self.agents}
        
    def move_next_locations(self):
        """"全てのAgentを1ステップ進める"""
        for agent in self.agents:
            agent.next_location()
    
    def do_all_steps(self):
        """"全てのAgentでシミュレーションの全ステップ実施"""
        for i in range(self.n_steps):
            self.move_next_locations()
            print("Step {} done.".format(i))
            #self.print_agents_names_locations()

    def get_simulated_data(self):
        df = pd.DataFrame()
        for agent in self.agents:
            if df.shape[0]==0:
                df = pd.DataFrame(agent.location_history)
                df['name'] = agent.agent_name
            else:
                df_tmp = pd.DataFrame(agent.location_history)
                df_tmp['name'] = agent.agent_name
                df = pd.concat([df, df_tmp])
            #print(agent.location_history)
        df = df[['name','time','x','y']]
        #print(df)
        df.to_csv(SAVE_CSV_NAME, index=False)
        print('SAVED!!!')
        
    def print_agents_names_locations(self):
        for agent in self.agents:
            agent.print_name_location()
    



sim = PlaySimulation()
sim.agents

sim.agents_locations

"""
sim.print_agents_names_locations()
sim.move_next_locations()
sim.print_agents_names_locations()
"""

sim.do_all_steps()

sim.get_simulated_data()


