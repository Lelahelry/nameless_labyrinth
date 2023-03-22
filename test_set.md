the tiles
I do one list of fixed tile, one of moving
``` json
{ "fixed":    [{"filepath":'', 
    "sides":[False, True, True, False],
    "position":(0,0) ,
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[False, False, True, True],
    "position":(0,6) ,
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, False, False, True],
    "position":(6,6) ,
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, True, False, False],
    "position":(6,0) ,
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[False, True, True, True],
    "position":(0,2) ,
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[False, True, True, True],
    "position":(0,4) ,
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[False, True, True, True],
    "position":(2,4) ,
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, True, True, False],
    "position":(2,0) ,
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, True, True, False],
    "position":(4,0) ,
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, True, True, False],
    "position":(2,2) ,
    "treasure":None,
    "pawn":None },


    {"filepath":'', 
    "sides":[True, False, True, True],
    "position":(2,6) ,
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, False, True, True],
    "position":(4,6) ,
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, False, True, True],
    "position":(4,4) ,
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, True, False, True],
    "position":(4,2) ,
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, True, False, True],
    "position":(6,2) ,
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, True, False, True],
    "position":(6,4) ,
    "treasure":None,
    "pawn":None },
    ] ,
    "moving":
    [{"filepath":'', 
    "sides":[True, True, False, False],
    "treasure":None,
    "pawn":None },
    
    {"filepath":'', 
    "sides":[False, True, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[False, True, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[False, True, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[False, True, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[False, True, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[False, True, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[False, True, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[False, True, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[False, True, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[False, True, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[False, True, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[False, True, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[False, True, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[False, True, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[False, True, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, False, True, False],
    "treasure":None,
    "pawn":None },
    
    {"filepath":'', 
    "sides":[True, False, True, False],
    "treasure":None,
    "pawn":None },
    
    {"filepath":'', 
    "sides":[True, False, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, False, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, False, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, False, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, False, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, False, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, False, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, False, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, False, True, False],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, True, False, True],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, True, False, True],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, True, False, True],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, True, False, True],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, True, False, True],
    "treasure":None,
    "pawn":None },

    {"filepath":'', 
    "sides":[True, True, False, True],
    "treasure":None,
    "pawn":None }

    ]

}
```

the grid
```py
grid={(0,0):TileA, }

