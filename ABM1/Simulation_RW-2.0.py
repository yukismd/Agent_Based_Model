# -*- coding: utf-8 -*-
"""
Created on Wed May 13 09:32:04 2020

@author: jpnyvs
"""


import numpy as np
import pandas as pd


SIMULATION_ITERATION = 150
N_AGENTS = 15
## エージェントの1ステップ幅係数（正規分布からの乱数へかける値）
STEP_SIZE = 2
## 枠のサイズ（X方向、Y方向）
RANGE_X = {'min':-30,'max':30}
RANGE_Y = {'min':-20,'max':20}
## 次のステップを実施しないエージェント間の半径
STOP_DISTANCE = 1

SAVE_CSV_NAME = 'sim4.csv'


class Agent():
    def __init__(self, agent_name=None, agent_type=0, step_size=STEP_SIZE):
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.step_size = step_size
        self.step = 0    # 現在のステップ数
        self.location = {'x': np.random.randint(RANGE_X['min'], RANGE_X['max']), 
                         'y': np.random.randint(RANGE_Y['min'], RANGE_Y['max'])}    # 現在位置
        #self.location_next = {'x_next':0, 'y_next':0}
        self.location_history = {'time':[self.step], 'x':[self.location['x']], 'y':[self.location['y']]}

    def next_location(self):
        # 乱数で次へのステップを与える
        x_next = self.location['x'] + np.random.randn() * self.step_size
        y_next = self.location['y'] + np.random.randn() * self.step_size
        
        # 次のステップが枠外の場合、その軸へは移動しない
        if (x_next < RANGE_X['min']) or (x_next > RANGE_X['max']):
            x_next = self.location['x']
        if (y_next < RANGE_Y['min']) or (y_next > RANGE_Y['max']):
            y_next = self.location['y']
        
        # 次のステップに他エージェントが居た場合、移動をしない
        for agent_key, agent_location in main_agents_locations.items():
            if agent_key == self.agent_name:    # 自分との比較はスキップ
                continue
            # 自分の次の位置と他エージェント(agent_name_key)との距離比較
            distance = (x_next - agent_location['x'])**2 + (y_next - agent_location['y'])**2
            if distance < STOP_DISTANCE**2:
                print("Agent {} faces with another agent {}".format(self.agent_name ,agent_key))
                x_next = self.location['x']
                y_next = self.location['y']
                break
        
        self.step += 1
        self.location['x'] = x_next
        self.location['y'] = y_next
        self.location_history['time'].append(self.step)
        self.location_history['x'].append(x_next)
        self.location_history['y'].append(y_next)
    
    def print_name_location(self):
        print( "name={}, x={}, y={}".format(self.agent_name, self.location['x'], self.location['y']) )


class PlaySimulation():
        
    def move_next_locations(self, agents):
        """"全てのAgentを1ステップ進める"""
        for agent in agents:
            agent.next_location()
    
    def do_all_steps(self, agents, n_steps):
        """"全てのAgentでシミュレーションの全ステップ実施"""
        for i in range(n_steps):
            self.move_next_locations(agents)
            print("Step {} done.".format(i))
            #self.print_agents_names_locations()

    def get_simulated_data(self, agents):
        df = pd.DataFrame()
        for agent in agents:
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
        
    def print_agents_names_locations(self, agents):
        for agent in agents:
            agent.print_name_location()



# 全エージェントをインスタンス化（インスタンスをリストへ格納）
main_agents = [Agent(agent_name=i) for i in range(N_AGENTS)]
# 全エージェントの現在位置を格納 {名前:{'x':位置,'y':位置},..}
main_agents_locations = {main_agent.agent_name:main_agent.location for main_agent in main_agents}

#print(main_agents_locations)
sim = PlaySimulation()
sim.do_all_steps(main_agents, SIMULATION_ITERATION)
#print(main_agents_locations)
    
sim.get_simulated_data(main_agents)

