# -*- coding: utf-8 -*-
"""
Created on Sat May  9 11:53:20 2020

@author: jpnyvs
"""

import numpy as np
import pandas as pd


SIMULATION_TIME = 100

N_AGENTS = 30
RANGE_X = {'min':-30,'max':30}
RANGE_Y = {'min':-20,'max':20}


class Agent():
    def __init__(self, agent_name=None, agent_type=0):
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.step = 0
        self.location = {'x': np.random.randint(RANGE_X['min'], RANGE_X['max']), 
                         'y': np.random.randint(RANGE_Y['min'], RANGE_Y['max'])}
        #self.location_next = {'x_next':0, 'y_next':0}
        self.location_history = {'time':[self.step], 'x':[self.location['x']], 'y':[self.location['y']]}

    def next_location(self):
        x_next = self.location['x'] + np.random.randn()
        y_next = self.location['y'] + np.random.randn()
        
        if (x_next < RANGE_X['min']) or (x_next > RANGE_X['max']):
            x_next = self.location['x']
        if (y_next < RANGE_Y['min']) or (y_next > RANGE_Y['max']):
            y_next = self.location['y']
        
        self.step += 1
        self.location['x'] = x_next
        self.location['y'] = y_next
        self.location_history['time'].append(self.step)
        self.location_history['x'].append(x_next)
        self.location_history['y'].append(y_next)
    
    def print_name_location(self):
        print( "name={}, x={}, y={}".format(self.agent_name, self.location['x'], self.location['y']) )


class PlaySimulation():
    def __init__(self, n_agents=N_AGENTS):
        # 全Agentをインスタンス化
        self.agents = [Agent(agent_name=i) for i in range(n_agents)]
        
    def move_next_locations(self):
        """"全てのAgentを1ステップ進める"""
        for agent in self.agents:
            agent.next_location()
    
    def do_all_steps(self, n_steps=SIMULATION_TIME):
        """"全てのAgentでシミュレーションの全ステップ実施"""
        for i in range(n_steps):
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
        df.to_csv('sim2.csv', index=False)
        print('SAVED!!!')
        
    def print_agents_names_locations(self):
        for agent in self.agents:
            agent.print_name_location()
    



sim = PlaySimulation()
sim.agents

"""
sim.print_agents_names_locations()
sim.move_next_locations()
sim.print_agents_names_locations()
"""

sim.do_all_steps()

sim.get_simulated_data()


