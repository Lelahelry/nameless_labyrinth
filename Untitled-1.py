from labyrinth import Pawn, Treasure
    
t1=Treasure("1","a")
t2=Treasure("1","b")
t3=Treasure("1","c")
t4=Treasure("1","d")
t5=Treasure("1","e")

p1=Pawn("blue","léa",[t1,t2,t3])
p2=Pawn("red","clem",[t4,t5])


print(p1.__repr__(), p2.__repr__())

print(p1.current_objective())

p1.collect()

p2.collect()
p2.collect()
print(p1.__repr__())
print(p2.__repr__())