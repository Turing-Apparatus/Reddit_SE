from random import shuffle


def solve(s,x,y):

    global B, found

    if s==N:
        B[x][y] = s
        found = True
        print '\n\n', n
        print_board()

    if not found:
        B[x][y] = s
        cost    = sorted ( (sum(B[i][j]==0  for i,j in A[nx][ny]), (nx,ny))
                                            for nx,ny in A[x][y] if B[nx][ny]==0 )
        greedy  = [ cost[i][1]              for i in xrange(len(cost))
                                            if  cost[i][0]==cost[0][0] ]
        shuffle(greedy)
        for gx,gy in greedy: solve(s+1, gx, gy)
        B[x][y] = 0




def print_board():

    w = len(str(N))
    for i in xrange(n):
        for j in xrange(n):
            print str(B[i][j]).rjust(w),
        print ''




if __name__ == '__main__':

    for n in xrange(5,31):
        N=n*n
        moves = [(0,3),(0,-3),(3,0),(-3,0),(2,2),(2,-2),(-2,2),(-2,-2)]
        A = [[[(i+x,j+y)   for x,y in moves if 0<=i+x<n and 0<=j+y<n]
                            for j in xrange(n)]
                            for i in xrange(n)]
        B = [[0]*n for i in xrange(n)]
        found = False
        solve(1,0,0)

