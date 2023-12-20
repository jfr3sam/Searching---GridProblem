class Problem (object):
    
    def __init__(self, initial_state, goal_state=None):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def is_goal(self, state):
        if state == self.goal_state:
            return True

        return False

    def action_cost(self, state1, action, state2):
        return 1

    def h(self, node):
        return 0


class RouteProblem(Problem):
    
    def __init__(self, initial_state, goal_state = None, map_graph = None, map_coords = None):
        super().__init__(initial_state, goal_state)
        self.map_coords = map_coords
        self.map_graph = map_graph

        neighbors = {}
        for i in range(len(list(map_graph.keys()))):
            if list(map_graph.keys())[i][0] not in neighbors:
                neighbors[list(map_graph.keys())[i][0]] = (
                    list(map_graph.keys())[i][1],)
            else:
                t = neighbors[list(map_graph.keys())[i][0]]
                neighbors[list(map_graph.keys())[i][0]] = t + \
                    (list(map_graph.keys())[i][1],)

        self.neighbors = neighbors

    def actions(self, state):
        lst = []
        if state not in self.neighbors:
            return lst

        a = self.neighbors[state]

        for i in range(len(a)):
            lst.append(a[i])

        return lst



    def result(self, state, action):

        if action in self.actions(state):
            return action
        else:
            return state



    def action_cost(self, state1, action, state2):

        if action in self.actions(state1):
            return self.map_graph[(state1, action)]



    def h(self, node):
        if (node.state == self.goal_state):
            return 0
        x1, y1 = self.map_coords[node.state]
        x2, y2 = self.map_coords[self.goal_state]
        return ((x2-x1) ** 2 + (y2 - y1) ** 2) ** 0.5


class GridProblem(Problem):
    
    def __init__(self, initial_state, N, M, wall_coords, food_coords):
        super().__init__(initial_state, goal_state = None)
        self.N = N      
        self.M = M      
        self.wall_coords = wall_coords
        self.food_coords = food_coords

        food_eaten = ()

        for i in food_coords:
            food_eaten += (False,)

        self.initial_state = (initial_state, food_eaten)  



    def actions(self, state):
        rows = self.N        
        col = self.M            
        x, y = state[0] 

        lst = []

        if (y+1) <= rows and (x, y + 1) not in self.wall_coords:
            lst.append('up')

        if (y-1) >= 1 and (x, y - 1) not in self.wall_coords:
            lst.append('down')

        if ((x + 1) <= col) and (x + 1, y) not in self.wall_coords:
            lst.append('right')

        if ((x - 1) >= 1) and (x - 1, y) not in self.wall_coords:
            lst.append('left')

        return lst

    def result(self, state, action):

        if action not in self.actions(state):
            return state

        state = list(state)
        if action == 'up':
            x, y = state[0]
            state[0] = (x, y + 1)
        elif action == 'down':
            x, y = state[0]
            state[0] = (x, y - 1)
        elif action == 'right':
            x, y = state[0]
            state[0] = (x + 1, y)

        elif action == 'left':
            x, y = state[0]
            state[0] = (x - 1, y)

        if state[0] in self.food_coords:

            index = -1
            for i in range(len(self.food_coords)):
                if self.food_coords[i] == state[0]:
                    index = i
                    break

            food_eaten = list(state[1])
            food_eaten[index] = True
            state[1] = tuple(food_eaten)

        state = tuple(state)
        return state
  
  
  
    def action_cost(self, state1, action, state2):
        return 1



    def is_goal(self, state):

        for i in state[1]:
            if i == False:
                return False

        return True




    def h(self, node):

        if self.is_goal(node.state):
            return 0

        foods = self.food_coords
        currloc = node.state[0]
        eaten = node.state[1]
        eaten = list(eaten)
        loc_food = []

        for i in range(len(foods)):  
            if eaten[i] == False:
                loc_food.append(foods[i])

        lst = []

        for i in range(len(loc_food)):
            x1, y1 = currloc
            x2, y2 = loc_food[i]

            lst.append(abs(x2 - x1) + abs(y2 - y1))

        return min(lst)