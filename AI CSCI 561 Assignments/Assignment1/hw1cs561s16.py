import sys

def copyboard(src,dest):
    dest=[]
    for i in range(len(src)):
        dest.append([])
        for j in range(len(src)):
            dest[i].append(src[i][j])
    return dest[:]

def copyarray(src,dest):
    for i in range(len(src)):
        dest.append(src[i])
    return dest


def printarray(a):
    for i in range(len(a)):
        tmp = ""
        for j in range(len(a[i])):
            tmp = tmp + str(a[i][j]) + " "
        print tmp


def calculate_initial_weight(weights, board, player, opponent):
    #printarray(board)
    #printarray(weights)
    #print player,opponent
    length_weights = len(weights)
    player_weight = 0
    opponent_weight = 0
    for i in range(length_weights):
        for j in range(length_weights):
            if board[i][j] == player:
                player_weight = player_weight + weights[i][j]
            elif board[i][j] == opponent:
                opponent_weight = opponent_weight + weights[i][j]
    return player_weight, opponent_weight



def computeweight1(weights, next_state, i, j, opponent, tempweight, initial_weight):
    length_weights = len(weights)
    for m in range(-1, 2):
        for k in range(-1, 2):
            if (i + m >= 0 and i + m < length_weights and j + k >= 0 and j + k < length_weights and (
                                i + m == i or j + k == j) and next_state[i + m][j + k] == '*'):
                tempweight[i + m][j + k] = computeweight2(weights, next_state, i + m, j + k, opponent, initial_weight)


def computeweight2(weights, next_state, i, j, opponent, initial_weight):
    length_weights = len(weights)

    player_weight = initial_weight[0] + weights[i][j]
    opponent_weight = initial_weight[1]
    for m in range(-1, 2):
        for n in range(-1, 2):
            if (i + m >= 0 and i + m < length_weights and j + n >= 0 and j + n < length_weights and (
                                i + m == i or j + n == j) and next_state[i + m][j + n] == opponent):
                player_weight = player_weight + weights[i + m][j + n]
                opponent_weight = opponent_weight - weights[i + m][j + n]
    return int(player_weight - opponent_weight)


def play(weights, board, player, opponent, initial_weight):
    # copy to create a new array and keep the original array as is
    next_state = board
    length_weights=len(weights)
    tempweight = []
    for i in range(len(weights)):
        tempweight.append([])
        for j in range(len(weights[i])):
            tempweight[i].append(-999999999)

    max_sneak = 0
    sneak_i = 0
    sneak_j = 0
    for i in range(len(weights)):
        for j in range(len(weights[i])):
            if (next_state[i][j] == player):
                computeweight1(weights, next_state, i, j, opponent, tempweight, initial_weight)
            else:
                if board[i][j] == '*' and max_sneak < weights[i][j]:
                    max_sneak = weights[i][j]
                    sneak_i = i
                    sneak_j = j

    printarray(weights)
    printarray(board)
    print max_sneak
    if player == 'X':
        max_sneak = initial_weight[0] + max_sneak
        sneak_weight = max_sneak - initial_weight[1]
    else:
        max_sneak = initial_weight[1] + max_sneak
        sneak_weight = max_sneak - initial_weight[0]

    #printarray(tempweight)
    max_raid = -999999999
    raid_i = 0
    raid_j = 0
    for i in range(len(tempweight)):
        for j in range(len(tempweight[i])):
            if max_raid < tempweight[i][j] and tempweight[i][j]<>-999999999:
                max_raid = tempweight[i][j]
                raid_i = i
                raid_j = j

    print max_raid,sneak_weight
    out_weight = 0;
    out_i = 0
    out_j = 0

    printarray(tempweight)
    if max_raid > sneak_weight:
        out_weight = max_raid
        out_i = raid_i
        out_j = raid_j
        for idxi in range(-1,2):
            for idxj in range(-1,2):
                print out_i , idxi ,length_weights ,out_j + idxj ,next_state[out_i + idxi][out_j + idxj]
                if (out_i + idxi >= 0 and out_i + idxi < length_weights and out_j + idxj >= 0 and out_j + idxj < length_weights and (
                                out_i + idxi == out_i or out_j + idxj == out_j) and next_state[out_i + idxi][out_j + idxj] == opponent):
                    print "Inside opponent"
                    board[out_i + idxi][out_j + idxj]=player

    elif max_raid < sneak_weight:
        out_weight = sneak_weight
        out_i = sneak_i
        out_j = sneak_j
    elif (raid_i * 10 + raid_j) <= (sneak_i * 10 + sneak_j):
        out_weight = max_raid
        out_i = raid_i
        out_j = raid_j
        for idxi in range(-1,2):
            for idxj in range(-1,2):
                if (out_i + idxi >= 0 and out_i + idxi < length_weights and out_j + idxj >= 0 and out_j + idxj < length_weights and (
                                out_i + idxi == out_i or out_j + idxj == out_j) and next_state[out_i + idxi][out_j + idxj] == opponent):
                    print "Inside opponent"
                    board[out_i + idxi][out_j + idxj]=player

    else:
        out_weight = sneak_weight
        out_i = sneak_i
        out_j = sneak_j

    return (out_weight, out_i, out_j)



def call_greedy():
    global board
    initial_weight = calculate_initial_weight(weights, board, player, opponent)


    nxt_move = play(weights, board, player, opponent, initial_weight)
    #print nxt_move
    board[nxt_move[1]][nxt_move[2]] = player



    outfile = open("next_state.txt",'w')
    for i in range(len(board)):
        temp = ""
        for j in range(len(board[i])):
            temp = temp + board[i][j]
        outfile.write(temp + "\n")
    outfile.close()




"""
Minimax starts here

"""

def minimax(board,local_board,player,opponent,level):
    global cnt,exhaustive_arr,min_max_arr,node_list,player_bkp,opponent_bkp
    length_weights=len(weights)

    local_board=copyboard(board,local_board)
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == '*':
                board[i][j] = player

                if level<in_level:
                    inf=None
                    if level%2==0:
                        inf='-Infinity'
                    else:
                        inf='Infinity'
                    arr=[chr(65+j)+str(i+1),level,inf]
                    exhaustive_arr.append(arr)
                    min_max_arr.append(arr)

                for m in range(-1,2):
                    for n in range(-1,2):
                        if (i+m >= 0 and i+m < length_weights and j+n >= 0 and j+n < length_weights and (i+m==i or j+n==j) and (m+n<>0) and board[i+m][j+n]==player):
                            for x in range(-1,2):
                                for y in range(-1,2):
                                    if (i+x >= 0 and i+x < length_weights and j+y>= 0 and j+y < length_weights and (i+x==i or j+y==j) and (x+y<>0) and board[i+x][j+y]==opponent):
                                        board[i+x][j+y]=player
                if (level==in_level):
                    temp_cost=calculate_initial_weight(weights,board,player_bkp,opponent_bkp)
                   # print "temp_cost=",temp_cost,player_bkp,opponent_bkp

                    board=copyboard(local_board,board)
                    arr=[chr(65+j)+str(i+1),level,temp_cost[0]-temp_cost[1]]
                    exhaustive_arr.append(arr)
                    min_max_arr.append(arr)

                    prev_low_lvl_idx=0
                    for idx in range(len(exhaustive_arr)):
                        if exhaustive_arr[idx][1]==level-1:
                            prev_low_lvl_idx=idx

                    for i_idx in range(prev_low_lvl_idx,len(exhaustive_arr)):
                        for j_idx in range(prev_low_lvl_idx+1,len(exhaustive_arr)):
                            if exhaustive_arr[i_idx][1]<exhaustive_arr[j_idx][1]:
                                if level%2==0: #Min for even levels
                                    if exhaustive_arr[i_idx][2]>exhaustive_arr[j_idx][2]:
                                        a=list([exhaustive_arr[i_idx][0],exhaustive_arr[i_idx][1],exhaustive_arr[j_idx][2]])
                                        exhaustive_arr.append(a)
                                    else:
                                        a=list(exhaustive_arr[i_idx])
                                        exhaustive_arr.append(a)
                                else: #Max for odd levels
                                    if exhaustive_arr[i_idx][2]<exhaustive_arr[j_idx][2] or exhaustive_arr[i_idx][2] in (['-Infinity','Infinity']):
                                        a=list([exhaustive_arr[i_idx][0],exhaustive_arr[i_idx][1],exhaustive_arr[j_idx][2]])
                                        exhaustive_arr.append(a)
                                    else:
                                        a=list(exhaustive_arr[i_idx])
                                        exhaustive_arr.append(a)





                else:
                    minimax(board,local_board,opponent,player,level=level+1)


            if level<in_level:
                board=copyboard(local_board,board)




def searchNodeList(src,srch):
   # print "srch",srch
    i=-1
    for i in range(len(src)):
        if [src[i][0],src[i][1],src[i][2]]==srch:
            break#return i
    return i




def getMiniMaxNodeRange():
    global min_max_arr,in_level
    for i in range(len(node_list)):
        for j in range(len(node_list[i])):
            if i==in_level:
                node_list[i][j].append(node_list[i][j][3])
            else:
                cntr=0
                for k in range(node_list[i][j][3]+1,len(min_max_arr)):
                    if [min_max_arr[k][1],min_max_arr[k][2]]==[node_list[i][j][1],node_list[i][j][2]]:
                        break
                    else:
                        cntr=cntr+1
                node_list[i][j].append(cntr)



def minimax_print(node,depth,maximizingPlayer):
    global minimax_output,node_list
    #print "In minimax nodelist:"
    #printarray(node_list)
    if (depth==0 or depth==in_level ) and node[2] not in ('Infinity','-Infinity'):
        minimax_output.append([node[0],node[1],node[2]])
        return node[2]
    if maximizingPlayer:
        bs='-Infinity'
        print "Max Player:",node
        #print node[1]+1,len(node_list[node[1]+1])
        minimax_output.append([node[0],node[1],node[2]])
        #print range(int(node[3]),int(node[3])+int(node[4])+1)
        for i in range(len(node_list[node[1]+1])):

            if node_list[node[1]+1][i][3] in range(int(node[3]),int(node[3])+int(node[4])+1):
     #           print "call via para",node_list[node[1]+1][i]
       #         print node_list[node[1]+1][i][1],False,node[1]
                v=minimax_print(node_list[node[1]+1][i],node_list[node[1]+1][i][1],False)
      #          print "alpha,v :",v
                if bs in ('-Infinity','Infinity'):
                    bs=v
                else:
                    bs=max(bs,v)
                #print "Prev State:",node_list[node[1]+1][i]
                node[2]=bs

                #print "next node=",node_list[node[1]+1][i]
                #alphabeta_output.append([node_list[node[1]+1][i][0],node_list[node[1]+1][i][1],node_list[node[1]+1][i][2],node_list[node[1]+1][i][5],node_list[node[1]+1][i][6]])
                print "For node %s  v %s"%(node,v)
                minimax_output.append([node[0],node[1],node[2]])

        #print v
        return bs
    else:
        bs='Infinity'
        #print "Min Player:",node#,node_list[node[1]+1],len(node_list[node[1]+1])
        minimax_output.append([node[0],node[1],node[2]])
        for i in range(len(node_list[node[1]+1])):
            if node_list[node[1]+1][i][3] in range(node[3],node[3]+node[4]+1):
      #          print "call via para",node_list[node[1]+1][i],node_list[node[1]+1][i][2],alpha,beta,False
                v=minimax_print(node=node_list[node[1]+1][i],depth=node_list[node[1]+1][i][1],maximizingPlayer=True)
                if bs in ('-Infinity','Infinity'):
                    backup_beta=bs
                    bs=v
                else:
                    print "bs",bs
                    backup_beta=bs
                    bs=min(bs,v)
                #print "Prev State:",node_list[node[1]+1][i]
                node[2]=bs

                #print "next node=",node_list[node[1]+1][i]
                #alphabeta_output.append([node_list[node[1]+1][i][0],node_list[node[1]+1][i][1],node_list[node[1]+1][i][2],node_list[node[1]+1][i][5],node_list[node[1]+1][i][6]])
                print "For node %s  v %s"%(node,v)
                #alphabeta_output.append([node[0],node[1],node[2],alpha,beta])
                minimax_output.append([node[0],node[1],node[2]])
        #print v
        return bs









def print_minimax():
    global board,node_list,final_out,orig_board
    for i in reversed(range(len(final_out))):
        if final_out[i][0]=='root':
            break
    #print "Final output:",final_out
    j=0
    for j in range(len(node_list[1])):
        if node_list[1][j][2]==final_out[i][2]:
            break
    #print "Level 1 value for board",node_list[1][j]

    #chk_out=False
    #printarray(orig_board)

    y=ord(node_list[1][j][0][0])-65

    temp=''
    for k in range(1,len(node_list[1][j][0])):
        temp=temp+node_list[1][j][0][k]

    x=int(temp)-1
    #print x,y
    length_weights=len(orig_board)
    next_state=[]
    next_state=copyboard(orig_board,next_state)
    for m in range(-1, 2):
        for k in range(-1, 2):
            ##print x + m ,y + k,next_state[x + m][y + k]
            if (x + m >= 0 and x + m < length_weights and y + k >= 0 and y + k < length_weights and (
                x + m == x or y + k == y) and next_state[x + m][y + k] == player):
                for i in range(-1,2):
                    for j in range(-1,2):
                        if (x + i >= 0 and x + i < length_weights and y + j >= 0 and y + j < length_weights and (
                                    x + i == x or y + j == y) and next_state[x + i][y + j] == opponent):
                            orig_board[x + i][y + j]=player
    orig_board[x][y]=player

    board=copyboard(orig_board,board)
    #print "Final Board:"
    #printarray(orig_board)


    outfile = open("next_state.txt",'w')
    for i in range(len(orig_board)):
        temp = ""
        for j in range(len(orig_board[i])):
            temp = temp + orig_board[i][j]
        outfile.write(temp + "\n")
    outfile.close()

    outfile = open("traverse_log.txt",'w')
    outfile.write("Node,Depth,Value\n")
    for i in range(len(final_out)):
        outfile.write(str(final_out[i][0])+","+str(final_out[i][1])+","+str(final_out[i][2])+"\n")
    outfile.close()












def call_algos():
    global node_list,min_max_arr,final_out,alphabeta_output,board,player,opponent,in_level
    cntr=0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j]=='*':
                cntr=cntr+1
    print "cntr=",cntr
    if cntr<in_level:
        in_level=cntr

    if Algo_type==1:
        call_greedy()

    elif Algo_type==2:
        min_max_arr=[]
        min_max_arr.append(['root',0,'-Infinity'])
        exhaustive_arr=[]
        exhaustive_arr.append(['root',0,'-Infinity'])

        minimax(board,board,player,opponent,1)
        node_list=[]
        for i in range(in_level+1):
            node_list.append([])
        #Copying from min_max_arr to node_list (tree)
        #adding one more column to track the min_max_arr idx column no 3 (starting from 0)
        for i in range(len(min_max_arr)):
            a=list(min_max_arr[i])
            if min_max_arr[i][1]==in_level:
                a.append(i)
            else:
                a.append(i)
            node_list[min_max_arr[i][1]].append(a)
       # print "MIN MAX ARRAY"
      #  printarray(min_max_arr)
        #printarray(node_list)

        #adding two more columns to parent nodes whihc contains the range of child idx (column no 4,5)
        getMiniMaxNodeRange()
        #printarray(node_list)
        final_out=[]
        #print_output(node_list,node_list[0][0][1],node_list[0][0][3],[node_list[0][0][4],node_list[0][0][5]])

      #  print "Nodelist before output:",node_list
        minimax_print(node_list[0][0],node_list[0][0][1],True)
        final_out=minimax_output
        print_minimax()

    elif Algo_type==3:
       # print "In Algo 3"
        min_max_arr=[]
        min_max_arr.append(['root',0,'-Infinity'])
        exhaustive_arr=[]
        exhaustive_arr.append(['root',0,'-Infinity'])
        cnt=1

        minimax(board,board,player,opponent,1)
      #  print "MINIMAX",min_max_arr
        node_list=[]
        for i in range(in_level+1):
            node_list.append([])

        #print node_list

        #Copying from min_max_arr to node_list (tree)
        #adding one more column to track the min_max_arr idx column no 3 (starting from 0)
        cntr=0
        for i in range(len(min_max_arr)):
            a=list(min_max_arr[i])
            if min_max_arr[i][1]==in_level:
                a.append(i)
            else:
                a.append(i)

            node_list[min_max_arr[i][1]].append(a)
        getAlphaBetaNodeRange()
        printarray(node_list)
        alphabeta_output=[]
        alphabeta(node_list[0][0],node_list[0][0][1],node_list[0][0][5],node_list[0][0][6],True)

        alphabeta_print()






"""
Alpha Beta starts here
"""


def alphabeta(node,depth,alpha,beta,maximizingPlayer):
   # print "alpha,beta",alpha,beta
    global alphabeta_output,node_list,in_level
    print "in_level=",depth,in_level
    backup_beta=None
    backup_alpha=None
    #print "Depth =",depth,maximizingPlayer
    if (depth==0 or depth==in_level ) and node[2] not in ('Infinity','-Infinity'):
       # print "In return :",node,alpha,beta
        alphabeta_output.append([node[0],node[1],node[2],alpha,beta])
        #temp_cost=calculate_initial_weight(weights,board,player_bkp,opponent_bkp)
        print "Depth =0 or in_level",node[2]
        return node[2]
    if maximizingPlayer:
        v='-Infinity'
      #  print "Max Player:",node#,node_list[node[1]+1],len(node_list[node[1]+1])
        alphabeta_output.append([node[0],node[1],node[2],alpha,beta])
        print node[3],node[3],node[4],len(node_list[node[1]+1])
        for i in range(len(node_list[node[1]+1])):

            if node_list[node[1]+1][i][3] in range(int(node[3]),int(node[3])+int(node[4])+1):
       #         print "call via para",node_list[node[1]+1][i],node_list[node[1]+1][i][2],alpha,beta,False
                if v in ('-Infinity','Infinity'):
                    v=alphabeta(node=node_list[node[1]+1][i],depth=node_list[node[1]+1][i][1],alpha=alpha,beta=beta,maximizingPlayer=False)
                else:
                    v=max(v,alphabeta(node=node_list[node[1]+1][i],depth=node_list[node[1]+1][i][1],alpha=alpha,beta=beta,maximizingPlayer=False))
             #   print "alpha,v :",alpha,v
                if alpha in ('-Infinity','Infinity'):
                    backup_alpha=alpha
                    alpha=v
                else:
                    backup_alpha=alpha
                    alpha=max(alpha,v)


                #print "Prev State:",node_list[node[1]+1][i]
                node_list[node[1]+1][i][5]=alpha
                node[5]=alpha
                node[2]=alpha

                #print "next node=",node_list[node[1]+1][i]
                #alphabeta_output.append([node_list[node[1]+1][i][0],node_list[node[1]+1][i][1],node_list[node[1]+1][i][2],node_list[node[1]+1][i][5],node_list[node[1]+1][i][6]])
              #  print "For node %s alpha %s beta %s, v %s, alphabeta %s"%(node,alpha,beta,v,backup_alpha)
                #alphabeta_output.append([node[0],node[1],node[2],alpha,beta])
                if beta not in ('Infinity','-Infinity') and alpha not in ('Infinity','-Infinity') and  beta<=alpha:
                    alphabeta_output.append([node[0],node[1],node[2],backup_alpha,beta])
        #            print "Beta less than alpha ",beta,alpha
                    break #beta cut off#
                alphabeta_output.append([node[0],node[1],v,alpha,beta])
        #print v
        return v
    else:
        v='Infinity'
       # print "Min Player:",node#,node_list[node[1]+1],len(node_list[node[1]+1])
        alphabeta_output.append([node[0],node[1],node[2],alpha,beta])
        for i in range(len(node_list[node[1]+1])):
            if node_list[node[1]+1][i][3] in range(node[3],node[3]+node[4]+1):
      #          print "call via para",node_list[node[1]+1][i],node_list[node[1]+1][i][2],alpha,beta,False
                if v in ('-Infinity','Infinity'):
                    v=min(v,alphabeta(node=node_list[node[1]+1][i],depth=node_list[node[1]+1][i][1],alpha=alpha,beta=beta,maximizingPlayer=True))
                else:
                    v=min(v,alphabeta(node=node_list[node[1]+1][i],depth=node_list[node[1]+1][i][1],alpha=alpha,beta=beta,maximizingPlayer=True))
                if beta in ('-Infinity','Infinity'):
                    backup_beta=beta
                    beta=v
                else:
               #     print "alpha,Beta , v",alpha,beta,v
                    backup_beta=beta
                    beta=min(beta,v)
                #print "Prev State:",node_list[node[1]+1][i]
                node_list[node[1]+1][i][6]=beta
                node[6]=beta
                node[2]=beta

                #print "next node=",node_list[node[1]+1][i]
                #alphabeta_output.append([node_list[node[1]+1][i][0],node_list[node[1]+1][i][1],node_list[node[1]+1][i][2],node_list[node[1]+1][i][5],node_list[node[1]+1][i][6]])
             #   print "For node %s alpha %s beta %s, v %s"%(node,alpha,beta,v)
                #alphabeta_output.append([node[0],node[1],node[2],alpha,beta])
                if alpha not in ('Infinity','-Infinity') and beta not in ('Infinity','-Infinity') and  beta<=alpha:
                #    print "For node %s alpha %s beta %s, v %s"%(node,alpha,backup_beta,v)
                    alphabeta_output.append([node[0],node[1],node[2],alpha,backup_beta])

                    break #Alpha cut off#
                alphabeta_output.append([node[0],node[1],v,alpha,beta])
        #print v
        return v





def alphabeta_print():
    global orig_board,board,alphabeta_output,next_state,node_list
    printarray(node_list)
    outfile = open("traverse_log.txt",'w')
    outfile.write("Node,Depth,Value,Alpha,Beta\n")
    for i in range(len(alphabeta_output)):
        outfile.write(str(alphabeta_output[i][0])+","+str(alphabeta_output[i][1])+","+str(alphabeta_output[i][2])+","+str(alphabeta_output[i][3])+","+str(alphabeta_output[i][4])+"\n")
    outfile.close()

    node=alphabeta_output[len(alphabeta_output)-1]
    #print node
    for i in range(len(alphabeta_output)):
        if alphabeta_output[i][1]==node[1]+1 and alphabeta_output[i][2]==node[2] :
            break
    #print i,alphabeta_output[i]
    out_node=alphabeta_output[i]
    #print out_node
    y=ord(out_node[0][0])-65

    temp=''
    for k in range(1,len(out_node[0])):
        temp=temp+out_node[0][k]

    x=int(temp)-1
    #print x,y
    length_weights=len(orig_board)
    next_state=[]
    next_state=copyboard(orig_board,next_state)
    for m in range(-1, 2):
        for k in range(-1, 2):
            ##print x + m ,y + k,next_state[x + m][y + k]
            if (x + m >= 0 and x + m < length_weights and y + k >= 0 and y + k < length_weights and (
                x + m == x or y + k == y) and next_state[x + m][y + k] == player):
                for i in range(-1,2):
                    for j in range(-1,2):
                        if (x + i >= 0 and x + i < length_weights and y + j >= 0 and y + j < length_weights and (
                                    x + i == x or y + j == y) and next_state[x + i][y + j] == opponent):
                            orig_board[x + i][y + j]=player

    #print "orig_board[x][y]",x,y,len(orig_board),orig_board,orig_board[x][y]
    orig_board[x][y]=player
    board=copyboard(orig_board,board)
    outfile = open("next_state.txt",'w')
    for i in range(len(orig_board)):
        temp = ""
        for j in range(len(orig_board[i])):
            temp = temp + orig_board[i][j]
        outfile.write(temp + "\n")
    outfile.close()





def getAlphaBetaNodeRange():
    global node_list,alpha,beta
    alpha='-Infinity'
    beta='Infinity'
    for i in range(len(node_list)):
        for j in range(len(node_list[i])):
            if i==in_level:
                node_list[i][j].append(node_list[i][j][3])
                node_list[i][j].append(alpha)
                node_list[i][j].append(beta)
            else:
                cntr=0
                for k in range(node_list[i][j][3]+1,len(min_max_arr)):
                    if [min_max_arr[k][1],min_max_arr[k][2]]==[node_list[i][j][1],node_list[i][j][2]]:
                        break
                    else:
                        cntr=cntr+1
                node_list[i][j].append(cntr)
                node_list[i][j].append(alpha)
                node_list[i][j].append(beta)


def read_input():
    global player,opponent,cutoff,weights,board
    player = "X"
    player = txt.readline().rstrip()
    opponent = ""

    if player == 'X':
        opponent = 'O'
    else:
        opponent = 'X'
    #print player, opponent

    # Third line contains the cutoff value
    cutoff = 2
    cutoff = int(txt.readline().rstrip())
    #print cutoff

    for i in range(5):
        temparr = txt.readline().rstrip().split()
        weights.append([])
        for j in range(len(temparr)):
            weights[i].append(int(temparr[j]))

    #print temparr
    #printarray(weights)

    for i in range(5):
        tempstr = txt.readline().rstrip()
        board.append([])
        for j in range(len(tempstr)):
            board[i].append(tempstr[j])

    #print tempstr
    #printarray(board)
    txt.close()











def read_input():
    global player,opponent,cutoff,weights,board,player_bkp,opponent_bkp
    player = "X"
    player = txt.readline().rstrip()
    opponent = ""

    if player == 'X':
        opponent = 'O'
    else:
        opponent = 'X'
    #print player, opponent
    player_bkp=player
    opponent_bkp=opponent
    # Third line contains the cutoff value
    cutoff = 2
    cutoff = int(txt.readline().rstrip())
    #print cutoff

    for i in range(5):
        temparr = txt.readline().rstrip().split()
        weights.append([])
        for j in range(len(temparr)):
            weights[i].append(int(temparr[j]))

    #print temparr
    #printarray(weights)

    for i in range(5):
        tempstr = txt.readline().rstrip()
        board.append([])
        for j in range(len(tempstr)):
            board[i].append(tempstr[j])

    #print tempstr
    #printarray(board)
    txt.close()

#End for read input




"""

For calling the battle simulation

"""

def call_gameplay_input():
    global player_arr,opponent_arr,cutoff_arr,algo_arr,board,weights,player_bkp_arr,opponent_bkp_arr
    player_arr.append(txt.readline().rstrip())
    algo_arr.append(int(txt.readline().rstrip()))
    cutoff_arr.append(int(txt.readline().rstrip()))
    player_arr.append(txt.readline().rstrip())
    algo_arr.append(int(txt.readline().rstrip()))
    cutoff_arr.append(int(txt.readline().rstrip()))

    if player_arr[0]=='X':
        opponent_arr.append('O')
    else:
        opponent_arr.append('X')

    if player_arr[1]=='X':
        opponent_arr.append('O')
    else:
        opponent_arr.append('X')

    player_bkp_arr=copyarray(player_arr,player_bkp_arr)
    opponent_bkp_arr=copyarray(opponent_arr,opponent_bkp_arr)

    for i in range(5):
        temparr = txt.readline().rstrip().split()
        weights.append([])
        for j in range(len(temparr)):
            weights[i].append(int(temparr[j]))


    for i in range(5):
        tempstr = txt.readline().rstrip()
        board.append([])
        for j in range(len(tempstr)):
            board[i].append(tempstr[j])

    txt.close()


def check_board_positions():
    global orig_board
    for i in range(len(orig_board)):
        for j in range(len(orig_board[i])):
            if orig_board[i][j]=='*':
                return True
    return False




weights = []
# board=[['*','*','X','X','*'],['*','*','X','O','X'],['*','*','*','O','*'],['*','*','O','O','*'],['*','*','*','*','*']]
board = []
orig_board=[]
exhaustive_arr=[]
min_max_arr=[]
final_out=[]
node_list=[]
minimax_output=[]

alphabeta_output=[]
alpha=""
beta=""
player=""
opponent=""
cutoff=""
player_bkp=""
opponent_bkp=""
chk_board=True
in_level=""

player_arr=[]
player_bkp_arr=[]
#player2=""
opponent_arr=[]
opponent_bkp_arr=[]
#opponent2=""
algo_arr=[]
#algo2=""
cutoff_arr=[]
#cutoff2=""

fname = sys.argv[-1]
#fname="C:/Users/lenovo poc/Google Drive/usc study material/AI/Assignments/Sample inputs + outputs/4/input.txt"
txt = open(fname)

# First line for deciding the algo
Algo_type = int(txt.readline().rstrip())
print Algo_type
if Algo_type <> 4:
    read_input()
    print "After read player_bkp,opponent_bkp",player_bkp,opponent_bkp
    orig_board=copyboard(board,orig_board)
    in_level=cutoff
    print "Board in read algo type",board
    call_algos()
else:
    call_gameplay_input()
    orig_board=copyboard(board,orig_board)
    print "Board in read algo type",board
    fname="trace_state.txt"
    txt=open(fname,'w')

    incr=0
    while check_board_positions():
        orig_board=copyboard(board,orig_board)
        player=player_arr[incr%2]
        opponent=opponent_arr[incr%2]
        cutoff=cutoff_arr[incr%2]
        Algo_type=algo_arr[incr%2]
        in_level=cutoff
        player_bkp=player_bkp_arr[incr%2]
        opponent_bkp=opponent_bkp_arr[incr%2]
        print ("player,opponent,cutoff,Algo_type,in_level,player_bkp,opponent_bkp",player,opponent,cutoff,Algo_type,in_level,player_bkp,opponent_bkp)
        print "Board At loop no",incr,board
        call_algos()
        orig_board=copyboard(board,orig_board)
        print "Board After loop no;",incr,board,"\n"
        for i in range(len(board)):
            temp=""
            for j in range(len(board[i])):
                temp=temp+board[i][j]
            txt.writelines(temp+"\n")



        incr=incr+1
    txt.close()




