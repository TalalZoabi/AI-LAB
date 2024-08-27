import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go


class Problem:
    def initialize_population(self):
        raise NotImplementedError

    def evaluate_fitness(self, candidate):
        raise NotImplementedError
    
    def display_individual(self, individual):
        raise NotImplementedError
    
    def distance(self, candidate1, candidate2):
        raise NotImplementedError
    
    def distance_unit(self):
        raise NotImplementedError









