import model
import numpy as np


class MyStrategy:
    def __init__(self):
        pass

    def jumpcspace(self,game,cspace,x,y,maxht):
        if x<=0 or y<=0 or x>=20 or y>=29 or maxht==0 or game.level.tiles[x][y]==model.Tile.WALL:# or cspace[x][y]==1 :
            return
        self.createcspace(game,cspace,x,y)
        if game.level.tiles[x][y]==model.Tile.LADDER or game.level.tiles[x][y]==model.Tile.JUMP_PAD:
            return
        self.createcspace(game,cspace,x+1,y)
        self.createcspace(game,cspace,x-1,y)
        self.jumpcspace(game,cspace,x+1,y+1,maxht-1)
        self.jumpcspace(game,cspace,x-1,y+1,maxht-1)
        #if game.level.tiles[x]
        #if game.level.tiles[x+1][y]!=model.Tile.WALL:
        #   self.jumpcspace(game,cspace,x+1,y+1,maxht-1)
        #if game.level.tiles[x-1][y]!=model.Tile.WALL:
        #   self.jumpcspace(game,cspace,x-1,y+1,maxht-1)
        
            

    def createcspace(self,game,cspace,x,y):
        
        if x<=0 or y<=0 or x>=20 or y>=29 or cspace[x][y]==1:
            return
        if game.level.tiles[x][y]==model.Tile.WALL:
            return
        cspace[x][y],cspace[39-x][y]=1,1

        if game.level.tiles[x][y]==model.Tile.JUMP_PAD:
            self.jumpcspace(game,cspace,x,y+1,11)
            return
        if game.level.tiles[x][y]==model.Tile.LADDER:
            self.createcspace(game,cspace,x,y+1)
            self.createcspace(game,cspace,x,y-1)
            self.createcspace(game,cspace,x+1,y)
            self.createcspace(game,cspace,x-1,y)
            return
        if game.level.tiles[x][y-1]==model.Tile.PLATFORM or game.level.tiles[x][y-1]==model.Tile.LADDER:
            self.createcspace(game,cspace,x,y-1)
            self.createcspace(game,cspace,x+1,y)
            self.createcspace(game,cspace,x-1,y)
            self.jumpcspace(game,cspace,x,y+1,5)
        elif game.level.tiles[x][y-1]==model.Tile.EMPTY:
            self.createcspace(game,cspace,x,y-1)
            self.createcspace(game,cspace,x-1,y-1)
            self.createcspace(game,cspace,x+1,y-1)
        elif game.level.tiles[x][y-1]==model.Tile.WALL and game.level.tiles[x][y]!=model.Tile.LADDER:
            self.createcspace(game,cspace,x+1,y)
            self.createcspace(game,cspace,x-1,y)
            self.jumpcspace(game,cspace,x,y+1,5)
        





    def findnodes_wall(self,game):
        nodes=[]
        for j in range(0,29):
            y=j
            x=-1
            for i in range(1,39):
                if game.level.tiles[i][j]==model.Tile.WALL:
                    if x==-1:
                        if game.level.tiles[i][j+1]!=model.Tile.WALL:
                            x=i
                            nodes.append([x,y+1])
                            if game.level.tiles[i+1][j]==model.Tile.LADDER or game.level.tiles[i+1][j]==model.Tile.EMPTY or game.level.tiles[i+1][j]==model.Tile.PLATFORM or game.level.tiles[i+1][j+1]==model.Tile.WALL or game.level.tiles[i+1][j+1]==model.Tile.PLATFORM:
                                x=-1
                    else:
                        if game.level.tiles[i+1][j]==model.Tile.LADDER or game.level.tiles[i+1][j]==model.Tile.EMPTY or game.level.tiles[i+1][j+1]==model.Tile.WALL or game.level.tiles[i+1][j+1]==model.Tile.PLATFORM or game.level.tiles[i+1][j]==model.Tile.PLATFORM:
                            x=i
                            nodes.append([x,y+1])
                            x=-1
        print(nodes)

    def findnodes(self,game):
        nodes=[]
        for j in range(0,29):
            y=j
            x=-1
            for i in range(1,39):
                if game.level.tiles[i][j]==model.Tile.PLATFORM:
                    if x==-1:
                        if game.level.tiles[i][j+1]!=model.Tile.WALL:
                            x=i
                    if game.level.tiles[i][j+1]!=model.Tile.WALL:
                        if game.level.tiles[i+1][j]==model.Tile.WALL or game.level.tiles[i+1][j]==model.Tile.LADDER or game.level.tiles[i+1][j]==model.Tile.EMPTY or game.level.tiles[i+1][j+1]==model.Tile.WALL or game.level.tiles[i+1][j+1]==model.Tile.PLATFORM:
                            x+=i
                            nodes.append([x/2,y+1])
                            x=-1
        print(nodes)

    def findtarget(self,game,max):
        for j in range(1,max):
            for i in range(1,20):
                if game.level.tiles[20-i][29-j]==model.Tile.WALL or game.level.tiles[20-i][29-j]==model.Tile.PLATFORM:
                    return(20-i,30-j)

    def checkifjumpvalid(self,game,position,target_pos):
        
        for i in range(int(position.y),int(position.y)+12):
            if game.level.tiles[int(position.x)][i]==model.Tile.WALL:
                return False
            elif game.level.tiles[int(position.x)][i]==model.Tile.PLATFORM:
                return True
        return False

    def get_action(self, unit, game, debug):
        # Replace this code with your own
        def distance_sqr(a, b):
            return (a.x - b.x) ** 2 + (a.y - b.y) ** 2
        nearest_enemy = min(
            filter(lambda u: u.player_id != unit.player_id, game.units),
            key=lambda u: distance_sqr(u.position, unit.position),
            default=None)
        nearest_weapon = min(
            filter(lambda box: isinstance(
                box.item, model.Item.Weapon), game.loot_boxes),
            key=lambda box: distance_sqr(box.position, unit.position),
            default=None)
        print(nearest_enemy.position)
        target_pos = unit.position
        if unit.weapon is None and nearest_weapon is not None:
            target_pos = nearest_weapon.position
        elif nearest_enemy is not None:
            target_pos = nearest_enemy.position
        target_pos.x,target_pos.y=self.findtarget(game,29)

        debug.draw(model.CustomData.Log("Target pos: {}".format(target_pos)))
        aim = model.Vec2Double(0, 0)
        if nearest_enemy is not None:
            aim = model.Vec2Double(
                nearest_enemy.position.x - unit.position.x,
                nearest_enemy.position.y - unit.position.y)
        jump = target_pos.y > unit.position.y and self.checkifjumpvalid(game,unit.position,target_pos)
        if target_pos.x > unit.position.x and game.level.tiles[int(unit.position.x + 1)][int(unit.position.y)] == model.Tile.WALL:
            jump = True
        elif target_pos.x < unit.position.x and game.level.tiles[int(unit.position.x - 1)][int(unit.position.y)] == model.Tile.WALL:
            jump = True
        if target_pos.x > unit.position.x and game.level.tiles[int(unit.position.x)+1][int(unit.position.y-1)] == model.Tile.EMPTY:
            jump = True
        elif target_pos.x < unit.position.x and game.level.tiles[int(unit.position.x)-1][int(unit.position.y-1)] == model.Tile.EMPTY:
            jump = True
        #print(unit.position)
        #self.findnodes(game)
        #self.findnodes_wall(game)
        #cspace=np.zeros([40,30],dtype=int)
        #cspace=self.createcspace(game,cspace,int(unit.position.x),int(unit.position.y))
        #for row in cspace:
            #for val in row:
                #print(val,end='')
            #print()
        return model.UnitAction(
            velocity=target_pos.x - unit.position.x,
            jump=jump,
            jump_down=False,
            aim=aim,
            shoot=True,
            reload=False,
            swap_weapon=False,
            plant_mine=False)
