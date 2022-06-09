def topple(piles, row, col):
    '''
    Perform a single topple on the cell specified by its row and column
    '''
    piles = piles[:]
    height = len(piles)
    width = len(piles[0])
    pile = piles[row][col]
    if pile < 4:
        return piles
    piles[row][col] -= 4
    if row > 0:
        piles[row-1][col] += 1
    if row < height - 1:
        piles[row+1][col] += 1
    if col > 0:
        piles[row][col-1] += 1
    if col < width - 1:
        piles[row][col+1] += 1
    return piles

def complete_topple(piles):
    '''
    Topple all of the cells in the pile until the configuration is reduced.
    '''
    done = False
    while not done:
        done = True
        for row, row_pile in enumerate(piles):
            for col, cell in enumerate(row_pile):
                if cell > 3:
                    done = False
                    piles = topple(piles, row, col)
    return piles

def get_identity(width, height):
    '''
    Returns the rectangular configuration corresponding to the identity (zero) element of the sandpile group
    '''
    current_pile = [[3 for col in range(width)] for row in range(height)]
    next_pile = complete_topple([[3 + current_pile[row][col] for col in range(width)] for row in range(height)])
    while any(next_pile[row][col] != 3 for col in range(width) for row in range(height)):
        current_pile = next_pile[:]
        next_pile = complete_topple([[3 + current_pile[row][col] for col in range(width)] for row in range(height)])

    return current_pile

if __name__ == '__main__':
    print(get_identity(5,5))
